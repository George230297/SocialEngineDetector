import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_root(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Social Engineering Detector API"}

@pytest.mark.asyncio
async def test_analyze_url_safe(client: AsyncClient):
    payload = {
        "artifact_type": "URL",
        "content": "https://google.com"
    }
    response = await client.post("/api/v1/scan/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["risk_level"] == "SAFE"
    assert data["risk_score"] == 0

@pytest.mark.asyncio
async def test_analyze_url_malicious(client: AsyncClient):
    payload = {
        "artifact_type": "URL",
        "content": "http://paypal-secure-update.com.login.php"
    }
    response = await client.post("/api/v1/scan/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["risk_level"] in ["SUSPICIOUS", "MALICIOUS"]
    assert data["risk_score"] > 0

@pytest.mark.asyncio
async def test_analyze_text_urgency(client: AsyncClient):
    payload = {
        "artifact_type": "TEXT",
        "content": "URGENTE: Envia tu contraseña al CEO inmediatamente."
    }
    response = await client.post("/api/v1/scan/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["risk_level"] == "MALICIOUS"
    assert data["risk_score"] > 50
    assert any("urgente" in finding.lower() for finding in data["findings"])
