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

Password hashing and IAM fields were added in Phase S3.

### `devices`

Represents field hardware — ESP32 sensor controllers, ESP32-S3 cameras, and related edge devices. Expanded in Phase S4 with crossing assignment, health status, and JSONB metadata.

| Column | Purpose |
|--------|---------|
| device_code | Unique hardware identifier |
| device_type | Controller or sensor category |
| crossing_id | Optional assigned crossing |
| status / health_status | Administrative and health lifecycle |
| last_seen_at | Last heartbeat timestamp (future live updates) |

### `crossings`

Railway crossing locations managed by the system. Expanded in Phase S4 with hierarchy FKs and operational fields. Legacy geographic columns retained.

| Column | Purpose |
|--------|---------|
| crossing_code | Unique crossing identifier |
| station_id / division_id / zone_id | Organizational hierarchy |
| operational_status / monitoring_status | Administrative monitoring state |
| location, zone, state, country | Legacy geographic metadata |

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
| `users` | Authentication and role-based access control |
| `devices` | Map physical/simulated hardware to crossings and sensor streams |
| `crossings` | Central entity for risk scoring and alert routing |
| `sensor_types` | Normalize sensor metadata across heterogeneous hardware |
| `system_logs` | Diagnose failures without coupling to application logs |
| `audit_logs` | Safety-critical systems require accountable change history |
| `railway_zones` | Top-level railway administrative regions |
| `railway_divisions` | Divisions under zones |
| `railway_stations` | Stations under divisions |
| `sensors` | Planned/registered sensors under devices |
| `staff_assignments` | Staff responsibility links to organizational resources |

## Railway Organization Tables (Phase S4)

### `railway_zones`

Top-level administrative railway regions. Unique `zone_code`. Soft `is_active` deactivation.

### `railway_divisions`

Divisions under a zone (`zone_id` FK, `ondelete=RESTRICT`). Unique `division_code`.

### `railway_stations`

Stations under a division. Optional coordinates and contact fields. Unique `station_code`.

### `sensors`

Sensors under devices with `sensor_type_id` FK to `sensor_types`. Optional crossing, thresholds, provisional `gpio_reference`, JSONB metadata.

### `staff_assignments`

Typed links from users to zone/division/station/crossing/device resources with soft activation and duplicate-active prevention in the service layer.

## Relationships and Indexes

| Relationship | Behavior |
|--------------|----------|
| Zone → Divisions | 1:N, RESTRICT |
| Division → Stations | 1:N, RESTRICT |
| Station → Crossings | 1:N, RESTRICT |
| Crossing → Devices | 1:N, SET NULL |
| Device → Sensors | 1:N, RESTRICT |
| User → Staff Assignments | 1:N, RESTRICT |

Useful indexes: entity codes, parent FKs, operational/device/sensor status and health, `last_seen_at`, active staff assignments.

## Data Ownership

Organizational records are managed by railway administrators. Devices and sensors are administrative registrations until live telemetry arrives. Audit logs record who changed what.

## Future Planned Tables

| Table | Phase | Purpose |
|-------|-------|---------|
| `sensor_readings` | S5+ | Time-series sensor measurements |
| `risk_assessments` | S5+ | Computed risk scores per crossing |
| `alerts` | S5+ | Generated warnings and escalations |
| `train_events` | S5+ | Detected train approach/departure events |
| `camera_captures` | S6+ | AI vision inference metadata |
| `user_sessions` | Future | JWT refresh tokens and session tracking |

> Note: Device↔crossing is modeled as `devices.crossing_id` (one crossing per device at a time).

## Migration Strategy

- All schema changes go through Alembic under `backend/alembic/versions/`
- Models live in `backend/app/models/` and are registered in `alembic/env.py`
- Migrations are applied with `alembic upgrade head`
- Seed scripts are idempotent and separate from migrations
- Phase S4 migration: `c3d4e5f6a7b8_create_railway_organization_and_device_management.py`

## Health Monitoring

Database connectivity is verified at runtime via `app/db/init_db.py` and exposed on:

- `GET /api/health` — includes `database: connected | disconnected`
- `GET /api/db-health` — dedicated PostgreSQL status endpoint
