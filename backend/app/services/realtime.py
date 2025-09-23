"""Realtime arrival simulation services."""

from __future__ import annotations

import math
import time
from typing import List

from ..models.responses import RealtimeArrival


def _crowding_level(value: float) -> str:
    if value < 0.3:
        return "low"
    if value < 0.7:
        return "medium"
    return "high"


def fetch_arrivals(line_id: str) -> List[RealtimeArrival]:
    """Return simulated arrivals for a transit line using deterministic math."""
    now = time.time()
    base = abs(hash(line_id)) % 7
    arrivals: List[RealtimeArrival] = []
    for offset in range(3):
        wait = (base + offset * 3) % 15 + 2
        wave = math.sin(now / 300 + offset)
        confidence = max(0.5, min(0.95, 0.75 + wave * 0.1))
        crowding_value = (base + offset * 2) % 10 / 10
        arrivals.append(
            RealtimeArrival(
                line_id=line_id,
                vehicle_id=f"{line_id.upper()}-{offset+1}",
                stop="Trabajo",
                arrival_in_minutes=round(wait + wave, 2),
                crowding=_crowding_level(crowding_value),
                confidence=round(confidence, 2),
            )
        )
    return arrivals
