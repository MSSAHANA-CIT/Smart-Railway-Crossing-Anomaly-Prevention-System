"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.auth import router as auth_router
from app.api.routes.devices import router as devices_router
from app.api.routes.health import api_router, root_router
from app.api.routes.organization import router as organization_router
from app.api.routes.railway_crossings import router as railway_crossings_router
from app.api.routes.railway_divisions import router as railway_divisions_router
from app.api.routes.railway_stations import router as railway_stations_router
from app.api.routes.railway_zones import router as railway_zones_router
from app.api.routes.sensors import router as sensors_router
from app.api.routes.staff_assignments import router as staff_assignments_router
from app.api.routes.users import router as users_router
from app.core.config import get_settings
from app.core.logging import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(
        "Starting %s v%s [%s]",
        settings.PROJECT_SHORT_NAME,
        settings.APP_VERSION,
        settings.ENVIRONMENT,
    )
    yield
    logger.info("Shutting down %s", settings.PROJECT_SHORT_NAME)


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.APP_VERSION,
    description=(
        "Risk-Adaptive Railway Crossing Protection System — "
        "Phase S4 railway organization hierarchy, device registration, "
        "sensor registration, and staff assignment foundation. "
        "Prototype system; not connected to Indian Railways production systems."
    ),
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root_router)
app.include_router(api_router, prefix=settings.API_PREFIX)
app.include_router(auth_router, prefix=settings.API_PREFIX)
app.include_router(users_router, prefix=settings.API_PREFIX)
app.include_router(railway_zones_router, prefix=settings.API_PREFIX)
app.include_router(railway_divisions_router, prefix=settings.API_PREFIX)
app.include_router(railway_stations_router, prefix=settings.API_PREFIX)
app.include_router(railway_crossings_router, prefix=settings.API_PREFIX)
app.include_router(organization_router, prefix=settings.API_PREFIX)
app.include_router(devices_router, prefix=settings.API_PREFIX)
app.include_router(sensors_router, prefix=settings.API_PREFIX)
app.include_router(staff_assignments_router, prefix=settings.API_PREFIX)
