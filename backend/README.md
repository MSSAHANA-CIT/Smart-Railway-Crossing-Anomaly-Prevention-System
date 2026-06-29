# Backend — Smart Railway Crossing Anomaly Prevention System

FastAPI backend for the **Risk-Adaptive Railway Crossing Protection System**. Phase S3 adds Identity and Access Management (IAM) with JWT authentication, password hashing, role-based access control, protected routes, and audit logging.

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
│   │   ├── dependencies.py      # get_current_user, require_roles
│   │   └── routes/
│   │       ├── auth.py          # Login, /me, verify-token
│   │       ├── health.py
│   │       └── users.py         # User CRUD and enable/disable
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── security.py          # Password hashing and JWT
│   ├── db/
│   ├── models/
│   │   ├── user.py
│   │   └── audit_log.py
│   ├── schemas/
│   │   ├── auth.py
│   │   └── user.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   └── audit_service.py
│   └── main.py
├── scripts/
│   ├── create_admin_user.py
│   └── seed_database.py
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
```

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

## Using JWT in Swagger

1. Open `http://127.0.0.1:8000/docs`
2. Call `POST /api/auth/login` with email and password
3. Copy the `access_token` from the response
4. Click **Authorize** (top right)
5. Enter: `Bearer <paste_access_token_here>`
6. Call protected endpoints (`/api/auth/me`, `/api/users`, etc.)

## Health Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Project metadata |
| GET | `/api/health` | Backend + database health |
| GET | `/api/db-health` | Database health check |
| GET | `/api/version` | Version information |

## Phase S3 Status

- JWT authentication with password hashing (bcrypt)
- User model with IAM fields (`password_hash`, `status`, `last_login_at`, `failed_login_attempts`)
- Role-based access control on user management routes
- Audit logging for IAM actions
- Admin bootstrap script
- Alembic migration `add_identity_access_management_fields`

**Not included in Phase S3:** refresh tokens, password reset, frontend login UI, device management, sensor APIs.

## Next Backend Phase

Phase S4 will add device management APIs and sensor data ingestion.
