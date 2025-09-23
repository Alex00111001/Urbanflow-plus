"""Response schemas for UrbanFlow+ API."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ParsedQuery(BaseModel):
    origin: Optional[str]
    destination: Optional[str]
    departure_time: Optional[datetime]
    language: str


class RouteStep(BaseModel):
    mode: str
    instruction: str
    duration_minutes: float
    distance_meters: float
    cost: float
    co2_kg: float
    accessibility: str = Field("standard", description="Accessibility annotation for the step")


class Itinerary(BaseModel):
    id: str
    total_duration_minutes: float
    total_cost: float
    total_co2_kg: float
    transfers: int
    score: float
    steps: List[RouteStep]
    explanation: Optional[str] = None


class RouteResponse(BaseModel):
    generated_at: datetime
    itineraries: List[Itinerary]


class RealtimeArrival(BaseModel):
    line_id: str
    vehicle_id: str
    stop: str
    arrival_in_minutes: float
    crowding: str
    confidence: float


class PremiumSchedule(BaseModel):
    recommended_departure: datetime
    projected_arrival: datetime
    confidence: float
    considerations: List[str]


class HeatmapInsight(BaseModel):
    dominant_zones: List[str]
    peak_hours: List[str]
    recommendation: str
