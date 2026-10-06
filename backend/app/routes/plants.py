"""
Plants API Routes for AyurScan.
GET /api/plants
GET /api/plants/{scientific_name}
"""

import urllib.parse
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from app.services.plant_service import plant_service
from app.models.plant import PlantDatabaseRecord

router = APIRouter(prefix="/api/plants", tags=["Plants"])

@router.get(
    "",
    response_model=List[PlantDatabaseRecord],
    summary="Get list of curated Ayurvedic plants",
    description="Retrieves cataloged Ayurvedic plants with pagination support."
)
def get_plants(
    skip: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(50, ge=1, le=100, description="Maximum plants to return")
):
    return plant_service.get_all_plants(skip=skip, limit=limit)

@router.get(
    "/{scientific_name:path}",
    response_model=PlantDatabaseRecord,
    summary="Get plant details by scientific name",
    description="Fetches comprehensive traditional and botanical records for a specific plant by botanical binomial."
)
def get_plant_by_scientific_name(scientific_name: str):
    decoded_name = urllib.parse.unquote(scientific_name).strip()
    record = plant_service.get_by_scientific_name(decoded_name)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plant with scientific name '{decoded_name}' was not found in the catalog."
        )
    return record
