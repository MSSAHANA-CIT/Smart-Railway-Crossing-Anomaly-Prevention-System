# Phase S2 — Database Foundation

## Objective

Establish the PostgreSQL database foundation for the Smart Railway Crossing backend using SQLAlchemy ORM, Alembic migrations, core reference tables, database health checks, and sensor type seed data — without authentication, sensor readings, or risk engine APIs.

## Database Design

Database name: `smart_railway_crossing_db`

Connection string (default):

```
postgresql://postgres:postgres@localhost:5432/smart_railway_crossing_db
```

The backend reads `DATABASE_URL` from environment via `pydantic-settings` in `app/core/config.py`.

## Tables Created

| Table | Model File | Key Fields |
|-------|------------|------------|
| `users` | `app/models/user.py` | email, full_name, role, is_active |
| `devices` | `app/models/device.py` | device_code, device_name, device_type, status |
| `crossings` | `app/models/crossing.py` | crossing_code, crossing_name, location, zone, state |
| `sensor_types` | `app/models/sensor_type.py` | name, code, description, unit |
| `system_logs` | `app/models/system_log.py` | level, message, source |
| `audit_logs` | `app/models/audit_log.py` | actor, action, entity_type, entity_id |

All tables use integer primary keys, string fields where appropriate, boolean flags, and `created_at` / `updated_at` timestamps with `server_default=func.now()`.

## Migration Setup

- Alembic initialized under `backend/alembic/`
- `alembic.ini` configured; `alembic/env.py` reads `DATABASE_URL` from settings
- `target_metadata` points to `Base.metadata` with all models registered
- Initial migration: `create_core_database_tables`

Commands:

```bash
createdb smart_railway_crossing_db
alembic revision --autogenerate -m "create_core_database_tables"
alembic upgrade head
```

## Seed Data

`app/db/seed.py` defines eight sensor types:

| Name | Code |
|------|------|
| IR Entry Beam | IR_ENTRY |
| IR Exit Beam | IR_EXIT |
| Ultrasonic Distance Sensor | ULTRASONIC |
| PIR Motion Sensor | PIR |
| Vibration Sensor | VIBRATION |
| Rain Sensor | RAIN |
| LDR Light Sensor | LDR |
| ESP32-S3 Camera | CAMERA |

Run via:

```bash
python scripts/seed_database.py
```

The script is idempotent — existing codes are skipped.

## Health Check Endpoints

| Endpoint | Returns |
|----------|---------|
| `GET /api/health` | Backend `status`, `database` (connected/disconnected), `version`, `environment` |
| `GET /api/db-health` | `database`, `status`, `message` |

If PostgreSQL is unavailable, endpoints still respond safely with `disconnected` status and a clear error message.

## Testing Procedure

1. Install dependencies and configure `.env`
2. Create database: `createdb smart_railway_crossing_db`
3. Run migrations: `alembic upgrade head`
4. Seed sensor types: `python scripts/seed_database.py`
5. Start server: `uvicorn app.main:app --reload`
6. Verify endpoints:

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/api/health
curl http://127.0.0.1:8000/api/db-health
```

Open `http://127.0.0.1:8000/docs` for interactive API documentation.

## Expected Result

**`/api/health` (database connected):**

```json
{
  "status": "healthy",
  "database": "connected",
  "service": "railway-crossing-api",
  "version": "0.1.2",
  "environment": "development",
  "message": "Backend and database are operational."
}
```

**`/api/db-health` (database connected):**

```json
{
  "database": "PostgreSQL",
  "status": "connected",
  "message": "Database connection successful"
}
```

## Current Status

Phase S2 complete. PostgreSQL foundation, six core tables, Alembic migrations, health checks, and sensor type seeding are in place.

## Next Phase

Phase S3 — Authentication: JWT tokens, password hashing, user registration/login, and protected routes.
