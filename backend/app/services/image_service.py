"""
Image Processing Service for AyurScan.
Validates MIME types, ensures file size boundaries, and optimizes image dimensions
for Google Gemini Vision processing.
Designed with a modular architecture so future object detection (e.g., YOLO)
can be plugged into the pipeline without altering the core identification flow.
"""

import io
import logging
from typing import Tuple, List, Optional
from PIL import Image, ImageOps

logger = logging.getLogger("ayurscan.image")

ALLOWED_MIME_TYPES = {
    "image/jpeg": "JPEG",
    "image/jpg": "JPEG",
    "image/png": "PNG",
    "image/webp": "WEBP",
}

MAX_FILE_SIZE_BYTES = 15 * 1024 * 1024  # 15 MB
MAX_IMAGE_DIMENSION = 1600               # Max width or height for AI vision processing
TARGET_JPEG_QUALITY = 85

class ImageValidationError(Exception):
    """Raised when an uploaded file fails format or integrity validation."""
    pass

class ImageService:
    @staticmethod
    def validate_and_optimize(
        file_bytes: bytes,
        declared_mime_type: Optional[str] = None
    ) -> Tuple[bytes, str]:
        """
        Validates the incoming image bytes, normalizes orientation,
        downscales if larger than MAX_IMAGE_DIMENSION, and returns optimized JPEG bytes.
        """
        if not file_bytes:
            raise ImageValidationError("Empty image payload received. Please provide a valid plant image.")

        if len(file_bytes) > MAX_FILE_SIZE_BYTES:
            raise ImageValidationError(
                f"Image file size ({len(file_bytes) / (1024 * 1024):.1f} MB) exceeds maximum allowed limit (15 MB)."
            )

        try:
            image = Image.open(io.BytesIO(file_bytes))
            image.verify()  # Verify header and integrity
            # Reopen because verify() closes/invalidates the image stream
            image = Image.open(io.BytesIO(file_bytes))
        except Exception as e:
            raise ImageValidationError(f"Invalid or corrupted image file. Please upload a clear photo. Details: {e}")

        # Normalize EXIF orientation (handles mobile phone camera rotations)
        try:
            image = ImageOps.exif_transpose(image)
        except Exception:
            pass

        # Convert palette/transparency to RGB for consistent model processing
        if image.mode in ("RGBA", "LA", "P"):
            rgb_image = Image.new("RGB", image.size, (255, 255, 255))
            if image.mode == "P":
                image = image.convert("RGBA")
            rgb_image.paste(image, mask=image.split()[-1] if image.mode == "RGBA" else None)
            image = rgb_image
        elif image.mode != "RGB":
            image = image.convert("RGB")

        # Resize if dimensions exceed threshold
        width, height = image.size
        max_dim = max(width, height)
        if max_dim > MAX_IMAGE_DIMENSION:
            scale = MAX_IMAGE_DIMENSION / max_dim
            new_width = int(width * scale)
            new_height = int(height * scale)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            logger.info(f"Resized image from {width}x{height} to {new_width}x{new_height}")

        # Compress to optimized JPEG
        output_buffer = io.BytesIO()
        image.save(output_buffer, format="JPEG", quality=TARGET_JPEG_QUALITY, optimize=True)
        optimized_bytes = output_buffer.getvalue()

        return optimized_bytes, "image/jpeg"

    # =========================================================================
    # Modular Future Extension Point: YOLO / Object Detection
    # =========================================================================
    @staticmethod
    def extract_plant_crops_for_future_yolo(
        image_bytes: bytes,
        bounding_boxes: Optional[List[dict]] = None
    ) -> List[bytes]:
        """
        Architecture placeholder for Phase 2:
        When a YOLO/object detector is introduced, it will identify individual
        plant bounding boxes and pass them here to produce cropped images
        for separate Gemini identification passes.
        Currently returns the full image as a single item list.
        """
        if not bounding_boxes:
            return [image_bytes]

        crops = []
        try:
            image = Image.open(io.BytesIO(image_bytes))
            for box in bounding_boxes:
                # box expected format: {"xmin": int, "ymin": int, "xmax": int, "ymax": int}
                crop = image.crop((box["xmin"], box["ymin"], box["xmax"], box["ymax"]))
                buf = io.BytesIO()
                crop.save(buf, format="JPEG", quality=TARGET_JPEG_QUALITY)
                crops.append(buf.getvalue())
        except Exception as e:
            logger.warning(f"Error extracting bounding crops: {e}, falling back to full image.")
            return [image_bytes]

        return crops

image_service = ImageService()
