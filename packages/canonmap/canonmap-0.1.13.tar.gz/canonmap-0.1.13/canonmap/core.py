# canonmap/core.py
import tempfile
from pathlib import Path
from typing import Optional, List, Any, Dict

from .services.artifact_generator import ArtifactGenerator


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