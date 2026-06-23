# Phase 0 — Project Foundation

## What Phase 0 Did

Phase 0 established the complete skeleton for the **Smart Railway Crossing Anomaly Prevention System**. No production features were built — only structure, documentation, and runnable starters for backend and frontend.

### Deliverables

1. **Folder structure** — Separated concerns across backend, frontend, firmware, hardware, and documentation.
2. **Backend starter** — FastAPI with CORS, `/` and `/health` endpoints, environment configuration.
3. **Frontend foundation** — React dashboard with multilingual i18n, navigation, and status cards.
4. **Documentation** — Architecture plans, accessibility guidelines, daily progress, patent register.
5. **GitHub readiness** — README, CHANGELOG, PROJECT_PLAN, .gitignore.

## Why the Folder Structure Was Created

| Folder | Purpose |
|--------|---------|
| `backend/` | API, database logic, business rules — single source of truth for system state |
| `frontend/dashboard/` | Operator-facing UI — must stay simple and multilingual |
| `firmware/` | Embedded code for ESP32 devices — isolated from web stack |
| `hardware/` | Physical components, wiring, and bench testing — reference for assembly |
| `docs/` | Living documentation — progress, errors, patents, architecture |
| `reports/` | Future generated outputs (incident reports, analytics exports) |

Clear separation ensures teams can work in parallel: firmware engineers do not touch React; frontend designers reference `docs/architecture/` for UX decisions.

## Why Multilingual Support Is Planned from the Beginning

Railway employees across India speak different primary languages. Adding translations later causes inconsistent UI, missed strings, and poor operator trust. By integrating **i18next** and locale files in Phase 0:

- Every new UI label must have a translation key from Day 1.
- Language switcher is part of the core layout, not an afterthought.
- Hindi, Tamil, and Malayalam speakers can use the system comfortably alongside English.

## Why Documentation and GitHub Tracking Are Important

This is a safety-critical embedded systems project with potential patent value. From Day 1:

- **Daily progress logs** prove development timeline and decision history.
- **Error logs** capture failures for reproducibility.
- **Patent notes** document innovations before public disclosure.
- **GitHub** provides version control, collaboration, and audit trail for academic or regulatory review.

Phase 0 ensures the project is professional, traceable, and ready for team expansion.

## What Is NOT Done Yet

- Database connection and models
- Sensor integration
- AI camera pipeline
- WebSocket live updates
- JWT authentication
- Production deployment

These are explicitly scoped for Phases 1–6 per `PROJECT_PLAN.md`.
