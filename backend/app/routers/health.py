"""Health and diagnostics endpoints."""

from fastapi import APIRouter

from ..services import telemetry

router = APIRouter()


@router.get("/health", summary="API health status")
def healthcheck() -> dict:
    """Return service health information including build metadata."""
    return telemetry.collect_health_snapshot()


@router.get("/features", summary="List available UrbanFlow+ capabilities")
def list_capabilities() -> dict:
    """Expose a high level overview of currently implemented API capabilities."""
    return {"capabilities": telemetry.available_capabilities()}
