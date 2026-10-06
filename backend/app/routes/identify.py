"""
Identify API Route for AyurScan.
POST /api/identify
Receives an image, optimizes it, identifies all visible plants with Gemini,
enriches each with MongoDB Ayurvedic data, and returns structured response.
"""

import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.services.image_service import image_service, ImageValidationError
from app.services.gemini_service import (
    gemini_service,
    GeminiServiceError,
    GeminiConfigError,
    GeminiRateLimitError
)
from app.services.plant_service import plant_service
from app.models.plant import IdentifyResponse

logger = logging.getLogger("ayurscan.routes.identify")
router = APIRouter(prefix="/api", tags=["Identification"])

@router.post(
    "/identify",
    response_model=IdentifyResponse,
    summary="Identify all plants present in an uploaded image",
    description="Analyzes the full image with Gemini Vision, detects all distinguishable plants, and enriches them with Ayurvedic information from MongoDB."
)
async def identify_plants(image: UploadFile = File(...)):
    if not image:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No image file provided in upload."
        )

    # Read uploaded bytes
    try:
        content = await image.read()
    except Exception as e:
        logger.error(f"Error reading uploaded file: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not read the uploaded image."
        )

    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty. Please select a valid photo."
        )

    # 1. Validate & optimize image
    try:
        optimized_bytes, mime_type = image_service.validate_and_optimize(
            file_bytes=content,
            declared_mime_type=image.content_type
        )
    except ImageValidationError as ive:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ive)
        )
    except Exception as e:
        logger.error(f"Unexpected image processing error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded image format could not be verified."
        )

    # 2. Analyze with Google Gemini Vision
    try:
        detections = gemini_service.analyze_image(
            image_bytes=optimized_bytes,
            mime_type=mime_type
        )
    except GeminiConfigError as gce:
        logger.error("Gemini API key is not configured in environment.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=gce.message
        )
    except GeminiRateLimitError as rle:
        logger.warning("Gemini rate limit exceeded (HTTP 429).")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=rle.message
        )
    except GeminiServiceError as gse:
        logger.error(f"Gemini service error: {gse.message}")
        raise HTTPException(
            status_code=gse.status_code,
            detail=gse.message
        )
    except Exception as e:
        logger.error(f"Unexpected identification failure: {type(e).__name__}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during plant identification. Please try again."
        )

    # 3. Enrich identified plants with MongoDB Ayurvedic data
    enriched_plants = []
    identified_count = 0
    unclear_count = 0

    for det in detections:
        if det.status == "identified":
            enriched = plant_service.enrich_detection(det)
            enriched_plants.append(enriched)
            identified_count += 1
        else:
            enriched_plants.append(det)
            unclear_count += 1

    return IdentifyResponse(
        total_detected=len(enriched_plants),
        identified_count=identified_count,
        unclear_count=unclear_count,
        plants=enriched_plants
    )
