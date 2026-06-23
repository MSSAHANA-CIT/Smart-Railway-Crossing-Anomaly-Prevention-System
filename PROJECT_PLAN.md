# Project Plan

## Smart Railway Crossing Anomaly Prevention System

**Full Title:** Risk-Adaptive Railway Crossing Protection System Using Multi-Sensor Intrusion Analysis and Automated Preventive Response with False Alarm Rejection Engine

---

## Vision

Design a railway crossing protection platform for railway employees in India — simple, multilingual, accessible, and reliable for field operators including older staff who may not be highly technical.

---

## Phases

### Phase 0 — Project Foundation (Current)

- [x] Folder structure (backend, frontend, firmware, hardware, docs)
- [x] FastAPI backend starter (health, root endpoints)
- [x] React dashboard foundation with i18next (en, hi, ta, ml)
- [x] Documentation, changelog, patent register, accessibility plan
- [x] GitHub-ready structure

### Phase 1 — Backend Core

- Database models and PostgreSQL connection
- SQLAlchemy + Alembic migrations
- JWT authentication
- Sensor data ingestion API stubs
- WebSocket foundation for live updates

### Phase 2 — Frontend Dashboard

- Live monitoring views
- Risk level visualization (Recharts)
- Alert management UI
- Settings and user preferences
- Axios integration with backend

### Phase 3 — Firmware (ESP32 Sensor Controller)

- Ultrasonic, IR, vibration sensor reading
- MQTT/HTTP data transmission
- Local alarm triggers
- Power and connectivity handling

### Phase 4 — Firmware (ESP32-S3 AI Camera)

- Camera capture pipeline
- On-device or edge AI intrusion detection
- False alarm rejection signals
- Integration with sensor controller

### Phase 5 — Integration & Testing

- End-to-end sensor → backend → dashboard flow
- Hardware bench testing
- Field simulation scenarios
- False alarm rejection tuning

### Phase 6 — Deployment & Documentation

- Production deployment guides
- Operator training materials (multilingual)
- Final reports and patent documentation

---

## Tech Stack Summary

| Layer      | Technologies                                      |
|------------|---------------------------------------------------|
| Backend    | Python, FastAPI, SQLAlchemy, PostgreSQL, Pydantic |
| Frontend   | React, Vite, TypeScript, Tailwind, i18next        |
| Firmware   | Arduino C++, ESP32, ESP32-S3                      |
| Database   | PostgreSQL                                        |
| Docs       | Markdown                                          |

---

## Success Criteria

1. Railway employees can operate the dashboard in their preferred language.
2. System provides clear risk levels with color + text indicators.
3. Multi-sensor data feeds into risk-adaptive logic with false alarm rejection.
4. Automated preventive responses trigger when intrusion is confirmed.
5. Full documentation and version control from Day 1.

---

## Timeline (Estimated)

| Phase | Duration (est.) |
|-------|-----------------|
| 0     | 1 week          |
| 1–2   | 3–4 weeks       |
| 3–4   | 4–6 weeks       |
| 5     | 2–3 weeks       |
| 6     | 1–2 weeks       |

*Timeline is indicative and will be updated in daily progress logs.*
