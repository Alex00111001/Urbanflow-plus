"""Request schemas for the UrbanFlow+ API."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class Coordinate(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)


class LocationInput(BaseModel):
    label: str = Field(..., description="Human readable place label")
    coordinate: Optional[Coordinate] = Field(None, description="Optional geolocation for the place")


class RoutePreference(BaseModel):
    prioritize: str = Field(
        "fastest",
        description="Optimization goal: fastest | cheapest | least_walking | accessible | green",
    )
    avoid_transfers: bool = Field(False, description="Whether to penalize itineraries with multiple transfers")
    accessibility_required: bool = Field(False, description="Require accessible steps such as elevators and ramps")

    @field_validator("prioritize")
    @classmethod
    def validate_prioritize(cls, value: str) -> str:
        allowed = {"fastest", "cheapest", "least_walking", "accessible", "green"}
        if value not in allowed:
            raise ValueError(f"prioritize must be one of {sorted(allowed)}")
        return value


class RouteRequest(BaseModel):
    origin: LocationInput
    destination: LocationInput
    departure_time: Optional[datetime] = Field(
        None,
        description="Desired departure time. Defaults to now if not provided.",
    )
    preference: RoutePreference = Field(default_factory=RoutePreference)
    include_explanation: bool = Field(True, description="Include decision explanation metadata")


class ReplanRequest(BaseModel):
    trip_id: str
    origin: LocationInput
    destination: LocationInput
    preference: RoutePreference = Field(default_factory=RoutePreference)
    disruption: str = Field(..., description="Description of the disruption that triggered the replan")
    current_step: int = Field(..., ge=0, description="Current step index in the itinerary")


class SearchQuery(BaseModel):
    query: str
    language: str = Field("es-419", description="BCP47 locale for the natural language parser")


class ScheduleRequest(BaseModel):
    origin: LocationInput
    destination: LocationInput
    target_arrival: datetime
    buffer_minutes: int = Field(10, ge=0, le=90)
    weather_delay_minutes: int = Field(5, ge=0, le=60)


class HeatmapRequest(BaseModel):
    user_id: str
    recent_trips: List[str] = Field(default_factory=list, description="List of trip identifiers to aggregate usage")
