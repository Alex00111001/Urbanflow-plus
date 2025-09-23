"""Premium endpoints for UrbanFlow+."""

from fastapi import APIRouter, HTTPException

from ..models.requests import HeatmapRequest, ScheduleRequest
from ..models.responses import HeatmapInsight, PremiumSchedule
from ..services import scheduler

router = APIRouter()


@router.post("/schedule", response_model=PremiumSchedule)
def build_schedule(request: ScheduleRequest) -> PremiumSchedule:
    try:
        return scheduler.compute_schedule(request)
    except ValueError as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/heatmap", response_model=HeatmapInsight)
def heatmap(request: HeatmapRequest) -> HeatmapInsight:
    return scheduler.generate_heatmap(request)
