# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2025-06-23

### Added

- Backend foundation created with FastAPI, configuration, CORS, logging, and health endpoints.
- Clean architecture layout under `backend/app/` (`api`, `core`, `schemas`, `db`, `models`, `services`, `utils`).
- pydantic-settings configuration with `PROJECT_NAME`, `APP_VERSION`, `BACKEND_CORS_ORIGINS`, and `API_PREFIX`.
- Structured logging module with timestamp, level, and message output.
- Health routes: `GET /`, `GET /api/health`, `GET /api/version`.
- Phase S1 documentation at `docs/phase-documentation/phase-s1-backend-foundation.md`.

## [0.1.0] - 2025-06-23

### Added

- Initial project foundation created.
- Backend FastAPI starter with health and root endpoints.
- Frontend React + Vite + TypeScript dashboard with multilingual i18n support (English, Hindi, Tamil, Malayalam).
- Firmware folder structure for ESP32 sensor and ESP32-S3 AI camera controllers.
- Hardware documentation templates.
- Phase 0 documentation, daily progress logs, patent notes, and architecture plans.
- GitHub-ready README, PROJECT_PLAN, and .gitignore.
