import re
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class IAnalysisStrategy(ABC):
    """
    Interface for text analysis strategies (Strategy Pattern).
    """
    @abstractmethod
    def analyze(self, text: str) -> float:
        """
        Analyzes the text and returns a threat probability (0.0 to 1.0).
        """
        pass

    @abstractmethod
    def get_findings(self) -> List[str]:
        """
        Returns a list of specific findings from the last analysis.
        """
        pass

class UrgencyDetectionStrategy(IAnalysisStrategy):
    """
    Detects urgency or fear-inducing language.
    """
    def __init__(self):
        self.findings = []
        # Keywords indicating urgency or fear using word boundaries
        self.keywords = [
            r"\burgente\b", r"\binmediato\b", r"\bacción requerida\b", r"\bbloqueo\b", r"\bsuspendida\b",
            r"\bcancelación\b", r"\bahora\b", r"\bya\b", r"\blímite\b", r"\badvertencia\b"
        ]

    def analyze(self, text: str) -> float:
        self.findings = []
        if not text: return 0.0
        
        score = 0.0
        lower_text = text.lower()
        
        match_count = 0
        for pattern in self.keywords:
            if re.search(pattern, lower_text):
                # Clean pattern for display
                display_pattern = pattern.replace(r"\b", "")
                self.findings.append(f"Detected urgency keyword: '{display_pattern}'")
                match_count += 1
        
        # Simple scoring logic: more matches = higher score, capped at 1.0
        if match_count > 0:
            score = 0.5 + (match_count * 0.1)
        
        return min(score, 1.0)

    def get_findings(self) -> List[str]:
        return self.findings

class AuthorityImpersonationStrategy(IAnalysisStrategy):
    """
    Detects attempts to impersonate authority figures or departments.
    """
    def __init__(self):
        self.findings = []
        # Roles with word boundaries
        self.roles = [
            r"\bceo\b", r"\bdirector\b", r"\bgerente\b", r"\brrhh\b", r"\brecursos humanos\b",
            r"\bdepartamento de ti\b", r"\bseguridad\b", r"\bbanco\b", r"\bsoporte técnico\b",
            r"\badministrador\b"
        ]
        self.demands = [
            r"\benvía\b", r"\btransfiere\b", r"\bcontraseña\b", r"\bacceso\b", r"\bpago\b", r"\bfactura\b"
        ]

    def analyze(self, text: str) -> float:
        self.findings = []
        if not text: return 0.0

        score = 0.0
        lower_text = text.lower()
        
        has_role = False
        for role in self.roles:
            if re.search(role, lower_text):
                has_role = True
                display_role = role.replace(r"\b", "")
                self.findings.append(f"Detected authority role claim: '{display_role}'")
                break
        
        has_demand = False
        for demand in self.demands:
            if re.search(demand, lower_text):
                has_demand = True
                display_demand = demand.replace(r"\b", "")
                self.findings.append(f"Detected demand language: '{display_demand}'")
                break

        if has_role:
            score += 0.4
            if has_demand:
                score += 0.5 # High risk if pretending to be authority AND demanding something
        
        return min(score, 1.0)

    def get_findings(self) -> List[str]:
        return self.findings

class MaliciousLinkStrategy(IAnalysisStrategy):
    """
    Detects and analyzes URLs within the text.
    """
    def __init__(self):
        self.findings = []
        # Simple regex for URL extraction
        self.url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

    def analyze(self, text: str) -> float:
        self.findings = []
        if not text: return 0.0

        urls = re.findall(self.url_pattern, text)
        
        if not urls:
            return 0.0
            
        score = 0.0
        for url in urls:
            self.findings.append(f"Found URL: {url}")
            # Heuristic checks
            if "@" in url:
                self.findings.append(f"Suspicious URL structure (contains '@'): {url}")
                score += 0.8
            elif text.count('.') > 3 and "domain" not in url: # Crude check for obsession
                self.findings.append(f"Potential complex/obfuscated URL: {url}")
                score += 0.4
            else:
                 self.findings.append(f"URL present, checking reputation (simulated): {url}")
                 score += 0.1 # Base risk just for having a link in this context
                 
        return min(score, 1.0)

    def get_findings(self) -> List[str]:
        return self.findings

class SocialEngineeringScanner:
    """
    Context class that uses multiple strategies to scan text.
    """
    def __init__(self, strategies: List[IAnalysisStrategy]):
        self.strategies = strategies

    def scan_text(self, text: str) -> Dict[str, Any]:
        # Robustness: Handle non-string or empty input safely
        if not text or not isinstance(text, str):
            return {
                "risk_score": 0.0,
                "risk_level": "LOW",
                "findings": []
            }

        total_risk = 0.0
        all_findings = []
        
        for strategy in self.strategies:
            risk = strategy.analyze(text)
            findings = strategy.get_findings()
            
            if risk > 0:
                # Accumulate risk but perhaps use a weighted approach or max
                # For now using logic: sum of risks, capped at 1.0
                total_risk += risk
                all_findings.extend(findings)
        
        final_risk = min(total_risk, 1.0)
        
        return {
            "risk_score": final_risk,
            "risk_level": self._get_risk_level(final_risk),
            "findings": all_findings
        }

    def _get_risk_level(self, score: float) -> str:
        if score > 0.7:
            return "CRITICAL"
        elif score > 0.4:
            return "HIGH"
        elif score > 0.1:
            return "MEDIUM"
        return "LOW"
