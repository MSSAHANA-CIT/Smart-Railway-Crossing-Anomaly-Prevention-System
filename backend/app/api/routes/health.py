"""Health, root, and version endpoints."""

from fastapi import APIRouter

from app.core.config import get_settings
from app.db.init_db import test_database_connection
from app.schemas.health import (
    DbHealthResponse,
    HealthResponse,
    RootResponse,
    VersionResponse,
)

settings = get_settings()

root_router = APIRouter(tags=["Root"])
api_router = APIRouter(tags=["Health"])


def _database_status() -> tuple[str, str]:
    """Return database connection status and message."""
    connected, message = test_database_connection()
    if connected:
        return "connected", message
    return "disconnected", message


@root_router.get("/", response_model=RootResponse)
async def root() -> RootResponse:
    return RootResponse(
        project=settings.PROJECT_NAME,
        short_title=settings.PROJECT_SHORT_NAME,
        version=settings.APP_VERSION,
        status="active",
        message=(
            "Backend foundation active with IAM authentication. "
            "Use /api/auth/login to obtain a JWT access token."
        ),
    )


@api_router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    db_status, db_message = _database_status()
    backend_status = "healthy" if db_status == "connected" else "degraded"

    if db_status == "connected":
        message = "Backend and database are operational."
    else:
        message = f"Backend is running but database is unavailable. {db_message}"

    return HealthResponse(
        status=backend_status,
        database=db_status,
        service="railway-crossing-api",
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        message=message,
    )


@api_router.get("/db-health", response_model=DbHealthResponse)
async def db_health() -> DbHealthResponse:
    db_status, db_message = _database_status()
    return DbHealthResponse(
        database="PostgreSQL",
        status=db_status,
        message=db_message,
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
