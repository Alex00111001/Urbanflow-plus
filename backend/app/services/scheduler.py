"""Premium scheduling and insights services."""

from __future__ import annotations

from datetime import timedelta

from ..models.requests import HeatmapRequest, RouteRequest, ScheduleRequest
from ..models.responses import HeatmapInsight, PremiumSchedule
from . import route_engine


def compute_schedule(request: ScheduleRequest) -> PremiumSchedule:
    base_route = route_engine.plan_route(
        RouteRequest(
            origin=request.origin,
            destination=request.destination,
            departure_time=request.target_arrival,
        )
    )
    if not base_route.itineraries:
        raise ValueError("No itineraries available for the provided schedule request")

    fastest = base_route.itineraries[0]
    travel_time = fastest.total_duration_minutes
    buffer = request.buffer_minutes + request.weather_delay_minutes
    recommended_departure = request.target_arrival - timedelta(minutes=travel_time + buffer)

    considerations = [
        f"Tiempo de viaje estimado {travel_time:.0f} min",
        f"Buffer dinámico {buffer} min por clima y tráfico",
        "Sincronizado con rutas preferidas",
    ]

    return PremiumSchedule(
        recommended_departure=recommended_departure,
        projected_arrival=request.target_arrival,
        confidence=0.82,
        considerations=considerations,
    )


def generate_heatmap(request: HeatmapRequest) -> HeatmapInsight:
    zone_seed = abs(hash(request.user_id)) % 4
    zones = ["Centro Histórico", "Distrito Financiero", "Zona Creativa", "Bordes Verdes"]
    dominant = [zones[(zone_seed + i) % len(zones)] for i in range(2)]
    peak_hours = ["07:00-09:00", "17:30-19:00"]
    recommendation = "Explora horarios alternos para evitar picos y activa alertas inteligentes"
    if request.recent_trips:
        recommendation = "Usa el cronograma IA para espaciar tus trayectos frecuentes"
    return HeatmapInsight(dominant_zones=dominant, peak_hours=peak_hours, recommendation=recommendation)
