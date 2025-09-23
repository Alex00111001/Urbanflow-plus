from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert "build" in payload


def test_features_endpoint_lists_capabilities():
    response = client.get("/features")
    assert response.status_code == 200
    capabilities = response.json()["capabilities"]
    assert "multimodal_routing" in capabilities
