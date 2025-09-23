"""Utilities to ingest GTFS feeds into the UrbanFlow+ routing engine."""
from __future__ import annotations

import csv
import io
import math
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from .route_engine import Edge, TransitGraph


@dataclass
class GTFSStop:
    stop_id: str
    name: str
    lat: float
    lon: float


@dataclass
class GTFSRoute:
    route_id: str
    route_type: int


@dataclass
class GTFSTrip:
    trip_id: str
    route_id: str


@dataclass
class GTFSStopTime:
    trip_id: str
    stop_id: str
    arrival_minutes: float
    departure_minutes: float
    sequence: int


@dataclass
class GTFSData:
    stops: Dict[str, GTFSStop]
    routes: Dict[str, GTFSRoute]
    trips: Dict[str, GTFSTrip]
    stop_times: Dict[str, List[GTFSStopTime]]


_ROUTE_TYPE_TO_MODE: Dict[int, str] = {
    0: "tram",
    1: "metro",
    2: "train",
    3: "bus",
    4: "ferry",
    5: "cable_car",
    6: "gondola",
    7: "funicular",
    11: "bus",
    12: "metro",
}

_MODE_PROFILES: Dict[str, Tuple[float, float, float, str]] = {
    "walk": (0.0, 0.0, 0.0, "accessible"),
    "tram": (1.5, 0.15, 0.04, "accessible"),
    "metro": (1.8, 0.12, 0.03, "accessible"),
    "train": (2.0, 0.18, 0.05, "accessible"),
    "bus": (1.3, 0.14, 0.08, "standard"),
    "ferry": (2.2, 0.25, 0.09, "accessible"),
    "cable_car": (2.0, 0.20, 0.07, "accessible"),
    "gondola": (2.0, 0.18, 0.06, "accessible"),
    "funicular": (1.8, 0.15, 0.05, "accessible"),
    "bus_rapid_transit": (1.5, 0.16, 0.07, "accessible"),
}


def load_gtfs_feed(feed_path: Path | str) -> GTFSData:
    """Load minimal GTFS tables required for routing."""

    path = Path(feed_path)
    if not path.exists():
        raise FileNotFoundError(f"GTFS feed not found: {feed_path}")

    if path.is_dir():
        return _load_from_directory(path)
    if path.suffix.lower() == ".zip":
        return _load_from_zip(path)

    raise ValueError("feed_path must be a directory or .zip file")


def build_transit_graph(data: GTFSData) -> TransitGraph:
    """Convert GTFS data into the routing engine TransitGraph."""

    edges: Dict[Tuple[str, str, str], Edge] = {}

    for trip_id, stop_times in data.stop_times.items():
        trip = data.trips.get(trip_id)
        if not trip:
            continue
        route = data.routes.get(trip.route_id)
        mode = _mode_for_route(route.route_type if route else None)
        ordered = sorted(stop_times, key=lambda st: st.sequence)
        for prev, curr in _pairwise(ordered):
            if prev.stop_id not in data.stops or curr.stop_id not in data.stops:
                continue
            origin_stop = data.stops[prev.stop_id]
            dest_stop = data.stops[curr.stop_id]
            duration_minutes = max(curr.arrival_minutes - prev.departure_minutes, 0.1)
            if duration_minutes <= 0:
                # Handles overnight services using modulo 24h and avoids zero durations
                duration_minutes = (duration_minutes % (24 * 60)) or _duration_from_distance(origin_stop, dest_stop, mode)
            distance_meters = _haversine(origin_stop.lat, origin_stop.lon, dest_stop.lat, dest_stop.lon)
            if distance_meters <= 0:
                distance_meters = 100.0  # fallback small distance
            cost, variable_cost, emission, accessibility = _MODE_PROFILES.get(mode, (1.5, 0.18, 0.06, "standard"))
            distance_km = distance_meters / 1000
            total_cost = cost + variable_cost * distance_km
            co2 = emission * distance_km
            key = (origin_stop.name, dest_stop.name, mode)
            candidate = Edge(
                origin=origin_stop.name,
                destination=dest_stop.name,
                mode=mode,
                duration=round(duration_minutes, 2),
                distance=round(distance_meters, 2),
                cost=round(total_cost, 2),
                co2=round(co2, 3),
                accessibility=accessibility,
            )
            previous = edges.get(key)
            if not previous or candidate.duration < previous.duration:
                edges[key] = candidate

    return TransitGraph(edges.values())


def _load_from_directory(path: Path) -> GTFSData:
    stops = _read_csv(path / "stops.txt")
    routes = _read_csv(path / "routes.txt")
    trips = _read_csv(path / "trips.txt")
    stop_times = _read_csv(path / "stop_times.txt")
    return _build_data_structures(stops, routes, trips, stop_times)


def _load_from_zip(path: Path) -> GTFSData:
    with zipfile.ZipFile(path) as zf:
        stops = _read_csv_from_zip(zf, "stops.txt")
        routes = _read_csv_from_zip(zf, "routes.txt")
        trips = _read_csv_from_zip(zf, "trips.txt")
        stop_times = _read_csv_from_zip(zf, "stop_times.txt")
    return _build_data_structures(stops, routes, trips, stop_times)


def _read_csv(file_path: Path) -> List[Dict[str, str]]:
    if not file_path.exists():
        raise FileNotFoundError(f"Missing required GTFS file: {file_path.name}")
    with file_path.open("r", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _read_csv_from_zip(zf: zipfile.ZipFile, name: str) -> List[Dict[str, str]]:
    try:
        with zf.open(name) as handle:
            return list(csv.DictReader(io.TextIOWrapper(handle, encoding="utf-8-sig")))
    except KeyError as exc:
        raise FileNotFoundError(f"Missing required GTFS file inside archive: {name}") from exc


def _build_data_structures(
    stops_rows: Iterable[Dict[str, str]],
    routes_rows: Iterable[Dict[str, str]],
    trips_rows: Iterable[Dict[str, str]],
    stop_times_rows: Iterable[Dict[str, str]],
) -> GTFSData:
    stops: Dict[str, GTFSStop] = {}
    for row in stops_rows:
        try:
            stop = GTFSStop(
                stop_id=row["stop_id"],
                name=row.get("stop_name", row["stop_id"]),
                lat=float(row["stop_lat"]),
                lon=float(row["stop_lon"]),
            )
            stops[stop.stop_id] = stop
        except (KeyError, ValueError) as exc:
            raise ValueError(f"Invalid stop row: {row}") from exc

    routes: Dict[str, GTFSRoute] = {}
    for row in routes_rows:
        try:
            route = GTFSRoute(
                route_id=row["route_id"],
                route_type=int(float(row.get("route_type", 3))),
            )
            routes[route.route_id] = route
        except (KeyError, ValueError) as exc:
            raise ValueError(f"Invalid route row: {row}") from exc

    trips: Dict[str, GTFSTrip] = {}
    for row in trips_rows:
        try:
            trip = GTFSTrip(trip_id=row["trip_id"], route_id=row["route_id"])
            trips[trip.trip_id] = trip
        except KeyError as exc:
            raise ValueError(f"Invalid trip row: {row}") from exc

    stop_times: Dict[str, List[GTFSStopTime]] = {}
    for row in stop_times_rows:
        try:
            trip_id = row["trip_id"]
            stop_time = GTFSStopTime(
                trip_id=trip_id,
                stop_id=row["stop_id"],
                arrival_minutes=_parse_time_to_minutes(row.get("arrival_time")),
                departure_minutes=_parse_time_to_minutes(row.get("departure_time")),
                sequence=int(row.get("stop_sequence", "0")),
            )
            stop_times.setdefault(trip_id, []).append(stop_time)
        except (KeyError, ValueError) as exc:
            raise ValueError(f"Invalid stop_time row: {row}") from exc

    return GTFSData(stops=stops, routes=routes, trips=trips, stop_times=stop_times)


def _parse_time_to_minutes(value: Optional[str]) -> float:
    if not value or value == "":
        return 0.0
    parts = value.split(":")
    if len(parts) != 3:
        raise ValueError(f"Invalid GTFS time: {value}")
    hours, minutes, seconds = (int(part) for part in parts)
    return hours * 60 + minutes + seconds / 60


def _mode_for_route(route_type: Optional[int]) -> str:
    if route_type is None:
        return "bus"
    return _ROUTE_TYPE_TO_MODE.get(route_type, "walk")


def _pairwise(items: List[GTFSStopTime]) -> Iterable[Tuple[GTFSStopTime, GTFSStopTime]]:
    for idx in range(len(items) - 1):
        yield items[idx], items[idx + 1]


def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius = 6371000  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius * c


def _duration_from_distance(origin: GTFSStop, dest: GTFSStop, mode: str) -> float:
    # Provide a sensible fallback speed in meters per minute depending on mode.
    speeds = {
        "walk": 80,
        "bus": 300,
        "metro": 500,
        "train": 550,
        "tram": 350,
        "ferry": 250,
    }
    distance = _haversine(origin.lat, origin.lon, dest.lat, dest.lon)
    speed = speeds.get(mode, 300)
    minutes = distance / speed if speed else 1
    return max(minutes, 1.0)
