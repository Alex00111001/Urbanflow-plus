from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def _schedule_request_payload() -> dict:
    return {
        "origin": {"label": "Casa"},
        "destination": {"label": "Trabajo"},
        "target_arrival": (datetime.utcnow() + timedelta(hours=1)).isoformat(),
        "buffer_minutes": 5,
        "weather_delay_minutes": 5,
    }


def test_schedule_endpoint_returns_recommendation():
    response = client.post("/premium/schedule", json=_schedule_request_payload())
    assert response.status_code == 200
    payload = response.json()
    assert "recommended_departure" in payload
    assert payload["confidence"] > 0.7


def test_heatmap_endpoint_returns_zones():
    response = client.post(
        "/premium/heatmap",
        json={"user_id": "user-123", "recent_trips": ["t1", "t2"]},
    )
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["dominant_zones"]) == 2
