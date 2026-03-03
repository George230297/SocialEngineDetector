import pytest
from src.services.analysis_engines.text_analysis import (
    SocialEngineeringScanner,
    UrgencyDetectionStrategy,
    AuthorityImpersonationStrategy,
    MaliciousLinkStrategy,
    ObfuscationDetectionStrategy
)

@pytest.fixture
def scanner():
    strategies = [
        UrgencyDetectionStrategy(),
        AuthorityImpersonationStrategy(),
        MaliciousLinkStrategy(),
        ObfuscationDetectionStrategy()
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
    # "insurgente" contains "urgente" but sequence matcher ratio is below threshold (0.82 < 0.85)
    score = strategy.analyze("El movimiento insurgente avanza.")
    assert score == 0.0

def test_fuzzy_match_obfuscation():
    strategy = UrgencyDetectionStrategy()
    # Simulate typo/obfuscation like "urg3nte"
    score = strategy.analyze("Esto es muy urg3nte.")
    assert score > 0.0
    assert "urgente" in strategy.get_findings()[0]
    
def test_authority_fuzzy_match():
    strategy = AuthorityImpersonationStrategy()
    # 6 matches out of 7 lengths = 12/14 = 0.857 >= 0.85 threshold
    score = strategy.analyze("Soy tu ger3nte no respondas.")
    assert score > 0.0
    assert "gerente" in strategy.get_findings()[0]

def test_urgency_strategy_accumulation_cap():
    strategy = UrgencyDetectionStrategy()
    # Multiple keywords: urgente, inmediato, ahora, ya (note: "ya" is not in the list, so 3 matches: urgente, inmediato, ahora)
    text = "Urgente! Necesito esto inmediato ahora mismo ya."
    score = strategy.analyze(text)
    assert score <= 1.0
    assert score >= 0.8 # 0.5 + 3 * 0.1 = 0.8

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
    assert any("contrasena" in f for f in findings)

def test_obfuscation_strategy_zero_width():
    strategy = ObfuscationDetectionStrategy()
    # Text with zero-width spaces (\u200b)
    text = "U\u200bR\u200bG\u200bE\u200bN\u200bT\u200bE"
    score = strategy.analyze(text)
    assert score > 0.0
    assert any("hidden/zero-width" in f for f in strategy.get_findings())

def test_obfuscation_strategy_irregular_spacing():
    strategy = ObfuscationDetectionStrategy()
    # Irregular spacing bypassing word boundary filters
    text = "C U E N T A B L O Q U E A D A"
    score = strategy.analyze(text)
    assert score > 0.0
    assert any("irregular spacing" in f for f in strategy.get_findings())

def test_obfuscation_strategy_mixed_alphabets():
    strategy = ObfuscationDetectionStrategy()
    # Mix Latin with Cyrillic characters (e.g. Cyrillic 'а')
    text = "bаnco" # Cyrillic a (\u0430)
    score = strategy.analyze(text)
    assert score > 0.0
    assert any("mixed character sets" in f for f in strategy.get_findings())

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
