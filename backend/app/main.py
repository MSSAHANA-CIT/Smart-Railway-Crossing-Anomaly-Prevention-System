"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    description=(
        "Risk-Adaptive Railway Crossing Protection System — "
        "Phase 0 foundation. Sensors and AI not yet integrated."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "project": settings.PROJECT_NAME,
        "short_title": settings.PROJECT_SHORT_NAME,
        "status": "foundation",
        "version": settings.API_VERSION,
        "phase": "0",
        "message": "Project foundation active. Full features in development.",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "railway-crossing-api",
        "version": settings.API_VERSION,
        "environment": settings.ENVIRONMENT,
    }
