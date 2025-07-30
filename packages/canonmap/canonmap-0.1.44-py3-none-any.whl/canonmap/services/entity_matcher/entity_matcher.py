from pathlib import Path
import pickle
import re
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional, Any, Dict, Callable

import numpy as np
from rapidfuzz import fuzz
from metaphone import doublemetaphone
from sklearn.preprocessing import normalize
from sklearn.neighbors import NearestNeighbors

from canonmap.utils.logger import get_logger
logger = get_logger()


class EntityMatcher:
    """
    Matcher with semantic search (sklearn ANN), and customizable scoring weights.
    Always performs semantic prune first, then scores candidates, allowing
    an override to return an exact number of results.
    """

    def __init__(
        self,
        metadata_path: str,
        schema_path: str,
        embedding_path: Optional[str],
        embedding_model: Callable[[str], np.ndarray],
        semantic_prune: int = 50,
        n_jobs: int = 4,
        user_semantic_search: bool = False,
        token_prefilter_k: int = 200,
        weights: Optional[Dict[str, float]] = None,
    ):
        logger.info("Initializing EntityMatcher with custom weights and semantic_search=%s", user_semantic_search)
        logger.info(f"  metadata:  {metadata_path}")
        logger.info(f"  schema:    {schema_path}")
        logger.info(f"  embeddings: {embedding_path}")
        logger.info(f"  semantic_prune: {semantic_prune}")
        logger.info(f"  n_jobs: {n_jobs}")

        # load metadata
        self.metadata: List[Dict[str, Any]] = pickle.loads(Path(metadata_path).read_bytes())
        self.N = len(self.metadata)

        # embedder for on-the-fly embeddings
        self.embed = embedding_model

        # scoring weights (matching old ratios)
        self.weights = weights or {
            'semantic': 0.45,
            'fuzzy':    0.35,
            'initial':  0.10,
            'keyword':  0.05,
            'phonetic': 0.05,
        }
        logger.info("Using scoring weights: %s", self.weights)

        # precompute entities and phonetic codes
        self.entities = [m['_canonical_entity_'] for m in self.metadata]
        self.phonetics = [doublemetaphone(ent)[0] for ent in self.entities]

        # semantic ANN via sklearn
        self.semantic_enabled = False
        if user_semantic_search and embedding_path and Path(embedding_path).exists():
            arr = np.load(embedding_path)["embeddings"].astype(np.float32)
            if arr.shape[0] != self.N:
                raise ValueError("Metadata/embeddings mismatch")
            self.embeddings = normalize(arr, axis=1)
            self.nn = NearestNeighbors(
                n_neighbors=min(semantic_prune, self.N),
                metric='cosine',
                n_jobs=n_jobs
            )
            self.nn.fit(self.embeddings)
            self.semantic_prune = min(semantic_prune, self.N)
            self.semantic_enabled = True
            logger.info("Built sklearn KNN index on %d vectors", self.N)
        elif user_semantic_search:
            logger.warning("Requested semantic search but no embeddings found; disabled.")

        # thread pool for scoring
        self.pool = ThreadPoolExecutor(max_workers=n_jobs)

    def match(
        self,
        query: str,
        query_embedding: Optional[np.ndarray] = None,
        top_k: int = 5,
        threshold: float = 95.0,
        num_results_returned: Optional[int] = None,
        field_filter: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        q = query.strip().lower()

        # embed on the fly if needed
        if self.semantic_enabled and query_embedding is None:
            query_embedding = self.embed(query)

        # prepare normalized query embedding
        q_emb = None
        if self.semantic_enabled and query_embedding is not None:
            q_emb = query_embedding.astype(np.float32)
            q_emb = q_emb / (np.linalg.norm(q_emb) + 1e-12)

        # semantic prune first
        if self.semantic_enabled and q_emb is not None:
            _, nbrs = self.nn.kneighbors(q_emb.reshape(1, -1), return_distance=True)
            cand = list(nbrs[0])
        else:
            cand = list(range(self.N))

        # apply field filter if provided
        if field_filter:
            cand = [i for i in cand if self.metadata[i].get('_field_name_') in field_filter]

        # score and rank
        return self._score_and_rank(cand, q, q_emb, threshold, top_k, num_results_returned)

    def _score_and_rank(
        self,
        idxs: List[int],
        q: str,
        q_emb: Optional[np.ndarray],
        threshold: float,
        top_k: int,
        num_results_returned: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        sem_scores = None
        if self.semantic_enabled and q_emb is not None:
            mat = self.embeddings[idxs]
            sem_scores = mat.dot(q_emb) * 100

        futures = []
        results = []

        def _score(i, sem_val):
            ent = self.entities[i]
            sc = {
                'semantic': sem_val or 0.0,
                'fuzzy': fuzz.token_set_ratio(q, ent),
                'phonetic': 100 if doublemetaphone(q)[0] == self.phonetics[i] else 0,
                'initial': 100 if ''.join(w[0] for w in q.split()) == ''.join(w[0] for w in ent.split()) else 0,
                'keyword': 100 if q == ent.lower().strip() else 0,
            }
            # compute weighted total
            total = sum(sc[k] * self.weights[k] for k in sc)
            # reintroduce cross-metric bonuses from old logic
            if sc['semantic'] > 80 and sc['fuzzy'] > 80:
                total += 10
            if sc['fuzzy'] > 90 and sc['semantic'] < 60:
                total -= 15
            if sc['initial'] == 100:
                total += 10
            if sc['phonetic'] == 100:
                total += 5
            total = min(total, 100)

            passes = sum(1 for v in sc.values() if v >= threshold)
            return {
                'entity': ent,
                'score': total,
                'passes': passes,
                'metadata': self.metadata[i],
            }

        for idx, i in enumerate(idxs):
            sem_val = sem_scores[idx] if sem_scores is not None else 0.0
            futures.append(self.pool.submit(_score, i, sem_val))
        for f in futures:
            results.append(f.result())

        # if the caller wants an exact count, ignore threshold/passes
        if num_results_returned is not None:
            sorted_all = sorted(results, key=lambda r: -r['score'])
            return sorted_all[:num_results_returned]

        # else apply pass-based filtering and top_k
        filtered = [r for r in results if r['passes'] > 0] or results
        filtered.sort(key=lambda r: (-r['passes'], -r['score']))
        return filtered[:top_k]
