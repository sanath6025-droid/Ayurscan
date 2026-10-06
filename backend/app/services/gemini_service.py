"""
Google Gemini Vision Service for AyurScan.
Uses the official google-genai SDK to analyze images for all visible plants.
Enforces structured JSON output, application-level confidence thresholding,
and robust error handling.
"""

import os
import json
import logging
from typing import List, Tuple, Optional
from pydantic import ValidationError

from google import genai
from google.genai import types
from google.genai.errors import APIError

from app.models.plant import (
    GeminiRawResponse,
    GeminiRawPlantItem,
    PlantDetectionResult
)

logger = logging.getLogger("ayurscan.gemini")

GEMINI_SYSTEM_PROMPT = """You are the plant identification vision system for AyurScan.

Analyze the entire uploaded image carefully.

Identify every visually distinguishable plant that is sufficiently visible.

Do not identify only the largest or most prominent plant.

Systematically inspect the complete image across the foreground, background, left, center, and right.

For each plant:
- provide the most likely common name
- provide the scientific name (botanical binomial nomenclature)
- provide an estimated confidence score from 0.0 to 1.0
- determine whether the plant is sufficiently visible
- mark unclear plants as status="unclear"
- do not guess when visual evidence is insufficient

If multiple plants are present, return every clearly distinguishable plant separately in the 'plants' list.

If plants overlap, are blurry, partially hidden, too small, or otherwise lack sufficient visual evidence, mark them with status="unclear", common_name=null, scientific_name=null, and provide a clear reason in 'reason'.

If no plants are present in the image, return an empty 'plants' list.

Do not invent plant identities.

Return ONLY valid JSON according to the required schema."""

class GeminiServiceError(Exception):
    """Base exception for Gemini service issues."""
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class GeminiConfigError(GeminiServiceError):
    def __init__(self, message: str = "Google Gemini API key is not configured. Please add GEMINI_API_KEY to your backend/.env file."):
        super().__init__(message, status_code=503)

class GeminiRateLimitError(GeminiServiceError):
    def __init__(self, message: str = "Too many requests right now. Please try again in a moment."):
        super().__init__(message, status_code=429)

class GeminiService:
    def __init__(self):
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.threshold = float(os.getenv("CONFIDENCE_THRESHOLD", "0.70"))
        self._client: Optional[genai.Client] = None

    def _get_client(self) -> genai.Client:
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key:
            raise GeminiConfigError()
        if self._client is None:
            self._client = genai.Client(api_key=api_key)
        return self._client

    def analyze_image(
        self,
        image_bytes: bytes,
        mime_type: str = "image/jpeg"
    ) -> List[PlantDetectionResult]:
        """
        Sends the image to Google Gemini Vision with structured schema output.
        Inspects the entire image and identifies all distinguishable plants.
        Applies application-level confidence threshold.
        """
        client = self._get_client()

        try:
            image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)

            config = types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=GeminiRawResponse,
                temperature=0.1,  # Low temperature for deterministic identification
                system_instruction=GEMINI_SYSTEM_PROMPT
            )

            candidate_models = [self.model_name]
            for fallback in ["gemini-3.5-flash-lite", "gemini-3.8-flash"]:
                if fallback not in candidate_models:
                    candidate_models.append(fallback)

            response = None
            last_err = None
            for model_to_use in candidate_models:
                try:
                    logger.info(f"Dispatching image analysis to Gemini model '{model_to_use}'...")
                    response = client.models.generate_content(
                        model=model_to_use,
                        contents=[image_part, "Analyze this entire image and identify all visible plants according to instructions."],
                        config=config
                    )
                    if response and response.text:
                        break
                except Exception as m_err:
                    last_err = m_err
                    logger.warning(f"Model '{model_to_use}' failed: {m_err}. Trying fallback...")
                    continue

            if response is None or not response.text:
                if last_err and isinstance(last_err, APIError):
                    raise last_err
                raise GeminiServiceError("Gemini returned an empty response. Please try another image.", 502)

            raw_text = response.text
            parsed_data = json.loads(raw_text)
            validated = GeminiRawResponse.model_validate(parsed_data)

            return self._process_detections(validated.plants)

        except APIError as api_err:
            err_msg = str(api_err).lower()
            logger.error(f"Gemini API Error: {api_err.code} - {api_err.message}")
            if "429" in str(api_err.code) or "quota" in err_msg or "resource_exhausted" in err_msg:
                raise GeminiRateLimitError()
            elif "400" in str(api_err.code) or "invalid" in err_msg:
                raise GeminiServiceError("The image format or request could not be processed by the vision service.", 400)
            else:
                raise GeminiServiceError("AI vision service is momentarily unavailable. Please try again in a few moments.", 502)

        except json.JSONDecodeError as jde:
            logger.error(f"Failed to parse Gemini structured JSON: {jde}")
            raise GeminiServiceError("Unable to parse identification results from AI vision service.", 502)

        except ValidationError as ve:
            logger.error(f"Validation error against GeminiRawResponse schema: {ve}")
            raise GeminiServiceError("AI vision service returned an unexpected structure.", 502)

        except (GeminiConfigError, GeminiRateLimitError):
            raise

        except Exception as ex:
            logger.error(f"Unexpected error during Gemini analysis: {type(ex).__name__}: {ex}")
            raise GeminiServiceError("Plant identification encountered an unexpected issue.", 500)

    def _process_detections(self, raw_plants: List[GeminiRawPlantItem]) -> List[PlantDetectionResult]:
        """
        Applies application-level confidence threshold (Section 6)
        and normalizes plant identification results.
        """
        processed_results: List[PlantDetectionResult] = []

        for item in raw_plants:
            confidence = round(float(item.confidence), 2)
            is_unclear = (
                confidence < self.threshold
                or item.status.lower() == "unclear"
                or not item.scientific_name
            )

            if is_unclear:
                reason = item.reason or "Plant could not be identified clearly. Please upload a clearer image or capture the plant separately."
                processed_results.append(
                    PlantDetectionResult(
                        common_name=None,
                        scientific_name=None,
                        confidence=confidence,
                        status="unclear",
                        approximate_location=item.approximate_location,
                        reason=reason,
                        message="Plant is not clearly visible. Please upload a clearer image or capture the plant separately."
                    )
                )
            else:
                processed_results.append(
                    PlantDetectionResult(
                        common_name=item.common_name or "Unknown Plant",
                        scientific_name=item.scientific_name.strip(),
                        confidence=confidence,
                        status="identified",
                        approximate_location=item.approximate_location,
                        reason=None,
                        message=None
                    )
                )

        return processed_results

gemini_service = GeminiService()
