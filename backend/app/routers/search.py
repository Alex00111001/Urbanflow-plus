"""Search endpoints."""

from fastapi import APIRouter

from ..models.requests import SearchQuery
from ..models.responses import ParsedQuery, RouteResponse
from ..services import route_engine, search

router = APIRouter()


@router.post("/interpret", response_model=ParsedQuery)
def interpret(query: SearchQuery) -> ParsedQuery:
    parsed, _ = search.interpret_query(query)
    return parsed


@router.post("/plan", response_model=RouteResponse)
def plan_from_query(query: SearchQuery) -> RouteResponse:
    parsed, route_request = search.interpret_query(query)
    _ = parsed  # for parity with interface, ensures parser executed
    return route_engine.plan_route(route_request)
