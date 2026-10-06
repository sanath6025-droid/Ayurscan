from typing import List, Optional
from pydantic import BaseModel, Field

class AyurvedicInfo(BaseModel):
    category: Optional[str] = None
    ayurvedic_name: Optional[str] = None
    family: Optional[str] = None
    description: Optional[str] = None
    ayurvedic_uses: List[str] = Field(default_factory=list)
    traditional_uses: List[str] = Field(default_factory=list)
    plant_parts_used: List[str] = Field(default_factory=list)
    precautions: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    image_url: Optional[str] = None
    video_url: Optional[str] = None

class PlantDatabaseRecord(BaseModel):
    common_name: str
    scientific_name: str
    category: Optional[str] = None
    ayurvedic_name: Optional[str] = None
    family: Optional[str] = None
    description: Optional[str] = None
    ayurvedic_uses: List[str] = Field(default_factory=list)
    traditional_uses: List[str] = Field(default_factory=list)
    plant_parts_used: List[str] = Field(default_factory=list)
    precautions: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    image_url: Optional[str] = None
    video_url: Optional[str] = None

class GeminiRawPlantItem(BaseModel):
    common_name: Optional[str] = Field(None, description="Most likely common name of the plant")
    scientific_name: Optional[str] = Field(None, description="Botanical scientific binomial name (e.g. Ocimum tenuiflorum)")
    confidence: float = Field(..., description="Estimated identification confidence score between 0.0 and 1.0")
    status: str = Field(..., description="'identified' if plant is clearly visible and recognized, 'unclear' if blurry, partially hidden, or uncertain")
    approximate_location: Optional[str] = Field(None, description="Visual location in image, e.g. 'center', 'top-left foreground', 'background right'")
    reason: Optional[str] = Field(None, description="Reason if unclear, e.g. 'Partially obscured behind another leaf and lacking visible flowers'")

class GeminiRawResponse(BaseModel):
    plants: List[GeminiRawPlantItem] = Field(default_factory=list, description="List of visually distinguishable plants found across the entire image")

class PlantDetectionResult(BaseModel):
    common_name: Optional[str] = None
    scientific_name: Optional[str] = None
    confidence: float
    status: str  # "identified" or "unclear"
    approximate_location: Optional[str] = None
    reason: Optional[str] = None
    message: Optional[str] = None
    ayurvedic_info: Optional[AyurvedicInfo] = None

class IdentifyResponse(BaseModel):
    total_detected: int
    identified_count: int
    unclear_count: int
    plants: List[PlantDetectionResult]
    disclaimer: str = "This information is provided for educational purposes and describes traditional/Ayurvedic uses. It is not medical advice and should not be used as a substitute for professional medical care."

class SearchResponse(BaseModel):
    query: str
    count: int
    results: List[PlantDatabaseRecord]
