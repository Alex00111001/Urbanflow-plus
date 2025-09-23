from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_interpret_query_extracts_destination_and_time():
    response = client.post(
        "/search/interpret",
        json={"query": "Llévame a trabajo a las 8:30", "language": "es-419"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["destination"] == "Trabajo"
    assert payload["departure_time"] is not None


def test_plan_from_query_returns_itineraries():
    response = client.post(
        "/search/plan",
        json={"query": "Necesito llegar al centro", "language": "es-419"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["itineraries"], "Should return at least one itinerary"
