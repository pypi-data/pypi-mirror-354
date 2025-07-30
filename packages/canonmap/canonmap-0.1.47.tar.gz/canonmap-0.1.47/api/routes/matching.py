from fastapi import APIRouter, HTTPException
from typing import List
from ..models.schemas import MatchRequest, MatchResult
from canonmap import CanonMap

router = APIRouter()

@router.post("/match-entity/", response_model=List[MatchResult])
async def match_entity(request: MatchRequest):
    """
    Match an entity against the database using various strategies.
    
    The matching process combines multiple strategies with configurable weights:
    - Semantic matching (45% by default, enabled with use_semantic_search)
    - Fuzzy matching (35% by default)
    - Initial matching (10% by default)
    - Keyword matching (5% by default)
    - Phonetic matching (5% by default)
    
    Additional scoring bonuses are applied for:
    - High semantic + fuzzy score combinations (+10 points)
    - Perfect initial matches (+10 points)
    - Perfect phonetic matches (+5 points)
    - Penalties for mismatched high fuzzy/low semantic scores (-15 points)
    
    Args:
        use_semantic_search (bool): Whether to enable semantic search (default: False)
        threshold (float): Minimum score threshold for matches (default: 0)
    """
    try:
        canonmap = CanonMap()
        results = canonmap.match_entity(
            query=request.query,
            metadata_path=request.metadata_path,
            schema_path=request.schema_path,
            embedding_path=request.embedding_path,
            top_k=request.top_k,
            threshold=request.threshold,
            field_filter=request.field_filter,
            use_semantic_search=request.use_semantic_search,
            weights=request.weights
        )
        
        return [
            MatchResult(
                entity=result["entity"],
                score=result["score"],
                passes=result["passes"],
                metadata=result["metadata"]
            )
            for result in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 