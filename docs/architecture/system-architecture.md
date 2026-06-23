# System Architecture

## Overview

The Smart Railway Crossing Anomaly Prevention System is a distributed safety platform with three primary layers:

```
┌─────────────────────────────────────────────────────────────┐
│                    OPERATOR DASHBOARD                        │
│              React + TypeScript + i18next                    │
│         (English, Hindi, Tamil, Malayalam)                   │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP / WebSocket (Phase 1+)
┌─────────────────────────▼───────────────────────────────────┐
│                    BACKEND API                               │
│              FastAPI + PostgreSQL                            │
│    Risk logic · Alerts · Auth · Event storage                │
└─────────────┬───────────────────────────┬───────────────────┘
              │                           │
┌─────────────▼──────────┐   ┌────────────▼──────────────────┐
│  ESP32 Sensor          │   │  ESP32-S3 AI Camera           │
│  Controller            │   │  Controller                   │
│  Ultrasonic·IR·Vibe    │   │  Visual intrusion detection   │
└────────────────────────┘   └───────────────────────────────┘
```

## Data Flow (Planned)

1. Sensors detect proximity, motion, or vibration at crossing zone.
2. ESP32 sensor controller sends readings to backend API.
3. ESP32-S3 camera provides visual confirmation for intrusion events.
4. Backend applies risk-adaptive logic and false alarm rejection.
5. Dashboard displays risk level, alerts, and system health in operator's language.
6. Automated preventive response triggers when threat is confirmed (Phase 5+).

## Phase 0 Scope

- Backend: health and metadata endpoints only
- Frontend: static dashboard with placeholder status cards
- Firmware: folder structure and README placeholders
- No live sensor or camera data

## Security (Planned)

- JWT authentication for dashboard access (Phase 1)
- HTTPS in production
- Role-based access for operators vs administrators

## Reliability

- Health endpoints for monitoring
- Error logging in `docs/error-logs/`
- Daily progress tracking for audit trail
