"""
Comprehensive Test Suite for AyurScan Full-Stack Backend.
Covers:
- Database lookup, fallback, indexing, and search
- Image validation and optimization
- Multiple-plant identification logic
- Confidence threshold application (Section 6)
- Unclear plant handling without hallucinations (Section 7, 27)
- Plant not in database graceful enrichment
- API endpoint integration
"""

import io
import unittest
from unittest.mock import patch, MagicMock
from PIL import Image

from fastapi.testclient import TestClient
from app.main import app
from app.database.mongodb import db_manager
from app.services.image_service import image_service, ImageValidationError
from app.services.gemini_service import gemini_service, GeminiRawPlantItem, GeminiConfigError, GeminiRateLimitError
from app.services.plant_service import plant_service
from app.models.plant import PlantDetectionResult

class TestDatabaseAndCatalog(unittest.TestCase):
    def test_catalog_loaded_fallback(self):
        """Verify the 70 plants fallback dataset is properly loaded in database manager."""
        self.assertGreaterEqual(len(db_manager._fallback_plants), 50)

    def test_find_by_scientific_name_exact(self):
        """Verify exact botanical name matching for Tulsi."""
        plant = db_manager.find_by_scientific_name("Ocimum tenuiflorum")
        self.assertIsNotNone(plant)
        self.assertIn("Tulsi", plant["common_name"])
        self.assertEqual(plant["ayurvedic_name"], "Tulasi")

    def test_find_by_scientific_name_case_insensitive(self):
        """Verify case-insensitive lookup."""
        plant = db_manager.find_by_scientific_name("ocimum tenuiflorum")
        self.assertIsNotNone(plant)
        self.assertEqual(plant["scientific_name"], "Ocimum tenuiflorum")

    def test_find_by_scientific_name_neem(self):
        """Verify Neem lookup."""
        plant = db_manager.find_by_scientific_name("Azadirachta indica")
        self.assertIsNotNone(plant)
        self.assertEqual(plant["ayurvedic_name"], "Nimba")

    def test_search_by_common_name(self):
        """Verify searching by common name 'Turmeric'."""
        results = db_manager.search_plants("Turmeric")
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]["scientific_name"], "Curcuma longa")

    def test_search_by_ayurvedic_name(self):
        """Verify searching by Ayurvedic name 'Ashwagandha'."""
        results = db_manager.search_plants("Ashwagandha")
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]["scientific_name"], "Withania somnifera")

    def test_search_by_scientific_name(self):
        """Verify searching by botanical name fragment 'Zingiber'."""
        results = db_manager.search_plants("Zingiber")
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]["scientific_name"], "Zingiber officinale")


class TestImageProcessing(unittest.TestCase):
    def _create_sample_image(self, width=800, height=600, color="green"):
        img = Image.new("RGB", (width, height), color=color)
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        return buf.getvalue()

    def test_valid_image_processing(self):
        raw_bytes = self._create_sample_image(800, 600)
        optimized, mime = image_service.validate_and_optimize(raw_bytes)
        self.assertEqual(mime, "image/jpeg")
        self.assertTrue(len(optimized) > 0)

    def test_large_image_downscaling(self):
        # 3000x2000 image should be scaled down to max dimension <= 1600
        large_bytes = self._create_sample_image(3000, 2000)
        optimized, _ = image_service.validate_and_optimize(large_bytes)
        out_img = Image.open(io.BytesIO(optimized))
        self.assertLessEqual(max(out_img.size), 1600)

    def test_invalid_image_fails_validation(self):
        bad_bytes = b"NOT_A_REAL_IMAGE_BYTES"
        with self.assertRaises(ImageValidationError):
            image_service.validate_and_optimize(bad_bytes)

    def test_empty_image_fails_validation(self):
        with self.assertRaises(ImageValidationError):
            image_service.validate_and_optimize(b"")

    def test_future_yolo_crops_interface(self):
        raw_bytes = self._create_sample_image(400, 400)
        # Without bounding boxes, returns full image
        crops = image_service.extract_plant_crops_for_future_yolo(raw_bytes)
        self.assertEqual(len(crops), 1)

        # With mock bounding box, returns crop
        boxes = [{"xmin": 10, "ymin": 10, "xmax": 100, "ymax": 100}]
        crops_with_boxes = image_service.extract_plant_crops_for_future_yolo(raw_bytes, boxes)
        self.assertEqual(len(crops_with_boxes), 1)


class TestGeminiMultiPlantLogic(unittest.TestCase):
    def test_confidence_threshold_separation(self):
        """
        Critical Test from Section 6 & 27:
        Upload image containing 3 Ayurvedic plants where 2 are clearly visible
        and 1 is partially hidden/blurry.
        Expected:
        Plant 1 -> identified
        Plant 2 -> identified
        Plant 3 -> unclear (NOT invented or hallucinated)
        """
        raw_plants = [
            GeminiRawPlantItem(
                common_name="Tulsi",
                scientific_name="Ocimum tenuiflorum",
                confidence=0.94,
                status="identified",
                approximate_location="Foreground center"
            ),
            GeminiRawPlantItem(
                common_name="Neem",
                scientific_name="Azadirachta indica",
                confidence=0.91,
                status="identified",
                approximate_location="Left branch"
            ),
            GeminiRawPlantItem(
                common_name="Hibiscus",
                scientific_name="Hibiscus rosa-sinensis",
                confidence=0.35,  # Below 0.70 threshold
                status="unclear",
                approximate_location="Background upper right",
                reason="Plant is partially hidden and blurry, lacking floral structures."
            )
        ]

        results = gemini_service._process_detections(raw_plants)
        self.assertEqual(len(results), 3)

        # Plant 1: Clear Tulsi
        self.assertEqual(results[0].status, "identified")
        self.assertEqual(results[0].scientific_name, "Ocimum tenuiflorum")
        self.assertEqual(results[0].confidence, 0.94)

        # Plant 2: Clear Neem
        self.assertEqual(results[1].status, "identified")
        self.assertEqual(results[1].scientific_name, "Azadirachta indica")
        self.assertEqual(results[1].confidence, 0.91)

        # Plant 3: Must be marked unclear and NOT guess
        self.assertEqual(results[2].status, "unclear")
        self.assertIsNone(results[2].scientific_name)
        self.assertIsNone(results[2].common_name)
        self.assertIn("partially hidden", results[2].reason.lower())

    def test_enrichment_with_mongodb(self):
        """Verify plant service enriches detection with authentic Ayurvedic properties."""
        det = PlantDetectionResult(
            common_name="Tulsi",
            scientific_name="Ocimum tenuiflorum",
            confidence=0.95,
            status="identified"
        )
        enriched = plant_service.enrich_detection(det)
        self.assertIsNotNone(enriched.ayurvedic_info)
        self.assertEqual(enriched.ayurvedic_info.ayurvedic_name, "Tulasi")
        self.assertTrue(len(enriched.ayurvedic_info.ayurvedic_uses) > 0)
        self.assertTrue(len(enriched.ayurvedic_info.precautions) > 0)

    def test_plant_not_in_database_graceful(self):
        """Plant identified by AI but not in database does not crash and provides graceful message."""
        det = PlantDetectionResult(
            common_name="Exotic Rare Fern",
            scientific_name="Polypodium vulgare",
            confidence=0.88,
            status="identified"
        )
        enriched = plant_service.enrich_detection(det)
        self.assertIsNotNone(enriched.ayurvedic_info)
        self.assertIn("Polypodium vulgare", enriched.ayurvedic_info.description)


class TestApiEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_endpoint(self):
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["service"], "AyurScan")
        self.assertIn("confidence_threshold", data)

    def test_get_plants_pagination(self):
        res = self.client.get("/api/plants?skip=0&limit=5")
        self.assertEqual(res.status_code, 200)
        plants = res.json()
        self.assertEqual(len(plants), 5)
        self.assertIn("scientific_name", plants[0])

    def test_get_single_plant_found(self):
        res = self.client.get("/api/plants/Withania%20somnifera")
        self.assertEqual(res.status_code, 200)
        plant = res.json()
        self.assertEqual(plant["scientific_name"], "Withania somnifera")
        self.assertEqual(plant["ayurvedic_name"], "Ashwagandha")
        self.assertEqual(plant["category"], "Ayurvedic")

    def test_get_single_plant_not_found(self):
        res = self.client.get("/api/plants/Fictional%20botanical%20plant")
        self.assertEqual(res.status_code, 404)

    def test_search_endpoint(self):
        res = self.client.get("/api/search?q=neem")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["query"], "neem")
        self.assertGreaterEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["scientific_name"], "Azadirachta indica")

    def test_identify_empty_upload_fails(self):
        res = self.client.post("/api/identify", files={})
        self.assertIn(res.status_code, [400, 422])

    def test_identify_endpoint_multi_plant_mock(self):
        """End-to-end multi-plant identification test using mock Gemini service response."""
        mock_detections = [
            PlantDetectionResult(
                common_name="Tulsi (Holy Basil)",
                scientific_name="Ocimum tenuiflorum",
                confidence=0.96,
                status="identified",
                approximate_location="Center Foreground"
            ),
            PlantDetectionResult(
                common_name="Neem",
                scientific_name="Azadirachta indica",
                confidence=0.92,
                status="identified",
                approximate_location="Upper Left"
            ),
            PlantDetectionResult(
                common_name=None,
                scientific_name=None,
                confidence=0.30,
                status="unclear",
                reason="Plant is partially hidden and not sufficiently visible."
            )
        ]

        img = Image.new("RGB", (400, 300), color="green")
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        image_bytes = buf.getvalue()

        with patch.object(gemini_service, "analyze_image", return_value=mock_detections):
            res = self.client.post(
                "/api/identify",
                files={"image": ("test.jpg", image_bytes, "image/jpeg")}
            )
            self.assertEqual(res.status_code, 200)
            data = res.json()

            self.assertEqual(data["total_detected"], 3)
            self.assertEqual(data["identified_count"], 2)
            self.assertEqual(data["unclear_count"], 1)
            self.assertEqual(len(data["plants"]), 3)

            # Check Tulsi
            tulsi = data["plants"][0]
            self.assertEqual(tulsi["common_name"], "Tulsi (Holy Basil)")
            self.assertEqual(tulsi["status"], "identified")
            self.assertEqual(tulsi["ayurvedic_info"]["ayurvedic_name"], "Tulasi")

            # Check Neem
            neem = data["plants"][1]
            self.assertEqual(neem["common_name"], "Neem")
            self.assertEqual(neem["status"], "identified")
            self.assertEqual(neem["ayurvedic_info"]["ayurvedic_name"], "Nimba")

            # Check Unclear plant
            unclear = data["plants"][2]
            self.assertEqual(unclear["status"], "unclear")
            self.assertIsNone(unclear["scientific_name"])
            self.assertIn("partially hidden", unclear["reason"])

if __name__ == "__main__":
    unittest.main()
