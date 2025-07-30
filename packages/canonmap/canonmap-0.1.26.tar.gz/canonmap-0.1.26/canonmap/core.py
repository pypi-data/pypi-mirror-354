# canonmap/core.py

import json
import tempfile
from pathlib import Path
from typing import Optional, List, Any, Dict

from canonmap.services.artifact_generator import ArtifactGenerator
from canonmap.services.entity_matcher.entity_matcher import EntityMatcher
from canonmap.utils.logger import get_logger

logger = get_logger()


class CanonMap:
    """Main interface for generating and saving artifacts."""
    def __init__(self):
        self.artifact_generator = ArtifactGenerator()

    def generate_artifacts(
        self,
        csv_path: str,
        output_path: Optional[str] = None,
        name: str = "data",
        entity_fields: Optional[List[str]] = None,
        use_other_fields_as_metadata: bool = False,
        num_rows: Optional[int] = None,
        embed: bool = True,
    ) -> Dict[str, Any]:
        out_dir = Path(output_path) if output_path else Path(tempfile.mkdtemp())
        return self.artifact_generator.generate_artifacts_from_csv(
            csv_path=csv_path,
            output_path=out_dir,
            name=name,
            entity_fields=entity_fields,
            use_other_fields_as_metadata=use_other_fields_as_metadata,
            num_rows=num_rows,
            embed=embed,
        )

    def match_entity(
        self,
        query: str,
        metadata_path: str,
        schema_path: str,
        embedding_path: Optional[str] = None,
        top_k: int = 5,
        threshold: float = 95.0,
        field_filter: Optional[List[str]] = None,
        user_semantic_search: bool = False,
    ) -> List[Dict[str, Any]]:
        logger.info("=" * 80)
        logger.info("Starting entity matching process")
        logger.info("=" * 80)
        logger.info(f"Query: '{query}'")
        logger.info("Parameters:")
        logger.info(f"  - metadata_path:        {metadata_path}")
        logger.info(f"  - schema_path:          {schema_path}")
        logger.info(f"  - embedding_path:       {embedding_path}")
        logger.info(f"  - top_k:                {top_k}")
        logger.info(f"  - threshold:            {threshold}")
        logger.info(f"  - field_filter:         {field_filter}")
        logger.info(f"  - user_semantic_search: {user_semantic_search}")

        # Instantiate matcher once, reusing CPU count from artifact_generator
        matcher = EntityMatcher(
            metadata_path=metadata_path,
            schema_path=schema_path,
            embedding_path=embedding_path,
            semantic_prune=50,                                # or expose as param
            n_jobs=self.artifact_generator.num_cores,
            user_semantic_search=user_semantic_search,
            token_prefilter_k=200                             # or expose as param
        )

        # Generate embedding, reusing the same ArtifactGenerator instance
        q_emb = None
        if user_semantic_search and embedding_path:
            try:
                logger.info("Generating query embedding for semantic search")
                # reuse the embedder you already have
                payload = json.dumps({"query": query}, default=str)
                q_emb = self.artifact_generator._embed_texts([payload])[0]
                logger.info("Successfully generated query embedding")
            except Exception as e:
                logger.warning(
                    "Failed to embed query for semantic search: %s. Falling back to metadata-only.", e
                )

        logger.info("Executing entity match")
        results = matcher.match(
            query=query,
            query_embedding=q_emb,
            top_k=top_k,
            threshold=threshold,
            field_filter=field_filter,
        )

        logger.info("=" * 80)
        logger.info(f"Entity match completed: found {len(results)} results")
        if results:
            logger.info("Top matches:")
            for i, r in enumerate(results[:3], 1):
                logger.info(f"  {i}. '{r['entity']}' (score: {r['score']:.1f})")
        logger.info("=" * 80)

        return results