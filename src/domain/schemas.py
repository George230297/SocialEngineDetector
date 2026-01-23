from enum import Enum
from typing import List
from pydantic import BaseModel, Field

class ArtifactType(str, Enum):
    URL = "URL"
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    AUDIO = "AUDIO"

class RiskLevel(str, Enum):
    SAFE = "SAFE"
    SUSPICIOUS = "SUSPICIOUS"
    MALICIOUS = "MALICIOUS"

class ScanRequest(BaseModel):
    artifact_type: ArtifactType
    content: str = Field(..., description="The content to analyze (e.g., URL string, text message, base64 data)")

class ScanResult(BaseModel):
    risk_score: int = Field(..., ge=0, le=100, description="Integer score between 0 and 100 indicating risk level")
    risk_level: RiskLevel
    findings: List[str] = Field(default_factory=list, description="List of technical findings justifying the score")
