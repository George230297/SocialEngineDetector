import re
import unicodedata
from difflib import SequenceMatcher
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.services.analysis_engines.base import AnalysisEngine
from src.domain.schemas import ArtifactType, ScanRequest, ScanResult

def normalize_text(text: str) -> str:
    """Removes invisible characters, normalizes unicode, and standardizes spacing."""
    if not text: return ""
    # Normalize unicode (e.g., standardizes visually similar characters)
    text = unicodedata.normalize('NFKC', text)
    # Remove non-printable characters and zero-width spaces
    text = re.sub(r'[\u200b-\u200f\u202a-\u202e\ufeff]', '', text)
    # Replace any punctuation with space for semantic matching
    text = re.sub(r'[^\w\s]', ' ', text)
    # Standardize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower()

def is_fuzzy_match(word: str, target: str, threshold: float = 0.8) -> bool:
    # Use simple SequenceMatcher for fuzzy comparison
    ratio = SequenceMatcher(None, word, target).ratio()
    return ratio >= threshold

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
        # Keywords indicating urgency or fear
        self.targets = [
            "urgente", "inmediato", "accion", "requerida", "bloqueo", "suspendida",
            "cancelacion", "ahora", "limite", "advertencia"
        ]

    def analyze(self, text: str) -> float:
        self.findings = []
        if not text: return 0.0
        
        score = 0.0
        normalized = normalize_text(text)
        words = normalized.split()
        
        match_count = 0
        for target in self.targets:
            # Check for exact matches or fuzzy matches to handle slight obfuscations/typos
            for word in words:
                 if is_fuzzy_match(word, target, 0.85):
                     self.findings.append(f"Detected potential urgency term: '{target}' (matched '{word}')")
                     match_count += 1
                     break
        
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
        self.roles = [
            "ceo", "director", "gerente", "rrhh", "recursos", "humanos",
            "departamento", "seguridad", "banco", "soporte", "tecnico", "administrador"
        ]
        self.demands = [
            "envia", "transfiere", "contrasena", "acceso", "pago", "factura", "verificar"
        ]

    def analyze(self, text: str) -> float:
        self.findings = []
        if not text: return 0.0

        score = 0.0
        normalized = normalize_text(text)
        words = normalized.split()
        
        has_role = False
        for role in self.roles:
            for word in words:
                if is_fuzzy_match(word, role, 0.85):
                    has_role = True
                    self.findings.append(f"Detected authority role claim: related to '{role}'")
                    break
            if has_role: break
        
        has_demand = False
        for demand in self.demands:
            for word in words:
                if is_fuzzy_match(word, demand, 0.85):
                    has_demand = True
                    self.findings.append(f"Detected demand language: related to '{demand}'")
                    break
            if has_demand: break

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
            elif url.count('.') > 3 and "domain" not in url: # Crude check for obfuscation/subdomains
                self.findings.append(f"Potential complex/obfuscated URL: {url}")
                score += 0.4
            else:
                 self.findings.append(f"URL present, checking reputation (simulated): {url}")
                 score += 0.1 # Base risk just for having a link in this context
                 
        return min(score, 1.0)

    def get_findings(self) -> List[str]:
        return self.findings

class ObfuscationDetectionStrategy(IAnalysisStrategy):
    """
    Detects structural anomalies in the text like excessive invisible characters or irregular spacing.
    """
    def __init__(self):
        self.findings = []
    
    def analyze(self, text: str) -> float:
        self.findings = []
        if not text: return 0.0
        
        score = 0.0
        
        # Check for zero-width characters
        zw_chars = re.findall(r'[\u200b-\u200f\u202a-\u202e\ufeff]', text)
        if zw_chars:
            self.findings.append(f"Detected {len(zw_chars)} hidden/zero-width formatting characters.")
            score += 0.4
            
        # Check for excessive spacing between letters (e.g., "u r g e n t e")
        if re.search(r'([a-zA-Z]\s){4,}[a-zA-Z]', text):
            self.findings.append("Detected irregular spacing indicative of filter evasion.")
            score += 0.3
            
        # Check for mixed alphabets (e.g. Cyrillic and Latin) in standard words
        if re.search(r'[a-zA-Z][\u0400-\u04FF]|[a-zA-Z][\u0370-\u03FF]|[\u0400-\u04FF][a-zA-Z]|[\u0370-\u03FF][a-zA-Z]', text):
             self.findings.append("Detected mixed character sets (homoglyph attack likely).")
             score += 0.6
             
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

class TextAnalysisEngine(AnalysisEngine):
    """
    Adapter for SocialEngineeringScanner to fit into AnalysisOrchestrator.
    """
    def __init__(self):
        strategies = [
            UrgencyDetectionStrategy(),
            AuthorityImpersonationStrategy(),
            MaliciousLinkStrategy(),
            ObfuscationDetectionStrategy()
        ]
        self.scanner = SocialEngineeringScanner(strategies)

    def supports(self, artifact_type: ArtifactType) -> bool:
        return artifact_type == ArtifactType.TEXT

    async def scan(self, request: ScanRequest) -> ScanResult:
        # validacion de seguridad adicional
        if request.artifact_type != ArtifactType.TEXT:
             raise ValueError("Unsupported artifact type for TextAnalysisEngine")

        report = self.scanner.scan_text(request.content)
        
        # Map internal risk definition to Schema RiskLevel
        internal_level = report["risk_level"]
        if internal_level == "LOW":
            schema_level = "SAFE"
        elif internal_level == "MEDIUM":
             schema_level = "SUSPICIOUS"
        else: # HIGH, CRITICAL
             schema_level = "MALICIOUS"

        return ScanResult(
            risk_score=int(report["risk_score"] * 100), # Convert 0.0-1.0 to 0-100
            risk_level=schema_level,
            findings=report["findings"]
        )

