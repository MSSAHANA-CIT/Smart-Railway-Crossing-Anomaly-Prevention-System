# Software Architecture

## Backend (`backend/`)

```
app/
├── main.py           # FastAPI app, CORS, routes
├── api/              # Route modules (REST, WebSocket)
├── core/             # Config, security, dependencies
├── db/               # Session, engine, base
├── models/           # SQLAlchemy ORM models
├── schemas/          # Pydantic request/response models
├── services/         # Business logic (risk engine, alerts)
└── utils/            # Shared helpers
```

### Planned Services (Phase 1+)

| Service | Responsibility |
|---------|----------------|
| `SensorIngestService` | Receive and validate sensor payloads |
| `RiskEngineService` | Compute risk level from multi-sensor data |
| `FalseAlarmService` | Reject spurious triggers using camera + rules |
| `AlertService` | Create, dispatch, and acknowledge alerts |
| `AuthService` | JWT issue and validation |

### Database (Phase 1)

- PostgreSQL via SQLAlchemy 2.x
- Alembic for migrations
- Tables: crossings, sensors, readings, alerts, users (planned)

## Frontend (`frontend/dashboard/`)

```
src/
├── components/       # Reusable UI (cards, buttons, status badges)
├── layouts/          # App shell, navigation
├── pages/            # Route-level views
├── routes/           # React Router configuration
├── i18n/             # i18next setup
├── locales/          # en, hi, ta, ml translation JSON
├── styles/           # Global CSS, Tailwind extensions
└── utils/            # API client, formatters
```

### State Management

- Phase 0: local component state
- Phase 2+: React Query or similar for server state
- WebSocket hook for live monitoring (Phase 2)

### API Integration (Phase 2)

- Axios client with base URL from environment
- Health check on dashboard load

## Firmware

| Project | MCU | Role |
|---------|-----|------|
| `esp32_sensor_controller` | ESP32 | Analog/digital sensors, MQTT/HTTP |
| `esp32s3_ai_camera` | ESP32-S3 | Camera pipeline, edge AI inference |

Firmware communicates with backend over Wi-Fi (HTTP/MQTT — TBD in Phase 3).

## Environment Configuration

| File | Purpose |
|------|---------|
| `backend/.env.example` | API port, CORS, database URL |
| `frontend/dashboard/.env.example` | API base URL (Phase 2) |

## Versioning

- Semantic versioning per `CHANGELOG.md`
- Current: **0.1.0** (Phase 0 foundation)
