"""
Plant Information Service for AyurScan.
Matches Gemini vision identification results with curated Ayurvedic records from MongoDB.
"""

import logging
from typing import Optional, List, Dict, Any
from app.database.mongodb import db_manager
from app.models.plant import (
    AyurvedicInfo,
    PlantDetectionResult,
    PlantDatabaseRecord
)

logger = logging.getLogger("ayurscan.plant_service")

class PlantService:
    def enrich_detection(self, detection: PlantDetectionResult) -> PlantDetectionResult:
        """
        Enriches an identified plant detection result with Ayurvedic data from MongoDB.
        Uses scientific_name as primary match key.
        """
        if detection.status != "identified" or not detection.scientific_name:
            return detection

        record = db_manager.find_by_scientific_name(detection.scientific_name)

        if record:
            detection.ayurvedic_info = AyurvedicInfo(
                category=record.get("category"),
                ayurvedic_name=record.get("ayurvedic_name"),
                family=record.get("family"),
                description=record.get("description"),
                ayurvedic_uses=record.get("ayurvedic_uses", []),
                traditional_uses=record.get("traditional_uses", []),
                plant_parts_used=record.get("plant_parts_used", []),
                precautions=record.get("precautions", []),
                warnings=record.get("warnings", []),
                image_url=record.get("image_url"),
                video_url=record.get("video_url")
            )
            # If common name was slightly different, prefer database's curated common name if available
            if record.get("common_name") and not detection.common_name:
                detection.common_name = record["common_name"]
        else:
            # Fallback when plant is identified by Gemini but not yet cataloged in MongoDB
            logger.info(f"Plant '{detection.scientific_name}' identified but not found in MongoDB dataset.")
            display_name = f"{detection.common_name} ({detection.scientific_name})" if detection.common_name else detection.scientific_name
            detection.ayurvedic_info = AyurvedicInfo(
                category="Botanical",
                ayurvedic_name=None,
                family=None,
                description=f"Identified as {display_name}. Curated botanical documentation is currently being compiled for this species.",
                ayurvedic_uses=["Botanical identity established; traditional uses awaiting entry into catalog."],
                traditional_uses=[],
                plant_parts_used=[],
                precautions=["Do not consume or apply wild plants without verification by a botanist or clinician."],
                warnings=["Always consult a healthcare provider before using unfamiliar plants for health purposes."],
                image_url=None,
                video_url=f"https://www.youtube.com/results?search_query={detection.scientific_name.replace(' ', '+')}"
            )

        return detection

    def get_by_scientific_name(self, scientific_name: str) -> Optional[PlantDatabaseRecord]:
        doc = db_manager.find_by_scientific_name(scientific_name)
        if not doc:
            return None
        return PlantDatabaseRecord(**doc)

    def search_plants(self, query: str, limit: int = 30) -> List[PlantDatabaseRecord]:
        docs = db_manager.search_plants(query, limit=limit)
        return [PlantDatabaseRecord(**d) for d in docs]

    def get_all_plants(self, skip: int = 0, limit: int = 100) -> List[PlantDatabaseRecord]:
        docs = db_manager.get_all_plants(skip=skip, limit=limit)
        return [PlantDatabaseRecord(**d) for d in docs]

plant_service = PlantService()
