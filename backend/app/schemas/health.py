"""Health and root response schemas."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    environment: str
    message: str


class RootResponse(BaseModel):
    project: str
    short_title: str
    version: str
    status: str
    message: str


class VersionResponse(BaseModel):
    project: str
    short_title: str
    version: str
    environment: str
    api_prefix: str
