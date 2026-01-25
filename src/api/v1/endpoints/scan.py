from functools import lru_cache
from fastapi import APIRouter, Depends
from src.domain.schemas import ScanRequest, ScanResult
from src.services.orchestrator import AnalysisOrchestrator

router = APIRouter()

@lru_cache()
def get_orchestrator() -> AnalysisOrchestrator:
    return AnalysisOrchestrator()

@router.post(
    "/analyze",
    response_model=ScanResult,
    summary="Analyze an artifact",
    description="Analyzes the provided artifact (URL, text, etc.) using available analysis engines to detect potential social engineering threats."
)
async def analyze_artifact(
    request: ScanRequest,
    orchestrator: AnalysisOrchestrator = Depends(get_orchestrator)
) -> ScanResult:
    return await orchestrator.analyze_artifact(request)
