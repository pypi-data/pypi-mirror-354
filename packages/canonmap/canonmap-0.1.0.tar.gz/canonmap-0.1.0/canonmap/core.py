from pathlib import Path
from typing import Optional, Dict, Any, List
import json
import tempfile
import shutil
import zipfile

from .services.artifact_generator import ArtifactGenerator

class CanonMap:
    """Main class for CanonMap functionality."""
    
    def __init__(self):
        """Initialize the CanonMap instance."""
        self.artifact_generator = ArtifactGenerator()
    
    def generate_artifacts(
        self,
        csv_path: str,
        output_path: Optional[str] = None,
        name: str = "data",
        entity_fields: Optional[List[str]] = None,
        use_other_fields_as_metadata: bool = False,
        num_rows: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Generate artifacts from a CSV file.
        
        Args:
            csv_path: Path to the input CSV file
            output_path: Directory to save artifacts (if None, uses temp directory)
            name: Base name for output files
            entity_fields: List of entity fields to extract
            use_other_fields_as_metadata: Whether to include other fields as metadata
            num_rows: Number of rows to process from the CSV
            
        Returns:
            Dictionary containing metadata and schema
        """
        if output_path is None:
            output_path = tempfile.mkdtemp()
            
        result = self.artifact_generator.generate_artifacts_from_csv(
            csv_path=csv_path,
            output_path=output_path,
            name=name,
            entity_fields=entity_fields,
            use_other_fields_as_metadata=use_other_fields_as_metadata,
            num_rows=num_rows
        )
        
        return result
    
    def save_artifacts(
        self,
        artifacts: Dict[str, Any],
        output_path: str,
        name: str = "data",
        save_metadata: bool = True,
        save_schema: bool = True,
    ) -> str:
        """
        Save artifacts to files.
        
        Args:
            artifacts: Dictionary containing metadata and schema
            output_path: Directory to save artifacts
            name: Base name for output files
            save_metadata: Whether to save metadata.json
            save_schema: Whether to save schema.json
            
        Returns:
            Path to the created zip file
        """
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)
        
        files_to_zip = []
        
        if save_metadata:
            meta_file = output_path / "metadata.json"
            meta_file.write_text(json.dumps(artifacts["metadata"], default=str))
            files_to_zip.append(meta_file)
            
        if save_schema:
            schema_file = output_path / "schema.json"
            schema_file.write_text(json.dumps(artifacts["schema"], default=str))
            files_to_zip.append(schema_file)
            
        zip_path = output_path / f"{name}_artifacts.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in files_to_zip:
                zf.write(f, arcname=f.name)
                
        return str(zip_path) 