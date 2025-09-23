"""Service utilities for telemetry and metadata reporting."""

from __future__ import annotations

import platform
import time
from typing import Dict, List

_BUILD_INFO = {
    "name": "UrbanFlow+ Backend",
    "version": "0.1.0",
    "commit": "dev",
}


_CAPABILITIES = [
    "natural_language_search",
    "multimodal_routing",
    "realtime_arrivals",
    "premium_scheduling",
    "explainable_recommendations",
]


def collect_health_snapshot() -> Dict[str, object]:
    """Gather runtime metadata for health endpoints."""
    return {
        "status": "ok",
        "timestamp": time.time(),
        "build": _BUILD_INFO,
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
    }


def available_capabilities() -> List[str]:
    """Expose the registered backend capabilities."""
    return list(_CAPABILITIES)
