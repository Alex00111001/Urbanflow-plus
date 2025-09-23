from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def _sample_route_request() -> dict:
    return {
        "origin": {"label": "Casa"},
        "destination": {"label": "Trabajo"},
        "preference": {"prioritize": "fastest"},
    }


def test_plan_route_returns_itineraries():
    response = client.post("/routes/plan", json=_sample_route_request())
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["itineraries"]) >= 1
    itinerary = payload["itineraries"][0]
    assert itinerary["steps"][0]["mode"] in {"walk", "bike_share", "bus", "ride_hailing"}


def test_replan_route_returns_recovery_itinerary():
    request_payload = _sample_route_request() | {"trip_id": "trip-1", "disruption": "Delay", "current_step": 1}
    response = client.post("/routes/replan", json=request_payload)
    assert response.status_code == 200
    itinerary = response.json()
    assert itinerary["explanation"].startswith("Replanificación")
