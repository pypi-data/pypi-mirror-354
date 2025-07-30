# canonmap/services/entity_matcher.py

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

class HybridEntityMatcher:
    """
    Load metadata + embeddings once at startup, build indexes,
    then answer individual match() calls given a query + its embedding.
    """

    def __init__(
        self,
        metadata_path: str,
        embedding_path: str,
        schema_path: str,
        semantic_prune: int = 50,
        n_jobs: int = 4
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

        # 3) Load & normalize embeddings
        arr = np.load(embedding_path)["embeddings"].astype(np.float32)
        if arr.shape[0] != len(self.metadata):
            raise ValueError("Metadata / embeddings count mismatch")
        self.embeddings = normalize(arr, axis=1)

        # 4) Precompute entity strings & phonetics
        self.entities = [m["_canonical_entity_"] for m in self.metadata]
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

        # 6) Build semantic KNN index
        self.semantic_prune = semantic_prune
        self.nn = NearestNeighbors(
            n_neighbors=min(semantic_prune, len(self.embeddings)),
            metric="cosine",
            n_jobs=-1
        )
        self.nn.fit(self.embeddings)

        # 7) Thread pool for parallel scoring
        self._executor = ThreadPoolExecutor(max_workers=n_jobs)

        # 8) Weights for hybrid scoring
        self.weights = {
            "semantic": 0.40,
            "fuzzy":    0.30,
            "fullstr":  0.10,
            "initial":  0.05,
            "keyword":  0.05,
            "phonetic": 0.05
        }

    def _load_schema(self, path: str) -> Dict[str, Any]:
        # (deprecated if loaded in __init__)
        pass

    def _score_one(self, idx: int, query: str, q_emb: np.ndarray, threshold: float) -> Dict[str, Any]:
        ent = self.entities[idx]
        ent_emb = self.embeddings[idx]

        # fuzzy measures
        sc_fuzzy    = fuzz.token_set_ratio(query, ent)
        sc_fullstr  = fuzz.token_sort_ratio(query, ent)
        sc_pho      = 100 if doublemetaphone(query)[0] == self.phonetics[idx] else 0
        sc_initial  = 100 if "".join(w[0] for w in query.split()).lower() == "".join(w[0] for w in ent.split()).lower() else 0
        sc_keyword  = 100 if query.strip().lower() == ent.strip().lower() else 0

        # semantic
        sc_semantic = float(np.dot(q_emb, ent_emb)) * 100

        # last-name bonus
        last_name   = ent.strip().lower().split()[-1] if ent else ""
        bonus_last  = 10 if last_name in query.lower().split() else 0

        # weighted total
        total = (
            sc_semantic * self.weights["semantic"]
          + sc_fuzzy    * self.weights["fuzzy"]
          + sc_fullstr  * self.weights["fullstr"]
          + sc_initial  * self.weights["initial"]
          + sc_keyword  * self.weights["keyword"]
          + sc_pho      * self.weights["phonetic"]
          + bonus_last
        )
        total = min(total, 100)

        passes = sum(1 for v in [sc_semantic, sc_fuzzy, sc_fullstr, sc_pho, sc_initial, sc_keyword] if v >= threshold)

        return {
            "entity":    ent,
            "score":     total,
            "passes":    passes,
            "metadata":  self.metadata[idx],
        }

    def match(
        self,
        query: str,
        query_embedding: np.ndarray,
        top_k: int = 5,
        threshold: float = 95.0,
        field_filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Returns up to `top_k` matches for `query` with precomputed `query_embedding`.
        """

        q_norm = query.strip().lower()
        # 1) Try exact / phonetic bucket
        bucket = set(self.exact_index.get(q_norm, []) + self.phonetic_index.get(doublemetaphone(query)[0], []))
        if bucket:
            # apply filter
            idxs = [i for i in bucket if not field_filter or all(self.metadata[i].get(k)==v for k,v in field_filter.items())]
            if idxs:
                # score in parallel
                results = list(self._executor.map(lambda i: self._score_one(i, query, query_embedding, threshold), idxs))
                results.sort(key=lambda x: (-x["passes"], -x["score"]))
                return results[:top_k]

        # 2) Fallback to semantic KNN
        q_emb = query_embedding / (np.linalg.norm(query_embedding) + 1e-12)
        dists, nbrs = self.nn.kneighbors(q_emb.reshape(1,-1), return_distance=True)
        candidates = nbrs[0]
        # apply filter
        if field_filter:
            candidates = [i for i in candidates if all(self.metadata[i].get(k)==v for k,v in field_filter.items())]
        # score
        results = list(self._executor.map(lambda i: self._score_one(i, query, q_emb, threshold), candidates))
        results.sort(key=lambda x: (-x["passes"], -x["score"]))
        return results[:top_k]