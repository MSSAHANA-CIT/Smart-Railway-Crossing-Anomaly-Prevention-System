# Backend — Smart Railway Crossing Anomaly Prevention System

FastAPI backend for the **Risk-Adaptive Railway Crossing Protection System**. Phase S4 adds railway organization hierarchy, device registration, sensor registration, staff assignments, and organization overview APIs on top of the S1–S3 foundation.

**Prototype note:** Demonstration records are fictional. This system is not integrated with Indian Railways production systems.

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.9+ | Runtime |
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| Pydantic / pydantic-settings | Validation and environment configuration |
| python-dotenv | `.env` file loading |
| SQLAlchemy 2.x | ORM and database models |
| Alembic | Schema migrations |
| psycopg2-binary | PostgreSQL driver |
| python-jose | JWT token creation and validation |
| passlib + bcrypt | Password hashing |
| email-validator | Email field validation |
| PostgreSQL | Primary database |

## Folder Structure

```
backend/
├── alembic/
│   ├── env.py
│   └── versions/
├── app/
│   ├── api/
│   │   ├── dependencies.py
│   │   └── routes/
│   │       ├── auth.py
│   │       ├── health.py
│   │       ├── users.py
│   │       ├── railway_zones.py
│   │       ├── railway_divisions.py
│   │       ├── railway_stations.py
│   │       ├── railway_crossings.py
│   │       ├── devices.py
│   │       ├── sensors.py
│   │       ├── staff_assignments.py
│   │       └── organization.py
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   │   ├── pagination.py
│   │   └── validation.py
│   └── main.py
├── scripts/
│   ├── create_admin_user.py
│   ├── seed_database.py
│   └── seed_railway_organization.py
├── tests/
│   └── api/
└── requirements.txt
```

## Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and set `DATABASE_URL`, `SECRET_KEY`, and other values.

## IAM Overview

Phase S3 provides enterprise-ready authentication for railway employees:

- **Password security** — bcrypt hashing via passlib; plain-text passwords are never stored
- **JWT access tokens** — signed with `SECRET_KEY`, include `sub`, `user_id`, `role`, `exp`
- **Role-based access** — eight roles from `SUPER_ADMIN` to `VIEWER`
- **User status** — `ACTIVE`, `INACTIVE`, `SUSPENDED`, `PENDING`
- **Protected routes** — Bearer token required on sensitive endpoints
- **Audit logging** — login, user creation, profile views, enable/disable, token validation

## Roles

| Role | Description |
|------|-------------|
| `SUPER_ADMIN` | Full system administration |
| `RAILWAY_ADMIN` | Railway-wide user and system management |
| `DIVISION_ADMIN` | Division-level administration |
| `STATION_MASTER` | Station-level operations |
| `CROSSING_OPERATOR` | Level crossing operator |
| `MAINTENANCE_ENGINEER` | Field maintenance staff |
| `SAFETY_INSPECTOR` | Safety inspection personnel |
| `VIEWER` | Read-only access |

## Database Setup

```bash
createdb smart_railway_crossing_db
cd backend
source venv/bin/activate
alembic upgrade head
python scripts/seed_database.py
python scripts/seed_railway_organization.py   # optional fictional DEMO hierarchy
```

## Phase S4 Models

| Model | Table | Notes |
|-------|-------|-------|
| RailwayZone | `railway_zones` | Top-level region |
| RailwayDivision | `railway_divisions` | Under a zone |
| RailwayStation | `railway_stations` | Under a division |
| RailwayCrossing | `crossings` | Expanded Phase S2 table |
| Device | `devices` | Expanded; optional crossing assignment |
| Sensor | `sensors` | Under device + sensor type |
| StaffAssignment | `staff_assignments` | Typed user↔resource link |

## Create First Admin User

When no users exist, create the bootstrap `SUPER_ADMIN`:

```bash
ADMIN_EMAIL=admin@example.com \
ADMIN_FULL_NAME="System Admin" \
ADMIN_PASSWORD="Admin@12345" \
python scripts/create_admin_user.py
```

Or set `ADMIN_EMAIL`, `ADMIN_FULL_NAME`, and `ADMIN_PASSWORD` in `.env`.

## Run

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

API: `http://127.0.0.1:8000`  
Swagger UI: `http://127.0.0.1:8000/docs`

## Auth Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/auth/login` | No | Login with email/password; returns JWT |
| GET | `/api/auth/me` | Bearer | Current logged-in user |
| POST | `/api/auth/verify-token` | Bearer | Validate token and return user info |

### Test Login

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"Admin@12345"}'
```

### Test Current User

```bash
curl http://127.0.0.1:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## User Endpoints

| Method | Path | Auth | Allowed Roles |
|--------|------|------|---------------|
| POST | `/api/users` | Optional* | Bootstrap or `SUPER_ADMIN` |
| GET | `/api/users` | Bearer | `SUPER_ADMIN`, `RAILWAY_ADMIN` |
| GET | `/api/users/{user_id}` | Bearer | Admins or self |
| PATCH | `/api/users/{user_id}/disable` | Bearer | `SUPER_ADMIN`, `RAILWAY_ADMIN` |
| PATCH | `/api/users/{user_id}/enable` | Bearer | `SUPER_ADMIN`, `RAILWAY_ADMIN` |

\* `POST /api/users` is open only when the database has zero users (first admin bootstrap).

## Railway Organization Endpoints (S4)

| Area | Base path | Key actions |
|------|-----------|-------------|
| Zones | `/api/railway/zones` | create, list, get, patch, activate, deactivate |
| Divisions | `/api/railway/divisions` | create, list, get, patch, activate, deactivate |
| Stations | `/api/railway/stations` | create, list, get, patch, activate, deactivate |
| Crossings | `/api/railway/crossings` | CRUD-like + operational/monitoring status |
| Hierarchy | `/api/railway/hierarchy` | summary tree (devices/sensors optional) |
| Overview | `/api/railway/crossings/{id}/overview` | crossing + parents + devices + counts |

## Device and Sensor Endpoints (S4)

| Area | Base path | Key actions |
|------|-----------|-------------|
| Devices | `/api/devices` | register, assign, unassign, status, health, sensors |
| Sensors | `/api/sensors` | register, status, health, activate/deactivate |
| Staff | `/api/staff-assignments` | create, list, update, activate/deactivate |
| User assignments | `/api/users/{id}/assignments` | list assignments for a user |

List endpoints use `page` (default 1) and `page_size` (default 20, max 100).

## Using JWT in Swagger (including S4)

1. Open `http://127.0.0.1:8000/docs`
2. Call `POST /api/auth/login` with SUPER_ADMIN credentials
3. Copy the `access_token`
4. Click **Authorize** → `Bearer <token>`
5. Create a DEMO zone → division → station → crossing
6. Register two devices (ESP32 controller + ESP32-S3 camera), assign to the crossing
7. Register sensors; create a staff assignment
8. Call `/api/railway/crossings/{id}/overview` and `/api/railway/hierarchy`
9. Deactivate/reactivate a record; confirm audit entries in `audit_logs`

## Health Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Project metadata |
| GET | `/api/health` | Backend + database health |
| GET | `/api/db-health` | Database health check |
| GET | `/api/version` | Version information |

## Tests

```bash
cd backend
source venv/bin/activate
pytest tests/ -v
```

## Phase Status

**S3 (complete):** JWT auth, password hashing, roles, user APIs, IAM audit logging.

**S4 (complete):** Railway hierarchy, device/sensor registration, staff assignments, organization overview, pagination, soft deactivation, role-protected management APIs, Alembic migration `c3d4e5f6a7b8`, demo seed script.

**Not included in S4:** live sensor ingestion, WebSockets, AI risk scoring, FARE, camera uploads, firmware OTA, assignment-scoped multi-tenant authorization, frontend organization screens.

## Next Backend Phase

Likely sensor telemetry ingestion and device heartbeat / live monitoring APIs.
