# Backend — Smart Railway Crossing Protection System

FastAPI backend for the Risk-Adaptive Railway Crossing Protection System.

## Phase 0 Status

- Health and root endpoints only
- Database not connected yet
- JWT and WebSocket planned for Phase 1

## Run Locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Project metadata |
| GET | `/health` | Service health check |

## Structure

```
app/
├── api/          # Route modules (Phase 1+)
├── core/         # Config, security (Phase 1+)
├── db/           # Database session (Phase 1+)
├── models/       # SQLAlchemy models (Phase 1+)
├── schemas/      # Pydantic schemas (Phase 1+)
├── services/     # Business logic (Phase 1+)
├── utils/        # Helpers
└── main.py       # Application entry point
```
