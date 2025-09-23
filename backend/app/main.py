"""Entry point for the UrbanFlow+ backend application."""

from fastapi import FastAPI

from .routers import health, routes, realtime, premium, search


app = FastAPI(
    title="UrbanFlow+ API",
    description="Urban mobility intelligence platform with routing AI, realtime transit, and premium trip services.",
    version="0.1.0",
)

app.include_router(health.router)
app.include_router(search.router, prefix="/search", tags=["search"])
app.include_router(routes.router, prefix="/routes", tags=["routes"])
app.include_router(realtime.router, prefix="/realtime", tags=["realtime"])
app.include_router(premium.router, prefix="/premium", tags=["premium"])

