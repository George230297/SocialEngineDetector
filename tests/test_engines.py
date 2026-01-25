import pytest
from src.domain.schemas import ScanRequest, ArtifactType, RiskLevel
from src.services.analysis_engines.url_engine import UrlAnalysisEngine

@pytest.mark.asyncio
async def test_url_engine_supports():
    engine = UrlAnalysisEngine()
    assert engine.supports(ArtifactType.URL)
    assert not engine.supports(ArtifactType.TEXT)

@pytest.mark.asyncio
async def test_url_engine_scan_safe():
    engine = UrlAnalysisEngine()
    request = ScanRequest(artifact_type=ArtifactType.URL, content="https://example.com")
    result = await engine.scan(request)
    assert result.risk_level == RiskLevel.SAFE
    assert result.risk_score == 0

@pytest.mark.asyncio
async def test_url_engine_scan_ip_address():
    engine = UrlAnalysisEngine()
    request = ScanRequest(artifact_type=ArtifactType.URL, content="http://192.168.1.1/login")
    result = await engine.scan(request)
    assert result.risk_score >= 50
    assert any("URL uses an IP address" in finding for finding in result.findings)
