# File: canonmap/core.py

import json
import tempfile
from pathlib import Path
from typing import Optional, List, Any, Dict

from canonmap.services.artifact_generator import ArtifactGenerator
from canonmap.services.entity_matcher.entity_matcher import EntityMatcher
from canonmap.utils.logger import get_logger

logger = get_logger()


class CanonMap:
    """
    Main interface for generating and saving artifacts, and performing entity matching.
    
    This class provides high-level methods for:
    1. Generating artifacts from CSV files (metadata, schema, embeddings)
    2. Matching entities against generated artifacts using various matching strategies
    
    The entity matching process uses a combination of:
    - Semantic search (using transformer embeddings)
    - Fuzzy string matching
    - Phonetic matching
    - Initial matching
    - Keyword matching
    - Full string matching
    """

    def __init__(self):
        """Initialize the CanonMap with an ArtifactGenerator instance."""
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
        Generate artifacts from a CSV file.

        Args:
            csv_path (str): Path to the input CSV file
            output_path (Optional[str]): Directory to save artifacts. If None, uses a temporary directory
            name (str): Base name for output files (default: "data")
            entity_fields (Optional[List[str]]): List of column names to treat as entity fields.
                If None, automatically detects entity fields
            use_other_fields_as_metadata (bool): If True, includes all non-entity columns as metadata
            num_rows (Optional[int]): Number of rows to process. If None, processes all rows
            embed (bool): Whether to compute and save embeddings for entities

        Returns:
            Dict[str, Any]: Dictionary containing:
                - "metadata": List of entity objects with their metadata
                - "schema": Nested dictionary of data types and formats
                - "paths": Dictionary of paths to saved artifacts
                - "embeddings": Optional numpy array of entity embeddings
        """
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
        threshold: float = 0,
        field_filter: Optional[List[str]] = None,
        use_semantic_search: bool = False,
        weights: Optional[Dict[str, float]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Match a query string against entities in the generated artifacts.

        The matching process uses a weighted combination of multiple matching strategies:
        - Semantic matching (45%): Uses transformer embeddings for semantic similarity
        - Fuzzy matching (35%): Uses fuzzy string matching for typo tolerance
        - Initial matching (10%): Matching of initials/abbreviations
        - Keyword matching (5%): Matching of individual words
        - Phonetic matching (5%): Sound-based matching using Double Metaphone

        Additional scoring bonuses are applied:
        - +10 points if both semantic and fuzzy scores are > 80
        - -15 points if fuzzy score > 90 but semantic score < 60
        - +10 points for perfect initial matching
        - +5 points for perfect phonetic matching

        Args:
            query (str): The query string to match
            metadata_path (str): Path to the metadata.pkl file
            schema_path (str): Path to the schema.pkl file
            embedding_path (Optional[str]): Path to the embeddings.npz file (required for semantic search)
            top_k (int): Maximum number of results to return (default: 5)
            threshold (float): Minimum score threshold for matches (default: 0)
            field_filter (Optional[List[str]]): List of field names to restrict matching to
            use_semantic_search (bool): Whether to enable semantic search (default: False)
            weights (Optional[Dict[str, float]]): Custom weights for different matching strategies.
                Default weights if not provided:
                {
                    'semantic': 0.45,  # Transformer-based semantic similarity
                    'fuzzy': 0.35,     # Fuzzy string matching
                    'initial': 0.10,   # Initial/abbreviation matching
                    'keyword': 0.05,   # Individual word matching
                    'phonetic': 0.05   # Sound-based matching
                }

        Returns:
            List[Dict[str, Any]]: List of match results, each containing:
                - 'entity': The matched entity string
                - 'score': Overall match score (0-100)
                - 'passes': Number of individual matching strategies that passed
                - 'metadata': Dictionary of entity metadata
        """
        logger.info("Starting entity matching process")
        logger.info(f"Query: '{query}'")
        logger.info(f"Parameters: top_k={top_k}, threshold={threshold}, semantic_search={use_semantic_search}")

        matcher = EntityMatcher(
            metadata_path=metadata_path,
            schema_path=schema_path,
            embedding_path=embedding_path,
            embedding_model=lambda txt: self.artifact_generator._embed_texts([txt])[0],
            semantic_prune=50,
            n_jobs=self.artifact_generator.num_cores,
            use_semantic_search=use_semantic_search,
            token_prefilter_k=200,
            weights=weights,
        )

        q_emb = None
        if use_semantic_search and embedding_path:
            try:
                q_emb = self.artifact_generator._embed_texts([query])[0]
            except Exception:
                logger.warning("Failed to compute query embedding; proceeding without semantic scores")

        results = matcher.match(
            query=query,
            query_embedding=q_emb,
            top_k=top_k,
            threshold=threshold,
            field_filter=field_filter,
        )

        logger.info(f"Entity match completed: found {len(results)} results")
        if results:
            logger.info("Top matches:")
            for i, r in enumerate(results[:top_k], 1):
                logger.info(f"  {i}. '{r['entity']}' (score: {r['score']:.1f})")
        return results
