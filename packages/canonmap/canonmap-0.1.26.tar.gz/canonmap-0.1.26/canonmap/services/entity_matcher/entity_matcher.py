# File: canonmap/services/entity_matcher/entity_matcher.py

import pickle
import numpy as np
import re
from pathlib import Path
from typing import List, Optional, Any, Dict
from concurrent.futures import ThreadPoolExecutor

from rapidfuzz import fuzz
from metaphone import doublemetaphone
from sklearn.preprocessing import normalize
from sklearn.neighbors import NearestNeighbors

try:
    import faiss
    HAS_FAISS = True
except ImportError:
    HAS_FAISS = False

from canonmap.utils.logger import get_logger
logger = get_logger()

# in-process cache for ANN index and embeddings
_ann_cache: Dict[str, Any] = {}

def _get_ann_index(embedding_path: str, prune: int):
    if embedding_path not in _ann_cache:
        arr = np.load(embedding_path)["embeddings"].astype(np.float32)
        arr = normalize(arr, axis=1)
        if HAS_FAISS:
            dim = arr.shape[1]
            idx = faiss.IndexFlatIP(dim)
            faiss.normalize_L2(arr)
            idx.add(arr)
        else:
            idx = NearestNeighbors(n_neighbors=min(prune, len(arr)),
                                   metric="cosine", n_jobs=-1)
            idx.fit(arr)
        _ann_cache[embedding_path] = (idx, arr)
    return _ann_cache[embedding_path]


class EntityMatcher:
    """
    High-performance matcher with optional semantic search and per-call field filtering.
    """

    def __init__(
        self,
        metadata_path: str,
        schema_path: str,
        embedding_path: Optional[str] = None,
        semantic_prune: int = 50,
        n_jobs: int = 4,
        user_semantic_search: bool = False,
        token_prefilter_k: int = 200,
    ):
        logger.info("Initializing EntityMatcher")
        logger.info(f"  metadata_path: {metadata_path}")
        logger.info(f"  schema_path:   {schema_path}")
        logger.info(f"  embeddings:    {embedding_path}")
        logger.info(f"  semantic_prune:{semantic_prune}")
        logger.info(f"  n_jobs:        {n_jobs}")
        logger.info(f"  semantic_on:   {user_semantic_search}")

        # load metadata list
        self.metadata: List[Dict[str, Any]] = pickle.loads(Path(metadata_path).read_bytes())
        self.N = len(self.metadata)

        # precompute entity strings, tokens, phonetics
        self.entities = [m["_canonical_entity_"] for m in self.metadata]
        self.entity_tokens: List[set] = []
        self.token_index: Dict[str, List[int]] = {}
        self.phonetics: List[str] = []
        for i, ent in enumerate(self.entities):
            lo = ent.lower()
            toks = set(re.findall(r"\w+", lo))
            self.entity_tokens.append(toks)
            for t in toks:
                self.token_index.setdefault(t, []).append(i)
            self.phonetics.append(doublemetaphone(ent)[0])

        # exact & phonetic buckets
        self.exact_index: Dict[str, List[int]] = {}
        self.phonetic_index: Dict[str, List[int]] = {}
        for i, ent in enumerate(self.entities):
            key = ent.strip().lower()
            if key:
                self.exact_index.setdefault(key, []).append(i)
        for i, ph in enumerate(self.phonetics):
            if ph:
                self.phonetic_index.setdefault(ph, []).append(i)

        # build semantic ANN if requested
        self.semantic_enabled = False
        if user_semantic_search and embedding_path and Path(embedding_path).exists():
            idx, arr = _get_ann_index(embedding_path, semantic_prune)
            self.embeddings = arr
            if HAS_FAISS:
                self.ann = idx
            else:
                self.nn = idx
            self.ann_k = min(semantic_prune, self.N)
            self.semantic_enabled = True
            logger.info("Semantic ANN ready (%s)", "FAISS" if HAS_FAISS else "sklearn")
        elif user_semantic_search:
            logger.warning("Semantic search requested but embeddings missing; disabling semantic.")

        # thread pool & weights
        self.pool = ThreadPoolExecutor(max_workers=n_jobs)
        self.weights = {
            "semantic": 0.40,
            "fuzzy":    0.30,
            "fullstr":  0.10,
            "initial":  0.05,
            "keyword":  0.05,
            "phonetic": 0.05,
        }
        self.token_prefilter_k = token_prefilter_k

    def match(
        self,
        query: str,
        query_embedding: Optional[np.ndarray] = None,
        top_k: int = 5,
        threshold: float = 95.0,
        field_filter: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        q = query.strip().lower()

        # 1) exact/phonetic bucket
        bucket = set(self.exact_index.get(q, []))
        bucket |= set(self.phonetic_index.get(doublemetaphone(q)[0], []))
        if bucket:
            cand = list(bucket)
        else:
            # 2) token prefilter
            toks = re.findall(r"\w+", q)
            counts: Dict[int,int] = {}
            for t in toks:
                for i in self.token_index.get(t, []):
                    counts[i] = counts.get(i, 0) + 1
            if counts:
                cand = sorted(counts, key=lambda i: -counts[i])[:self.token_prefilter_k]
            else:
                cand = list(range(self.N))

            # 3) semantic prune
            if self.semantic_enabled and query_embedding is not None:
                q_emb = query_embedding / (np.linalg.norm(query_embedding) + 1e-12)
                if HAS_FAISS:
                    _, I = self.ann.search(q_emb[np.newaxis, :], self.ann_k)
                    ann_ids = set(I[0])
                else:
                    _, I = self.nn.kneighbors(q_emb.reshape(1, -1), return_distance=True)
                    ann_ids = set(I[0])
                cand = list(set(cand) & ann_ids)

        # 4) apply field_filter by field_name if given
        if field_filter:
            cand = [i for i in cand if self.metadata[i].get("_field_name_") in field_filter]

        return self._score_and_rank(cand, q, query_embedding, threshold, top_k)

    def _score_and_rank(
        self,
        idxs: List[int],
        q: str,
        q_emb: Optional[np.ndarray],
        threshold: float,
        top_k: int,
    ) -> List[Dict[str, Any]]:
        sem_scores = None
        if self.semantic_enabled and q_emb is not None:
            mat = self.embeddings[idxs]
            sem_scores = mat.dot(q_emb) * 100

        futures, results = [], []
        def _score(i, s_val):
            ent = self.entities[i]
            sc = {
                "semantic": s_val or 0.0,
                "fuzzy": fuzz.token_set_ratio(q, ent),
                "fullstr": fuzz.token_sort_ratio(q, ent),
                "phonetic": 100 if doublemetaphone(q)[0] == self.phonetics[i] else 0,
                "initial": 100 if "".join(w[0] for w in q.split()) == "".join(w[0] for w in ent.split()) else 0,
                "keyword": 100 if q == ent.lower().strip() else 0,
            }
            bonus = 10 if ent.split()[-1].lower() in q.split() else 0
            total = sum(sc[k] * self.weights[k] for k in sc) + bonus
            total = min(total, 100)
            passes = sum(1 for v in sc.values() if v >= threshold)
            return {"entity": ent, "score": total, "passes": passes, "metadata": self.metadata[i]}

        for pos, idx in enumerate(idxs):
            val = sem_scores[pos] if sem_scores is not None else 0.0
            futures.append(self.pool.submit(_score, idx, val))
        for f in futures:
            results.append(f.result())

        filtered = [r for r in results if r["passes"] > 0] or results
        filtered.sort(key=lambda r: (-r["passes"], -r["score"]))
        return filtered[:top_k]