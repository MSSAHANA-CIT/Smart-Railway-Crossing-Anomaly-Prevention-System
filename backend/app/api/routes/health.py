"""Health, root, and version endpoints."""

from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.health import HealthResponse, RootResponse, VersionResponse

settings = get_settings()

root_router = APIRouter(tags=["Root"])
api_router = APIRouter(tags=["Health"])


@root_router.get("/", response_model=RootResponse)
async def root() -> RootResponse:
    return RootResponse(
        project=settings.PROJECT_NAME,
        short_title=settings.PROJECT_SHORT_NAME,
        version=settings.APP_VERSION,
        status="active",
        message=(
            "Backend foundation active. "
            "Sensors, database, and authentication not yet integrated."
        ),
    )


@api_router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        service="railway-crossing-api",
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        message="Backend is running and ready for Phase S2 development.",
    )


@api_router.get("/version", response_model=VersionResponse)
async def version() -> VersionResponse:
    return VersionResponse(
        project=settings.PROJECT_NAME,
        short_title=settings.PROJECT_SHORT_NAME,
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        api_prefix=settings.API_PREFIX,
    )
