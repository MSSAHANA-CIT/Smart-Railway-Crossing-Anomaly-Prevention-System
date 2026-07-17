# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.4] - 2026-07-17

### Added

- Embedded development foundation (Phase E0): firmware workspace for ESP32 DevKit V1 and ESP32-S3 AI Camera Board.
- ESP32 sensor controller starter sketch (Serial identity + non-blocking heartbeat).
- ESP32-S3 camera controller starter sketch (no camera init; board model pending verification).
- Shared firmware headers: communication protocol concepts, telemetry data model, safe constants.
- Arduino IDE setup documentation for macOS and ESP32 board support guide.
- Exact-board verification checklist and embedded development workflow.
- Firmware security guidelines and hardware-to-backend integration plan.
- Beginner examples: basic Serial test and Wi-Fi connection template (placeholders only).
- Phase E0 documentation and embedded daily progress log.
- `.gitignore` entries for firmware secrets and build artifacts (`device_config.h`, `*.bin`, `*.elf`, `*.map`).

## [0.1.3] - 2025-06-29

### Added

- Identity and Access Management foundation with password hashing, JWT authentication, user roles, protected routes, and audit logging.
- Security module (`app/core/security.py`) with bcrypt password hashing and JWT create/decode utilities.
- Auth service, user service, and audit service for login, user management, and IAM audit trail.
- Auth routes: `POST /api/auth/login`, `GET /api/auth/me`, `POST /api/auth/verify-token`.
- User routes: `POST /api/users`, `GET /api/users`, `GET /api/users/{user_id}`, `PATCH /api/users/{user_id}/disable`, `PATCH /api/users/{user_id}/enable`.
- FastAPI dependencies: `get_current_user`, `require_roles`.
- User model IAM fields: `password_hash`, `status`, `last_login_at`, `failed_login_attempts`.
- Eight railway roles and four user status values.
- Alembic migration `add_identity_access_management_fields`.
- Admin bootstrap script (`scripts/create_admin_user.py`).
- Phase S3 documentation.

## [0.1.2] - 2025-06-23

### Added

- PostgreSQL database foundation with SQLAlchemy, Alembic migrations, core models, database health checks, and sensor type seed foundation.
- SQLAlchemy models: `users`, `devices`, `crossings`, `sensor_types`, `system_logs`, `audit_logs`.
- Database session layer (`engine`, `SessionLocal`, `get_db` dependency).
- Alembic initial migration `create_core_database_tables`.
- `GET /api/db-health` endpoint for dedicated PostgreSQL status.
- Extended `GET /api/health` with `database` connected/disconnected status.
- Idempotent sensor type seed script (`scripts/seed_database.py`).
- Phase S2 documentation and database architecture plan.

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
