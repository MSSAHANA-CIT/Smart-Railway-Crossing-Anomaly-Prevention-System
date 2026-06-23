# Backend — Smart Railway Crossing Anomaly Prevention System

FastAPI backend for the **Risk-Adaptive Railway Crossing Protection System**. Phase S1 provides a clean architecture foundation with configuration, CORS, structured logging, and health endpoints.

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.9+ | Runtime |
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| Pydantic / pydantic-settings | Validation and environment configuration |
| python-dotenv | `.env` file loading |
| SQLAlchemy / Alembic / psycopg2 | Reserved for Phase S2 database work (not connected yet) |

## Folder Structure

```
backend/
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── health.py      # Root, health, and version routes
│   ├── core/
│   │   ├── config.py          # pydantic-settings configuration
│   │   └── logging.py         # Structured logging setup
│   ├── db/                    # Database session (Phase S2+)
│   ├── models/                # SQLAlchemy models (Phase S2+)
│   ├── schemas/
│   │   └── health.py          # Pydantic response schemas
│   ├── services/              # Business logic (future phases)
│   ├── utils/                 # Shared helpers (future phases)
│   └── main.py                # Application entry point
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

Edit `.env` as needed. Defaults work for local development.

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
| GET | `/` | Project metadata (`project`, `short_title`, `version`, `status`, `message`) |
| GET | `/api/health` | Backend health check (`status`, `service`, `version`, `environment`, `message`) |
| GET | `/api/version` | Version and environment information |
| GET | `/docs` | Interactive OpenAPI documentation |
| GET | `/redoc` | ReDoc API documentation |

## Phase S1 Status

- Clean architecture folder structure in place
- pydantic-settings configuration with CORS support
- Structured logging (timestamp, level, message)
- Health, root, and version endpoints
- Startup and shutdown lifecycle logging
- OpenAPI docs enabled at `/docs`

**Not included in Phase S1:** database models, authentication, sensor APIs.

## Next Backend Phase

Phase S2 will add PostgreSQL connection, SQLAlchemy models, Alembic migrations, and database health checks.
