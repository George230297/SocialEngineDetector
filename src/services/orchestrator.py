from typing import List
from fastapi import HTTPException
from src.domain.schemas import ScanRequest, ScanResult
from src.services.analysis_engines.base import AnalysisEngine
from src.services.analysis_engines.url_engine import UrlAnalysisEngine

class AnalysisOrchestrator:
    def __init__(self):
        self.engines: List[AnalysisEngine] = [
            UrlAnalysisEngine()
        ]

    async def analyze_artifact(self, request: ScanRequest) -> ScanResult:
        for engine in self.engines:
            if engine.supports(request.artifact_type):
                return await engine.scan(request)
        
        raise HTTPException(
            status_code=400,
            detail=f"No analysis engine found for artifact type: {request.artifact_type}"
        )
