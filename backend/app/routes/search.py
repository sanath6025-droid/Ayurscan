"""
Search API Route for AyurScan.
GET /api/search?q=
Search plants by common name, scientific name, or Ayurvedic name.
"""

from fastapi import APIRouter, Query, HTTPException, status
from app.services.plant_service import plant_service
from app.models.plant import SearchResponse

router = APIRouter(prefix="/api", tags=["Search"])

@router.get(
    "/search",
    response_model=SearchResponse,
    summary="Search plants by name or traditional properties",
    description="Allows quick search across common name, botanical scientific name, and Ayurvedic/Sanskrit name."
)
def search_plants(
    q: str = Query(..., min_length=1, description="Search query string"),
    limit: int = Query(20, ge=1, le=50, description="Max results to return")
):
    query_str = q.strip()
    if not query_str:
        return SearchResponse(query="", count=0, results=[])

    results = plant_service.search_plants(query=query_str, limit=limit)
    return SearchResponse(
        query=query_str,
        count=len(results),
        results=results
    )
