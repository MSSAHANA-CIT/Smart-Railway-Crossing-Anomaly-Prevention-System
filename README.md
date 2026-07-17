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

*Physical hardware has not been purchased or tested yet. Final GPIO pins are not assigned.*

## Embedded Firmware

Firmware lives in **`firmware/`** and follows a **two-controller architecture**:

| Board | Module folder | Planned role |
|-------|---------------|--------------|
| ESP32 DevKit V1 | `firmware/esp32_sensor_controller/` | Multi-sensor reading, LEDs, buzzer, servo, heartbeat |
| ESP32-S3 AI Camera Board | `firmware/esp32s3_ai_camera/` | Camera capture, visual verification, evidence metadata |

**Hardware status:** No boards tested. ESP32-S3 exact model is **unknown** — pin mapping is pending verification (`docs/embedded/exact-board-verification-checklist.md`).

**Arduino IDE:** Required for compile, upload, and Serial Monitor in the beginner workflow. Cursor is used to write and organize code. See `docs/embedded/arduino-ide-setup-macos.md`.

**Do not assume** the camera board is ESP32-S3-EYE, XIAO Sense, Waveshare, Freenove, ESP32-S3 CAM, or any other specific product until evidence is collected.

## Software Overview

| Layer | Stack |
|-------|-------|
| Backend | Python, FastAPI, SQLAlchemy, PostgreSQL, Pydantic |
| Frontend | React, Vite, TypeScript, Tailwind CSS, i18next |
| Firmware | Arduino C++ (ESP32 / ESP32-S3) — starter workspace only |

## Key Innovation

**INNOV-0001:** Risk-Adaptive Multilingual Railway Crossing Safety Monitoring Platform — combining multi-sensor monitoring, AI-assisted risk analysis, false alarm rejection, automated response, and multilingual field usability for railway operators.

## Languages Supported

- English (en)
- Hindi (hi)
- Tamil (ta)
- Malayalam (ml)

## Current Status

**Version 0.2.0 — Phase S4 Railway Organization and Device Management Complete**

### Software phases

- Phase 0 — Project foundation complete
- Phase S1 — Backend foundation complete
- Phase S2 — Database foundation complete
- Phase S3 — Identity and Access Management complete
- Phase S4 — Railway organization and device management complete
- Phase E0 — Embedded firmware workspace and Arduino docs complete

### Backend (S4)

- Railway zone → division → station → crossing hierarchy APIs
- Device registration, assignment, and sensor registration
- Staff assignment foundation
- Organization hierarchy and crossing overview endpoints
- Soft deactivation; no claim of live hardware connectivity

### Embedded / hardware

- Firmware folder structure and starter sketches created
- Sensors, camera init, and device networking **not implemented**
- Physical upload and hardware testing **not performed** (boards not received)

## Folder Structure

```
EMBEDDED SYSTEM PROJECT/
├── backend/                 # FastAPI application
├── frontend/dashboard/      # React + Vite dashboard
├── firmware/                # ESP32 / ESP32-S3 firmware workspace
│   ├── common/              # Shared headers
│   ├── esp32_sensor_controller/
│   ├── esp32s3_ai_camera/
│   └── examples/
├── hardware/                # Wiring, components, testing plans
├── docs/                    # Progress, architecture, embedded guides
│   └── embedded/            # Arduino IDE + firmware docs
├── reports/                 # Generated reports (future)
├── README.md
├── PROJECT_PLAN.md
└── CHANGELOG.md
```

## Day 1 Setup Note

Phase 0 (23 June 2025) established the complete project skeleton. Phase E0 (17 July 2026) added the embedded firmware workspace. No sensor or AI features are claimed as working on hardware.

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
