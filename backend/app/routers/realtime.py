"""Realtime endpoints."""

from fastapi import APIRouter

from ..models.responses import RealtimeArrival
from ..services import realtime

router = APIRouter()


@router.get("/{line_id}", response_model=list[RealtimeArrival])
def realtime_feed(line_id: str) -> list[RealtimeArrival]:
    """Return simulated realtime arrivals for the requested line."""
    return realtime.fetch_arrivals(line_id)
