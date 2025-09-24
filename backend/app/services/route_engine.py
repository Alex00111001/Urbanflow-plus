"""Simplified multimodal routing engine for UrbanFlow+."""

from __future__ import annotations

import heapq
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Iterable, List, Optional, Tuple
from uuid import uuid4

from ..models.requests import RoutePreference, RouteRequest
from ..models.responses import Itinerary, RouteResponse, RouteStep

__all__ = [
    "Edge",
    "TransitGraph",
    "plan_route",
    "replan_trip",
    "set_transit_graph",
    "get_transit_graph",
    "reset_transit_graph",
]

@dataclass(frozen=True)
class Edge:
    origin: str
    destination: str
    mode: str
    duration: float  # minutes
    distance: float  # meters
    cost: float  # local currency
    co2: float  # kg
    accessibility: str


class TransitGraph:
    """In-memory representation of a small multimodal transport graph."""

    def __init__(self, edges: Iterable[Edge]):
        self._edges = list(edges)
        self._adjacency: Dict[str, List[Edge]] = {}
        for edge in self._edges:
            self._adjacency.setdefault(edge.origin, []).append(edge)

    def neighbors(self, node: str) -> List[Edge]:
        return self._adjacency.get(node, [])


_SAMPLE_EDGES = [
    Edge("Casa", "Metro Azul", "walk", 6, 450, 0, 0.0, "accessible"),
    Edge("Metro Azul", "Centro", "metro", 12, 5400, 0.8, 0.3, "accessible"),
    Edge("Centro", "Trabajo", "walk", 5, 380, 0, 0.0, "accessible"),
    Edge("Casa", "Bicicletas Rio", "bike_share", 3, 620, 0.5, 0.0, "standard"),
    Edge("Bicicletas Rio", "Trabajo", "bike", 18, 6400, 0, 0.0, "standard"),
    Edge("Casa", "Parada 21", "bus", 10, 3200, 0.6, 0.5, "accessible"),
    Edge("Parada 21", "Trabajo", "bus", 20, 7000, 0.6, 0.6, "accessible"),
    Edge("Casa", "RideShare", "ride_hailing", 2, 1000, 1.5, 0.9, "accessible"),
    Edge("RideShare", "Trabajo", "ride_hailing", 14, 7200, 4.5, 2.1, "accessible"),
    Edge("Casa", "Tren Leste", "walk", 7, 550, 0, 0.0, "accessible"),
    Edge("Tren Leste", "Centro", "train", 15, 7800, 0.9, 0.4, "accessible"),
]

def _build_default_graph() -> TransitGraph:
    return TransitGraph(list(_SAMPLE_EDGES))


_GRAPH = _build_default_graph()


def set_transit_graph(graph: TransitGraph) -> None:
    """Replace the global transit graph used for routing."""

    global _GRAPH
    _GRAPH = graph


def get_transit_graph() -> TransitGraph:
    """Return the current global transit graph."""

    return _GRAPH


def reset_transit_graph() -> None:
    """Restore the routing engine to the baked-in demo graph."""

    set_transit_graph(_build_default_graph())


def _weight_for_edge(edge: Edge, preference: RoutePreference, previous_mode: Optional[str]) -> float:
    base = edge.duration

    if preference.prioritize == "cheapest":
        base = edge.cost * 10 + edge.duration * 0.3
    elif preference.prioritize == "least_walking":
        walking_penalty = 15 if edge.mode == "walk" else 0
        base = edge.duration + walking_penalty
    elif preference.prioritize == "accessible":
        accessibility_penalty = 50 if edge.accessibility != "accessible" else 0
        base = edge.duration + accessibility_penalty
    elif preference.prioritize == "green":
        base = edge.co2 * 40 + edge.duration * 0.5

    if preference.avoid_transfers and previous_mode and previous_mode != edge.mode:
        base += 8

    if preference.accessibility_required and edge.accessibility != "accessible":
        return float("inf")

    return base


def _dijkstra(
    origin: str,
    destination: str,
    preference: RoutePreference,
    graph: TransitGraph,
) -> Optional[List[Edge]]:
    queue: List[Tuple[float, str, Optional[str]]] = [(0.0, origin, None)]
    visited: Dict[str, float] = {origin: 0.0}
    previous: Dict[str, Tuple[str, Edge]] = {}

    while queue:
        current_cost, node, previous_mode = heapq.heappop(queue)
        if node == destination:
            break
        if current_cost > visited.get(node, float("inf")):
            continue
        for edge in graph.neighbors(node):
            weight = _weight_for_edge(edge, preference, previous_mode)
            if weight == float("inf"):
                continue
            new_cost = current_cost + weight
            best = visited.get(edge.destination)
            if best is None or new_cost < best:
                visited[edge.destination] = new_cost
                previous[edge.destination] = (node, edge)
                heapq.heappush(queue, (new_cost, edge.destination, edge.mode))

    if destination not in previous and destination != origin:
        return None

    path: List[Edge] = []
    node = destination
    while node != origin:
        parent, edge = previous[node]
        path.append(edge)
        node = parent
    path.reverse()
    return path


def _edges_to_itinerary(edges: List[Edge], preference: RoutePreference, explanation: Optional[str]) -> Itinerary:
    total_duration = sum(edge.duration for edge in edges)
    total_cost = sum(edge.cost for edge in edges)
    total_co2 = sum(edge.co2 for edge in edges)
    transfers = 0
    last_mode: Optional[str] = None
    steps: List[RouteStep] = []
    for edge in edges:
        if last_mode and last_mode != edge.mode:
            transfers += 1
        last_mode = edge.mode
        steps.append(
            RouteStep(
                mode=edge.mode,
                instruction=f"{edge.mode.replace('_', ' ').title()} from {edge.origin} to {edge.destination}",
                duration_minutes=edge.duration,
                distance_meters=edge.distance,
                cost=edge.cost,
                co2_kg=edge.co2,
                accessibility=edge.accessibility,
            )
        )

    if explanation is None:
        explanation = _build_explanation(preference, total_duration, total_cost, total_co2, transfers)

    score = _score_itinerary(preference, total_duration, total_cost, total_co2, transfers)

    return Itinerary(
        id=str(uuid4()),
        total_duration_minutes=round(total_duration, 2),
        total_cost=round(total_cost, 2),
        total_co2_kg=round(total_co2, 3),
        transfers=transfers,
        score=round(score, 3),
        steps=steps,
        explanation=explanation,
    )


def _build_explanation(
    preference: RoutePreference,
    duration: float,
    cost: float,
    co2: float,
    transfers: int,
) -> str:
    reasons = [
        f"Duración estimada {duration:.0f} min",
        f"Costo total {cost:.2f}",
        f"CO₂ {co2:.2f} kg",
        f"{transfers} transbordos",
    ]

    if preference.prioritize == "fastest":
        reasons.insert(0, "Seleccionamos la ruta más rápida disponible")
    elif preference.prioritize == "cheapest":
        reasons.insert(0, "Optimizamos por menor costo total")
    elif preference.prioritize == "least_walking":
        reasons.insert(0, "Priorizamos minimizar la caminata")
    elif preference.prioritize == "accessible":
        reasons.insert(0, "Solo incluimos segmentos accesibles")
    elif preference.prioritize == "green":
        reasons.insert(0, "Seleccionamos la alternativa con menor huella de CO₂")

    return " | ".join(reasons)


def _score_itinerary(
    preference: RoutePreference,
    duration: float,
    cost: float,
    co2: float,
    transfers: int,
) -> float:
    weights = {
        "fastest": (0.6, 0.2, 0.1, 0.1),
        "cheapest": (0.2, 0.6, 0.1, 0.1),
        "least_walking": (0.5, 0.1, 0.2, 0.2),
        "accessible": (0.4, 0.1, 0.1, 0.4),
        "green": (0.3, 0.1, 0.5, 0.1),
    }[preference.prioritize]
    duration_norm = duration / 60
    cost_norm = cost / 5 if cost else 0
    co2_norm = co2 / 2 if co2 else 0
    transfers_norm = transfers / 3 if transfers else 0
    duration_norm = min(duration_norm, 1.5)
    cost_norm = min(cost_norm, 1.5)
    co2_norm = min(co2_norm, 1.5)
    transfers_norm = min(transfers_norm, 1.5)
    total = (
        (1 - duration_norm) * weights[0]
        + (1 - cost_norm) * weights[1]
        + (1 - co2_norm) * weights[2]
        + (1 - transfers_norm) * weights[3]
    )
    return max(total, 0.0)


def plan_route(request: RouteRequest) -> RouteResponse:
    """Return itineraries generated according to the provided preferences."""
    now = datetime.utcnow()
    preference = request.preference

    candidate_preferences = [preference]
    alt_mapping = {
        "fastest": ["cheapest", "green"],
        "cheapest": ["fastest", "green"],
        "least_walking": ["fastest", "accessible"],
        "accessible": ["fastest", "cheapest"],
        "green": ["fastest", "cheapest"],
    }
    for alt in alt_mapping[preference.prioritize]:
        candidate_preferences.append(
            RoutePreference(
                prioritize=alt,
                avoid_transfers=preference.avoid_transfers,
                accessibility_required=preference.accessibility_required,
            )
        )

    graph = get_transit_graph()
    itineraries: List[Itinerary] = []
    for candidate in candidate_preferences:
        edges = _dijkstra(request.origin.label, request.destination.label, candidate, graph)
        if not edges:
            continue
        explanation = None
        if candidate is not preference:
            explanation = (
                f"Alternativa optimizada por {candidate.prioritize.replace('_', ' ')}"
            )
        itineraries.append(_edges_to_itinerary(edges, candidate, explanation))

    itineraries.sort(key=lambda it: it.score, reverse=True)
    return RouteResponse(generated_at=now, itineraries=itineraries)


def replan_trip(request: RouteRequest, disruption: str) -> Optional[Itinerary]:
    """Generate a new itinerary with minimal deviation after a disruption."""
    fallback_pref = RoutePreference(
        prioritize="fastest",
        avoid_transfers=True,
        accessibility_required=request.preference.accessibility_required,
    )
    graph = get_transit_graph()
    edges = _dijkstra(request.origin.label, request.destination.label, fallback_pref, graph)
    if not edges:
        return None
    explanation = f"Replanificación por evento: {disruption}"
    return _edges_to_itinerary(edges, fallback_pref, explanation)
