import re
from src.domain.schemas import ArtifactType, ScanRequest, ScanResult, RiskLevel
from src.services.analysis_engines.base import AnalysisEngine

class UrlAnalysisEngine(AnalysisEngine):
    """
    Concrete implementation of AnalysisEngine for URLs using basic heuristics.
    """

    def supports(self, artifact_type: ArtifactType) -> bool:
        return artifact_type == ArtifactType.URL

    async def scan(self, request: ScanRequest) -> ScanResult:
        url = request.content
        risk_score = 0
        findings = []

        # Heuristic 1: URL Length > 80
        if len(url) > 80:
            risk_score += 20
            findings.append("URL length exceeds 80 characters")

        # Heuristic 2: Suspicious keywords
        suspicious_keywords = ["login", "update", "verify"]
        found_keywords = [kw for kw in suspicious_keywords if kw in url.lower()]
        if found_keywords:
            risk_score += 30
            findings.append(f"Suspicious keywords found: {', '.join(found_keywords)}")

        # Heuristic 3: IP address usage
        # Simple regex for IPv4
        ip_pattern = r"^(?:http:\/\/|https:\/\/)?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
        if re.match(ip_pattern, url):
            risk_score += 50
            findings.append("URL uses an IP address instead of a domain name")

        # Cap score at 100
        risk_score = min(risk_score, 100)

        # Determine Risk Level
        if risk_score == 0:
            risk_level = RiskLevel.SAFE
        elif risk_score < 60:
            risk_level = RiskLevel.SUSPICIOUS
        else:
            risk_level = RiskLevel.MALICIOUS

        return ScanResult(
            risk_score=risk_score,
            risk_level=risk_level,
            findings=findings
        )
