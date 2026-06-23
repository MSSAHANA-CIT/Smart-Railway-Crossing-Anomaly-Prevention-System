# Smart Railway Crossing Anomaly Prevention System

**Full Title:** Risk-Adaptive Railway Crossing Protection System Using Multi-Sensor Intrusion Analysis and Automated Preventive Response with False Alarm Rejection Engine

---

## Problem Statement

Unmanned and poorly monitored railway crossings in India pose serious safety risks. Animals, vehicles, and pedestrians can enter crossing zones without timely detection. Existing systems often lack multilingual interfaces, produce false alarms, and are difficult for field staff — including older employees — to operate reliably.

## Objectives

1. Monitor railway crossings using multi-sensor intrusion analysis.
2. Provide risk-adaptive alerts with false alarm rejection.
3. Enable automated preventive response when threats are confirmed.
4. Deliver a simple, multilingual dashboard for Indian railway employees.
5. Build a documented, GitHub-tracked, production-ready architecture from Day 1.

## Hardware Overview

| Component | Role |
|-----------|------|
| ESP32 Sensor Controller | Ultrasonic, IR, vibration sensors; local alarms |
| ESP32-S3 AI Camera Controller | Visual intrusion detection; false alarm rejection |
| PostgreSQL Database | Persistent storage for events and configuration |

*Hardware integration is planned for later phases. Phase 0 establishes structure only.*

## Software Overview

| Layer | Stack |
|-------|-------|
| Backend | Python, FastAPI, SQLAlchemy, PostgreSQL, Pydantic |
| Frontend | React, Vite, TypeScript, Tailwind CSS, i18next |
| Firmware | Arduino C++ (ESP32 / ESP32-S3) |

## Key Innovation

**INNOV-0001:** Risk-Adaptive Multilingual Railway Crossing Safety Monitoring Platform — combining multi-sensor monitoring, AI-assisted risk analysis, false alarm rejection, automated response, and multilingual field usability for railway operators.

## Languages Supported

- English (en)
- Hindi (hi)
- Tamil (ta)
- Malayalam (ml)

## Current Status

**Version 0.1.0 — Phase 0 Complete**

- Project foundation and folder structure created
- Backend health and root API endpoints available
- Frontend dashboard with language switcher and status cards
- Documentation, architecture plans, and patent register initialized
- Sensors, AI, and database **not yet integrated**

## Folder Structure

```
EMBEDDED SYSTEM PROJECT/
├── backend/                 # FastAPI application
├── frontend/dashboard/      # React + Vite dashboard
├── firmware/                # ESP32 firmware projects
├── hardware/                # Wiring, components, testing plans
├── docs/                    # Progress logs, architecture, patent notes
├── reports/                 # Generated reports (future)
├── README.md
├── PROJECT_PLAN.md
└── CHANGELOG.md
```

## Day 1 Setup Note

Phase 0 (23 June 2025) established the complete project skeleton. No sensor or AI features are claimed as working. Next steps: initialize Git repository, run backend and frontend locally, and begin Phase 1 backend core development.

## Quick Start

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend/dashboard
npm install
npm run dev
```

API docs: http://localhost:8000/docs  
Dashboard: http://localhost:5173

## License

TBD — project documentation phase.
