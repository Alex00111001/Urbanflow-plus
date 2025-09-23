import pathlib

import pytest

from app.models.requests import LocationInput, RoutePreference, RouteRequest
from app.services import gtfs_loader, route_engine


@pytest.fixture()
def sample_gtfs_path() -> pathlib.Path:
    return pathlib.Path(__file__).parent / "data" / "sample_gtfs"


@pytest.fixture()
def restore_graph():
    original_graph = route_engine.get_transit_graph()
    try:
        yield
    finally:
        route_engine.set_transit_graph(original_graph)


def test_gtfs_loader_builds_graph(sample_gtfs_path: pathlib.Path, restore_graph) -> None:
    data = gtfs_loader.load_gtfs_feed(sample_gtfs_path)
    graph = gtfs_loader.build_transit_graph(data)
    assert list(graph.neighbors("Casa")), "Expected Casa stop to have outgoing edges"
    route_engine.set_transit_graph(graph)

    request = RouteRequest(
        origin=LocationInput(label="Casa"),
        destination=LocationInput(label="Trabajo"),
        preference=RoutePreference(prioritize="fastest"),
    )

    response = route_engine.plan_route(request)
    assert response.itineraries, "No itineraries generated from GTFS graph"
    primary = response.itineraries[0]
    assert primary.steps, "Itinerary must contain steps"
    modes = {step.mode for step in primary.steps}
    assert "bus" in modes or "metro" in modes

