# canonmap/core.py

import json
import tempfile
from pathlib import Path
from typing import Optional, List, Any, Dict

from canonmap.services.artifact_generator import ArtifactGenerator
from canonmap.services.entity_matcher import EntityMatcher
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
        """
        Generate metadata, schema, and optionally embeddings from a CSV file.

        Args:
            csv_path: path to input CSV
            output_path: directory to write artifacts
            name: base name for artifacts
            entity_fields: list of columns to treat as entities
            use_other_fields_as_metadata: include other fields in entity metadata
            num_rows: limit rows processed
            embed: whether to compute and save embeddings (default True)
        Returns:
            dict with keys 'paths', 'metadata', 'schema', and optionally 'embeddings'
        """
        out_dir = Path(output_path) if output_path else Path(tempfile.mkdtemp())
        result = self.artifact_generator.generate_artifacts_from_csv(
            csv_path=csv_path,
            output_path=out_dir,
            name=name,
            entity_fields=entity_fields,
            use_other_fields_as_metadata=use_other_fields_as_metadata,
            num_rows=num_rows,
            embed=embed,
        )
        return result
    

    def match_entity(
        self,
        query: str,
        metadata_path: str,
        schema_path: str,
        embedding_path: Optional[str] = None,
        top_k: int = 5,
        threshold: float = 95.0,
        field_filter: Optional[Dict[str, Any]] = None,
        user_semantic_search: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        Match a query against precomputed metadata (and embeddings if enabled).
        """
        logger.info(
            "Entity match requested: '%s', semantic_search=%s", query, user_semantic_search
        )
        matcher = EntityMatcher(
            metadata_path=metadata_path,
            schema_path=schema_path,
            embedding_path=embedding_path,
            user_semantic_search=user_semantic_search,
        )
        # if semantic_search requested but embeddings missing, EntityMatcher logs a warning
        # now perform match
        # query_embedding is required if semantic search is enabled
        q_emb = None
        if user_semantic_search and embedding_path:
            try:
                # simple embed: load one-off model? or reuse same embedder? assume external embedding
                from .services.artifact_generator import ArtifactGenerator
                # instantiate a temporary embedder
                embedder = ArtifactGenerator()
                q_emb = embedder._embed_texts([json.dumps({"query": query}, default=str)])[0]
            except Exception as e:
                logger.warning(
                    "Failed to embed query for semantic search: %s. Continuing metadata-only.", e
                )
        results = matcher.match(
            query=query,
            query_embedding=q_emb,
            top_k=top_k,
            threshold=threshold,
            field_filter=field_filter,
        )
        logger.info("Entity match completed: found %d results", len(results))
        return results