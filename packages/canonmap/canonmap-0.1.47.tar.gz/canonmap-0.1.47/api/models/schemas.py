from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class GenerateRequest(BaseModel):
    """Request model for artifact generation."""
    csv_path: str = Field(..., description="Path to the input CSV file")
    output_path: Optional[str] = Field(None, description="Directory to save artifacts")
    name: str = Field("data", description="Base name for output files")
    entity_fields: Optional[List[str]] = Field(None, description="List of column names to treat as entity fields")
    use_other_fields_as_metadata: bool = Field(False, description="Include all non-entity columns as metadata")
    num_rows: Optional[int] = Field(None, description="Number of rows to process")
    embed: bool = Field(True, description="Whether to compute and save embeddings")

class MatchRequest(BaseModel):
    """Request model for entity matching."""
    query: str = Field(..., description="The query string to match")
    metadata_path: str = Field(..., description="Path to the metadata.pkl file")
    schema_path: str = Field(..., description="Path to the schema.pkl file")
    embedding_path: Optional[str] = Field(None, description="Path to the embeddings.npz file")
    top_k: int = Field(5, description="Maximum number of results to return")
    threshold: float = Field(0, description="Minimum score threshold for matches")
    field_filter: Optional[List[str]] = Field(None, description="List of field names to restrict matching to")
    use_semantic_search: bool = Field(False, description="Whether to enable semantic search")
    weights: Optional[Dict[str, float]] = Field(None, description="Custom weights for different matching strategies")

class MatchResult(BaseModel):
    """Response model for a single match result."""
    entity: str = Field(..., description="The matched entity string")
    score: float = Field(..., description="Overall match score (0-100)")
    passes: int = Field(..., description="Number of individual matching strategies that passed")
    metadata: Dict[str, Any] = Field(..., description="Dictionary of entity metadata")

class GenerateResponse(BaseModel):
    """Response model for artifact generation."""
    metadata: List[Dict[str, Any]] = Field(..., description="List of entity objects with their metadata")
    data_schema: Dict[str, Any] = Field(..., description="Nested dictionary of data types and formats")
    paths: Dict[str, str] = Field(..., description="Dictionary of paths to saved artifacts")
    embeddings: Optional[List[float]] = Field(None, description="Optional list of entity embeddings") 