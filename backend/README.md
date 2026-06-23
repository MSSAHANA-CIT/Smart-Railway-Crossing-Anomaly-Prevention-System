# Backend — Smart Railway Crossing Anomaly Prevention System

FastAPI backend for the **Risk-Adaptive Railway Crossing Protection System**. Phase S2 adds PostgreSQL connectivity, SQLAlchemy models, Alembic migrations, database health checks, and sensor type seeding.

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
| PostgreSQL | Primary database |

## Folder Structure

```
backend/
├── alembic/
│   ├── env.py                 # Alembic environment (reads DATABASE_URL)
│   └── versions/              # Migration scripts
├── alembic.ini
├── app/
│   ├── api/routes/health.py   # Root, health, db-health, version routes
│   ├── core/
│   │   ├── config.py          # pydantic-settings configuration
│   │   └── logging.py         # Structured logging setup
│   ├── db/
│   │   ├── base.py            # SQLAlchemy DeclarativeBase
│   │   ├── session.py         # Engine, SessionLocal, get_db
│   │   ├── init_db.py         # Connection test helper
│   │   └── seed.py            # Sensor type seed data
│   ├── models/                # SQLAlchemy models
│   ├── schemas/health.py      # Pydantic response schemas
│   ├── services/              # Business logic (future phases)
│   ├── utils/                 # Shared helpers (future phases)
│   └── main.py                # Application entry point
├── scripts/
│   └── seed_database.py       # CLI seed script
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and set `DATABASE_URL` for your PostgreSQL instance.

Default (Linux/Docker-style install):

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/smart_railway_crossing_db
```

On macOS with Homebrew PostgreSQL, the default superuser is often your system username (no password):

```env
DATABASE_URL=postgresql://YOUR_USERNAME@localhost:5432/smart_railway_crossing_db
```

## Database Setup

Create the PostgreSQL database:

```bash
createdb smart_railway_crossing_db
```

If `createdb` is not on your PATH (Homebrew):

```bash
/opt/homebrew/opt/postgresql@16/bin/createdb smart_railway_crossing_db
```

Run Alembic migrations:

```bash
cd backend
source venv/bin/activate
alembic revision --autogenerate -m "create_core_database_tables"   # when models change
alembic upgrade head
```

Seed reference sensor types:

```bash
python scripts/seed_database.py
```

## Run

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

The API listens on `http://127.0.0.1:8000` by default.

## Available Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Project metadata |
| GET | `/api/health` | Backend + database health (`status`, `database`, `version`, `environment`) |
| GET | `/api/db-health` | Dedicated database health check |
| GET | `/api/version` | Version and environment information |
| GET | `/docs` | Interactive OpenAPI documentation |
| GET | `/redoc` | ReDoc API documentation |

### Health Check URLs

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/api/health`
- `http://127.0.0.1:8000/api/db-health`
- `http://127.0.0.1:8000/docs`

## Core Database Tables

| Table | Purpose |
|-------|---------|
| `users` | Operator and admin accounts (no password yet — Phase S3) |
| `devices` | ESP32 controllers, cameras, and field hardware |
| `crossings` | Railway crossing locations and metadata |
| `sensor_types` | Reference catalog of supported sensor types |
| `system_logs` | Operational system events |
| `audit_logs` | User and system action audit trail |

## Phase S2 Status

- PostgreSQL connection via SQLAlchemy engine and session factory
- Six core models with Alembic initial migration
- Database health checks on `/api/health` and `/api/db-health`
- Idempotent sensor type seed script
- `get_db` FastAPI dependency ready for future routes

**Not included in Phase S2:** authentication, passwords, sensor readings, risk engine APIs.

## Next Backend Phase

Phase S3 will add JWT authentication, password hashing, and user management APIs.
