"""Routing endpoints for UrbanFlow+."""

from fastapi import APIRouter, HTTPException

from ..models.requests import ReplanRequest, RouteRequest
from ..models.responses import Itinerary, RouteResponse
from ..services import route_engine

router = APIRouter()


@router.post("/plan", response_model=RouteResponse)
def plan_route(request: RouteRequest) -> RouteResponse:
    """Plan one or more itineraries between the requested endpoints."""
    return route_engine.plan_route(request)


@router.post("/replan", response_model=Itinerary)
def replan_route(request: ReplanRequest) -> Itinerary:
    """Generate a recovery itinerary when a disruption occurs."""
    base_request = RouteRequest(
        origin=request.origin,
        destination=request.destination,
        preference=request.preference,
    )
    itinerary = route_engine.replan_trip(base_request, request.disruption)
    if not itinerary:
        raise HTTPException(status_code=404, detail="No recovery itinerary available")
    return itinerary
