# Frontend Dashboard

React + Vite + TypeScript dashboard for the Smart Railway Crossing Anomaly Prevention System.

## Phase 0 Features

- Multilingual UI (English, Hindi, Tamil, Malayalam) via i18next
- Professional railway safety themed layout
- Language switcher with persistence
- Dashboard with safety, risk, health, and alert preview cards
- Placeholder pages for future modules

## Run Locally

```bash
npm install
npm run dev
```

Open http://localhost:5173

## Build

```bash
npm run build
npm run preview
```

## Structure

```
src/
├── components/     # LanguageSwitcher, StatusCard, Sidebar
├── layouts/        # AppLayout shell
├── pages/          # Dashboard and placeholder pages
├── routes/         # React Router config
├── i18n/           # i18next setup + locales
├── styles/         # Global CSS + Tailwind
└── utils/          # Helpers (Phase 2+)
```

## Adding Translations

1. Add keys to all four `src/i18n/locales/*/common.json` files
2. Use `t('key')` in components via `useTranslation()`

See `../../docs/architecture/multilingual-ux-plan.md`.
