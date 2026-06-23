# Database Architecture

## Purpose

The PostgreSQL database (`smart_railway_crossing_db`) is the persistent data layer for the Smart Railway Crossing Anomaly Prevention System. It stores reference data, operational metadata, audit trails, and (in future phases) time-series sensor readings and risk assessments.

## Technology

| Component | Role |
|-----------|------|
| PostgreSQL | Primary relational database |
| SQLAlchemy 2.x | ORM and connection management |
| Alembic | Schema versioning and migrations |
| psycopg2 | PostgreSQL driver |

Connection is configured via `DATABASE_URL` in `backend/app/core/config.py`.

## Core Tables (Phase S2)

### `users`

Stores operator and administrator accounts.

| Column | Purpose |
|--------|---------|
| email | Unique login identifier |
| full_name | Display name |
| role | Access level (e.g. operator, admin) |
| is_active | Account enabled flag |

Password fields are deferred to Phase S3 (authentication).

### `devices`

Represents field hardware — ESP32 sensor controllers, ESP32-S3 cameras, and related edge devices.

| Column | Purpose |
|--------|---------|
| device_code | Unique hardware identifier |
| device_type | Controller or sensor category |
| status | online / offline / fault |
| last_seen_at | Last heartbeat timestamp |

### `crossings`

Railway crossing locations managed by the system.

| Column | Purpose |
|--------|---------|
| crossing_code | Unique crossing identifier |
| location, zone, state, country | Geographic metadata |
| status | active / maintenance / disabled |

### `sensor_types`

Reference catalog of supported sensor modalities. Seeded at install time.

| Code | Sensor |
|------|--------|
| IR_ENTRY | IR Entry Beam |
| IR_EXIT | IR Exit Beam |
| ULTRASONIC | Ultrasonic Distance Sensor |
| PIR | PIR Motion Sensor |
| VIBRATION | Vibration Sensor |
| RAIN | Rain Sensor |
| LDR | LDR Light Sensor |
| CAMERA | ESP32-S3 Camera |

### `system_logs`

Operational events from backend services, firmware gateways, and scheduled jobs.

### `audit_logs`

Immutable trail of user and system actions for compliance and debugging.

## Why Each Table Exists

| Table | Rationale |
|-------|-----------|
| `users` | Future authentication and role-based access control |
| `devices` | Map physical hardware to crossings and sensor streams |
| `crossings` | Central entity for risk scoring and alert routing |
| `sensor_types` | Normalize sensor metadata across heterogeneous hardware |
| `system_logs` | Diagnose failures without coupling to application logs |
| `audit_logs` | Safety-critical systems require accountable change history |

## Future Planned Tables

| Table | Phase | Purpose |
|-------|-------|---------|
| `sensor_readings` | S4+ | Time-series sensor measurements |
| `risk_assessments` | S5+ | Computed risk scores per crossing |
| `alerts` | S5+ | Generated warnings and escalations |
| `train_events` | S5+ | Detected train approach/departure events |
| `camera_captures` | S6+ | AI vision inference metadata |
| `user_sessions` | S3 | JWT refresh tokens and session tracking |
| `device_crossing_assignments` | S4 | Many-to-many device ↔ crossing mapping |

## Migration Strategy

- All schema changes go through Alembic under `backend/alembic/versions/`
- Models live in `backend/app/models/` and are registered in `alembic/env.py`
- Migrations are applied with `alembic upgrade head`
- Seed scripts are idempotent and separate from migrations

## Health Monitoring

Database connectivity is verified at runtime via `app/db/init_db.py` and exposed on:

- `GET /api/health` — includes `database: connected | disconnected`
- `GET /api/db-health` — dedicated PostgreSQL status endpoint
