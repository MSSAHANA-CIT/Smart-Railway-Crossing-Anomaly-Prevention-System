# Multilingual UX Plan

## Why Multilingual Support Is Needed

Indian Railways employs staff across diverse linguistic regions. A crossing protection dashboard used in Tamil Nadu, Kerala, Maharashtra, or North India must be operable without forcing English literacy. Misunderstood alerts in safety-critical systems can delay response and increase accident risk.

Multilingual support is a **safety requirement**, not a cosmetic feature.

## Supported Languages

| Code | Language | Script | Primary Users (example regions) |
|------|----------|--------|--------------------------------|
| `en` | English | Latin | Pan-India default, technical staff |
| `hi` | Hindi | Devanagari | North and Central India |
| `ta` | Tamil | Tamil | Tamil Nadu |
| `ml` | Malayalam | Malayalam | Kerala |

## Translation File Structure

```
frontend/dashboard/src/i18n/locales/
├── en/common.json
├── hi/common.json
├── ta/common.json
└── ml/common.json
```

Each locale file uses nested keys for namespaces:

```json
{
  "nav": { "dashboard": "...", "alerts": "..." },
  "status": { "safe": "...", "critical": "..." },
  "app": { "title": "..." }
}
```

## i18next Integration

- Library: `i18next` + `react-i18next`
- Language persisted in `localStorage` key `railway-crossing-lang`
- Language switcher in header — large, labeled buttons with native script names
- Fallback language: English (`en`)

## Adding a New Language

1. Create `src/i18n/locales/<code>/common.json` with all keys from `en/common.json`
2. Register locale in `src/i18n/index.ts`
3. Add option to `LanguageSwitcher` component
4. Test all pages for text overflow (some scripts need more horizontal space)
5. Update this document and root `README.md`

## UX Principles for Railway Employees

1. **Native script labels** — Show "हिन्दी" not just "Hindi" in the switcher.
2. **Short, direct phrases** — Avoid technical jargon; use terms staff already know.
3. **Consistent terminology** — Same word for "Alert" everywhere in a given language.
4. **Large readable text** — Minimum 16px body; headings 20px+ (see accessibility plan).
5. **Color + text** — Risk levels always show word + color (e.g., "Critical" + red badge).
6. **No reliance on icons alone** — Every icon has a text label.

## Phase 0 Coverage

Initial translations include navigation, status labels, and app title. New screens in Phase 2+ must add keys to all four locale files before merge.

## Testing Checklist

- [ ] Switch language on dashboard — all visible text updates
- [ ] Refresh page — language preference persists
- [ ] Hindi/Tamil/Malayalam render correctly (UTF-8, web fonts)
- [ ] No truncated text in navigation at 1280px width
- [ ] Screen reader announces language-appropriate content (Phase 2+)
