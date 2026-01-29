from enum import Enum
from typing import List
from pydantic import BaseModel, Field, field_validator

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

    @field_validator('content')
    @classmethod
    def validate_content_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
             raise ValueError('Content cannot be empty/blank')
        return v

class ScanResult(BaseModel):
    risk_score: int = Field(..., ge=0, le=100, description="Integer score between 0 and 100 indicating risk level")
    risk_level: RiskLevel
    findings: List[str] = Field(default_factory=list, description="List of technical findings justifying the score")
