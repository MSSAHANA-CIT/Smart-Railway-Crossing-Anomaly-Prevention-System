"""Application configuration via pydantic-settings."""

import getpass
import sys
from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _default_database_url() -> str:
    """Use the current OS user on macOS Homebrew PostgreSQL; postgres elsewhere."""
    if sys.platform == "darwin":
        return (
            f"postgresql://{getpass.getuser()}@localhost:5432/smart_railway_crossing_db"
        )
    return "postgresql://postgres:postgres@localhost:5432/smart_railway_crossing_db"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    PROJECT_NAME: str = "Risk-Adaptive Railway Crossing Protection System"
    PROJECT_SHORT_NAME: str = "Smart Railway Crossing Anomaly Prevention System"
    APP_VERSION: str = "0.1.3"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = _default_database_url()
    SECRET_KEY: str = "change-this-secret-key-before-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
    BACKEND_CORS_ORIGINS: str = (
        "http://localhost:5173,http://127.0.0.1:5173"
    )
    API_PREFIX: str = "/api"

    @model_validator(mode="before")
    @classmethod
    def empty_env_values_use_defaults(cls, data: object) -> object:
        """Treat blank .env entries as unset so field defaults apply."""
        if not isinstance(data, dict):
            return data
        cleaned = dict(data)
        for key, value in list(cleaned.items()):
            if isinstance(value, str) and not value.strip():
                cleaned.pop(key)
        return cleaned

    @property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.BACKEND_CORS_ORIGINS.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()
