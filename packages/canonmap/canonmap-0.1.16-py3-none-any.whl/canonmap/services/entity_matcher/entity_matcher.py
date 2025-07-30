# File: canonmap/services/entity_matcher/entity_matcher.py

import pickle
import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Any
from concurrent.futures import ThreadPoolExecutor

from rapidfuzz import fuzz
from metaphone import doublemetaphone
from sklearn.preprocessing import normalize
from sklearn.neighbors import NearestNeighbors

from canonmap.utils.logger import get_logger

logger = get_logger()

class EntityMatcher:
    """
    Load metadata + optional embeddings once at startup, build indexes,
    then answer match() calls with or without semantic search.
    """

    def __init__(
        self,
        metadata_path: str,
        schema_path: str,
        embedding_path: Optional[str] = None,
        semantic_prune: int = 50,
        n_jobs: int = 4,
        user_semantic_search: bool = False,
    ):
        # 1) Load schema
        schema_file = Path(schema_path)
        if schema_file.suffix == ".pkl":
            self.schema = pickle.loads(schema_file.read_bytes())
        else:
            self.schema = json.loads(schema_file.read_text())

        # 2) Load metadata
        meta_file = Path(metadata_path)
        self.metadata: List[Dict[str, Any]] = pickle.loads(meta_file.read_bytes())

        # 3) Determine semantic mode
        self.semantic_enabled = False
        if user_semantic_search:
            if embedding_path and Path(embedding_path).exists():
                self._load_embeddings(embedding_path, semantic_prune)
                self.semantic_enabled = True
                logger.info("Semantic search enabled with embeddings '%s'", embedding_path)
            else:
                logger.warning(
                    "Semantic search requested but embeddings not found at '%s'. "
                    "Falling back to metadata-only matching.",
                    embedding_path
                )
        else:
            if embedding_path:
                logger.info(
                    "Embeddings passed at '%s' but semantic search disabled. "
                    "Ignoring embeddings.",
                    embedding_path
                )
        # 4) Precompute entity names & phonetics
        self.entities = [m['_canonical_entity_'] for m in self.metadata]
        self.phonetics = [doublemetaphone(e)[0] for e in self.entities]

        # 5) Build lookup buckets
        self.exact_index: Dict[str, List[int]] = {}
        self.phonetic_index: Dict[str, List[int]] = {}
        for i, (ent, ph) in enumerate(zip(self.entities, self.phonetics)):
            key = ent.strip().lower()
            if key:
                self.exact_index.setdefault(key, []).append(i)
            if ph:
                self.phonetic_index.setdefault(ph, []).append(i)

        # 6) Thread pool for scoring
        self._executor = ThreadPoolExecutor(max_workers=n_jobs)

        # 7) Weights
        self.weights = {
            'semantic': 0.40,
            'fuzzy':    0.30,
            'fullstr':  0.10,
            'initial':  0.05,
            'keyword':  0.05,
            'phonetic': 0.05,
        }

    def _load_embeddings(self, embedding_path: str, semantic_prune: int):
        arr = np.load(embedding_path)['embeddings'].astype(np.float32)
        if arr.shape[0] != len(self.metadata):
            raise ValueError("Metadata / embeddings count mismatch")
        self.embeddings = normalize(arr, axis=1)
        # semantic KNN index
        self.nn = NearestNeighbors(
            n_neighbors=min(semantic_prune, len(self.embeddings)),
            metric='cosine', n_jobs=-1
        )
        self.nn.fit(self.embeddings)

    def _score_one(
        self, idx: int, query: str, q_emb: Optional[np.ndarray], threshold: float
    ) -> Dict[str, Any]:
        ent = self.entities[idx]
        ent_emb = self.embeddings[idx] if self.semantic_enabled else None

        # fuzzy measures
        sc_fuzzy   = fuzz.token_set_ratio(query, ent)
        sc_fullstr = fuzz.token_sort_ratio(query, ent)
        sc_pho     = 100 if doublemetaphone(query)[0] == self.phonetics[idx] else 0
        sc_initial = (
            100
            if ''.join(w[0] for w in query.split()).lower()
               == ''.join(w[0] for w in ent.split()).lower()
            else 0
        )
        sc_keyword = 100 if query.strip().lower() == ent.strip().lower() else 0

        # semantic
        if self.semantic_enabled and q_emb is not None:
            sc_semantic = float(np.dot(q_emb, ent_emb)) * 100
        else:
            sc_semantic = 0.0

        # last-name bonus
        last_name = ent.strip().lower().split()[-1] if ent else ''
        bonus_last = 10 if last_name in query.lower().split() else 0

        total = (
            sc_semantic * self.weights['semantic']
          + sc_fuzzy   * self.weights['fuzzy']
          + sc_fullstr * self.weights['fullstr']
          + sc_initial * self.weights['initial']
          + sc_keyword * self.weights['keyword']
          + sc_pho     * self.weights['phonetic']
          + bonus_last
        )
        total = min(total, 100)

        passes = sum(
            1
            for v in [sc_semantic, sc_fuzzy, sc_fullstr, sc_pho, sc_initial, sc_keyword]
            if v >= threshold
        )

        return {'entity': ent, 'score': total, 'passes': passes, 'metadata': self.metadata[idx]}

    def match(
        self,
        query: str,
        query_embedding: Optional[np.ndarray] = None,
        top_k: int = 5,
        threshold: float = 95.0,
        field_filter: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        q_norm = query.strip().lower()
        # 1) exact / phonetic buckets
        bucket = set(
            self.exact_index.get(q_norm, [])
            + self.phonetic_index.get(doublemetaphone(query)[0], [])
        )
        if bucket:
            idxs = [
                i for i in bucket
                if not field_filter or all(
                    self.metadata[i].get(k) == v for k, v in field_filter.items()
                )
            ]
            if idxs:
                results = list(
                    self._executor.map(lambda i: self._score_one(i, query, query_embedding, threshold), idxs)
                )
                results.sort(key=lambda x: (-x['passes'], -x['score']))
                return results[:top_k]

        # 2) fallback
        if self.semantic_enabled and query_embedding is not None:
            q_emb = query_embedding / (np.linalg.norm(query_embedding) + 1e-12)
            dists, nbrs = self.nn.kneighbors(q_emb.reshape(1, -1), return_distance=True)
            candidates = nbrs[0]
        else:
            # metadata-only fallback: score all
            logger.info("Performing metadata-only fallback over all entities")
            candidates = list(range(len(self.entities)))

        if field_filter:
            candidates = [
                i for i in candidates
                if all(self.metadata[i].get(k) == v for k, v in field_filter.items())
            ]

        results = list(
            self._executor.map(lambda i: self._score_one(i, query, query_embedding, threshold), candidates)
        )
        results.sort(key=lambda x: (-x['passes'], -x['score']))
        return results[:top_k]