import pytest
from src.services.analysis_engines.text_analysis import (
    SocialEngineeringScanner,
    UrgencyDetectionStrategy,
    AuthorityImpersonationStrategy,
    MaliciousLinkStrategy
)

@pytest.fixture
def scanner():
    strategies = [
        UrgencyDetectionStrategy(),
        AuthorityImpersonationStrategy(),
        MaliciousLinkStrategy()
    ]
    return SocialEngineeringScanner(strategies)

def test_urgency_strategy_basic():
    strategy = UrgencyDetectionStrategy()
    # "urgente" should trigger match
    score = strategy.analyze("Esto es muy urgente pro favor.")
    assert score > 0.0
    assert "urgente" in strategy.get_findings()[0]

def test_urgency_strategy_no_match():
    strategy = UrgencyDetectionStrategy()
    score = strategy.analyze("Hola, todo tranquilo.")
    assert score == 0.0
    assert len(strategy.get_findings()) == 0

def test_urgency_partial_match_ignored():
    strategy = UrgencyDetectionStrategy()
    # "insurgente" contains "urgente" but should be ignored due to \b
    score = strategy.analyze("El movimiento insurgente avanza.")
    assert score == 0.0

def test_urgency_strategy_accumulation_cap():
    strategy = UrgencyDetectionStrategy()
    # Multiple keywords: urgente, inmediato, ahora, ya
    text = "Urgente! Necesito esto inmediato ahora mismo ya."
    score = strategy.analyze(text)
    assert score <= 1.0
    assert score > 0.8 # Should be very high

def test_authority_impersonation_role_only():
    strategy = AuthorityImpersonationStrategy()
    score = strategy.analyze("Soy el CEO de la empresa.")
    assert score == 0.4
    
def test_authority_impersonation_role_and_demand():
    strategy = AuthorityImpersonationStrategy()
    score = strategy.analyze("Soy de RRHH y necesito que envíes tu contraseña.")
    assert score >= 0.9 # 0.4 + 0.5
    findings = strategy.get_findings()
    # Findings report the pattern found, which is 'rrhh' in the list (lowercase)
    assert any("rrhh" in f for f in findings)

def test_malicious_link_extraction():
    strategy = MaliciousLinkStrategy()
    text = "Visita http://evil.com para ganar premios."
    score = strategy.analyze(text)
    assert score > 0
    assert "http://evil.com" in strategy.get_findings()[0]

def test_malicious_link_obfuscation():
    strategy = MaliciousLinkStrategy()
    text = "http://bank.com@evil.com"
    score = strategy.analyze(text)
    assert score >= 0.8
    assert "Suspicious URL structure" in str(strategy.get_findings())

def test_scanner_integration(scanner):
    result = scanner.scan_text("Urgente: El CEO requiere su pago en http://scam.com")
    assert result['risk_level'] == "CRITICAL"
    assert result['risk_score'] > 0.8
    assert len(result['findings']) >= 3 # Urgency, Authority, Link

def test_scanner_empty_input(scanner):
    # Should handle empty strings gracefully
    result = scanner.scan_text("")
    assert result['risk_score'] == 0.0
    assert result['risk_level'] == "LOW"

def test_scanner_none_input(scanner):
    # Now it should return 0/SAFE instead of crashing
    result = scanner.scan_text(None)
    assert result['risk_score'] == 0.0
    assert result['risk_level'] == "LOW"

def test_case_insensitivity():
    strategy = UrgencyDetectionStrategy()
    score_upper = strategy.analyze("URGENTE")
    score_lower = strategy.analyze("urgente")
    assert score_upper == score_lower > 0
