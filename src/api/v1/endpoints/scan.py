from functools import lru_cache
from fastapi import APIRouter, Depends
from src.domain.schemas import ScanRequest, ScanResult
from src.services.orchestrator import AnalysisOrchestrator
from src.services.analysis_engines.url_engine import UrlAnalysisEngine
from src.services.analysis_engines.text_analysis import TextAnalysisEngine

router = APIRouter()

@lru_cache()
def get_orchestrator() -> AnalysisOrchestrator:
    # Factory for engines - in a real app this might be more complex or use a DI framework
    engines = [
        UrlAnalysisEngine(),
        TextAnalysisEngine()
    ]
    return AnalysisOrchestrator(engines=engines)

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
