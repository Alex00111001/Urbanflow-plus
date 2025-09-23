"""Natural language query interpretation utilities."""

from __future__ import annotations

import re
from datetime import datetime, timedelta
from typing import Optional, Tuple

from ..models.requests import LocationInput, RoutePreference, RouteRequest, SearchQuery
from ..models.responses import ParsedQuery


_PLACES = {
    "casa": "Casa",
    "trabajo": "Trabajo",
    "centro": "Centro",
    "metro": "Metro Azul",
    "metro azul": "Metro Azul",
    "parada": "Parada 21",
}

_TIME_PATTERNS = [
    re.compile(r"a las (?P<hour>\d{1,2})(:(?P<minute>\d{2}))?", re.IGNORECASE),
    re.compile(r"at (?P<hour>\d{1,2})(:(?P<minute>\d{2}))?", re.IGNORECASE),
    re.compile(r"para las (?P<hour>\d{1,2})(:(?P<minute>\d{2}))?", re.IGNORECASE),
]


def _normalize_place(place: str) -> Optional[str]:
    place = place.strip().lower()
    return _PLACES.get(place)


def _parse_time(query: str) -> Optional[datetime]:
    for pattern in _TIME_PATTERNS:
        match = pattern.search(query)
        if match:
            hour = int(match.group("hour"))
            minute = int(match.group("minute") or 0)
            now = datetime.utcnow()
            candidate = now.replace(hour=hour % 24, minute=minute, second=0, microsecond=0)
            if candidate < now:
                candidate += timedelta(days=1)
            return candidate
    return None


def interpret_query(query: SearchQuery) -> Tuple[ParsedQuery, Optional[RouteRequest]]:
    """Return parsed metadata and an optional auto-generated route request."""
    text = query.query
    time_value = _parse_time(text)

    origin: Optional[str] = None
    destination: Optional[str] = None

    lower = text.lower()
    match = re.search(r"ll[ée]vame (?:hasta |a )(?P<dest>[a-záéíóúü0-9\s]+)", lower)
    if match:
        destination_candidate = match.group("dest")
        destination_candidate = re.split(r"a las|para las|en |\d{1,2}:\d{2}", destination_candidate)[0]
        destination_candidate = destination_candidate.strip().rstrip(".?!")
        if destination_candidate:
            destination = _normalize_place(destination_candidate) or destination_candidate.title()
    if "desde" in lower:
        match = re.search(r"desde ([a-zA-Z\s]+)", lower)
        if match:
            origin_candidate = match.group(1).strip()
            origin = _normalize_place(origin_candidate) or origin_candidate.title()

    if not origin:
        if "casa" in lower:
            origin = _PLACES["casa"]
        else:
            origin = "Casa"
    if not destination:
        for alias, place in _PLACES.items():
            if alias in lower and place != _PLACES["casa"]:
                destination = place
                break
        if not destination:
            destination = "Trabajo"

    parsed = ParsedQuery(
        origin=origin,
        destination=destination,
        departure_time=time_value,
        language=query.language,
    )

    origin_location = LocationInput(label=origin)
    destination_location = LocationInput(label=destination)
    preference = RoutePreference(prioritize="fastest")
    route_request = RouteRequest(
        origin=origin_location,
        destination=destination_location,
        departure_time=time_value,
        preference=preference,
    )

    return parsed, route_request
