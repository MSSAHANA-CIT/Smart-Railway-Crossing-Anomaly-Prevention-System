# Accessibility Plan

## Design Goal

The dashboard must be usable by **older railway employees** who may have reduced vision, limited tech experience, or prefer larger touch targets. Accessibility is integrated from Phase 0, not added later.

## Principles

### 1. Large Text Support

- Base font size: **16px minimum** (18px preferred for body on dashboard cards)
- Headings: **20px–28px** with clear hierarchy
- Status labels (Safe, Warning, Critical): **18px+ bold**
- Tailwind classes: `text-base`, `text-lg`, `text-xl` for primary content
- Future: user setting for "Extra Large Text" (Phase 2)

### 2. High Contrast UI

- WCAG AA contrast ratio target (4.5:1 for normal text, 3:1 for large text)
- Dark command-center theme with light text on dark backgrounds for main panels
- Status cards use strong border + background distinction
- Avoid light gray-on-gray for essential information

### 3. Clear Icons

- Icons always paired with text labels (never icon-only navigation)
- Simple, recognizable shapes (shield, bell, gauge)
- SVG icons with sufficient stroke width for visibility

### 4. Language Switching

- Prominent language control in header
- Buttons show language name in native script
- Selected language has clear visual state (border, background)
- See `multilingual-ux-plan.md`

### 5. Simple Navigation

- Fixed sidebar or top nav with 5–7 items maximum in Phase 0
- One primary action per screen area
- No hidden hamburger-only navigation on desktop
- Breadcrumbs or page title always visible

### 6. Color Plus Text Indicators

| Status | Color | Text Label (translated) |
|--------|-------|-------------------------|
| Safe | Green | "Safe" / localized equivalent |
| Warning | Amber | "Warning" |
| Critical | Red | "Critical" |
| Emergency | Red + pulse | "Emergency" |

Never convey status by color alone.

### 7. Touch-Friendly Buttons

- Minimum tap target: **44×44px** (WCAG 2.5.5)
- Adequate spacing between interactive elements (8px+ gap)
- Language switcher buttons: large padded chips

### 8. Older User Usability

- Minimal animations (subtle only; no distracting motion)
- Plain language in all locales
- Consistent layout — cards in same positions every visit
- High-level summary first (safety status, risk level) before details
- No dense tables on landing dashboard

## Keyboard & Screen Reader (Phase 2+)

- Focus visible outlines on all interactive elements
- Semantic HTML: `nav`, `main`, `header`, `button`, `aria-label` where needed
- `lang` attribute updates when language changes
- Skip-to-content link

## Testing

| Check | Method |
|-------|--------|
| Contrast | Browser DevTools, WebAIM contrast checker |
| Font size | Visual review at 100% and 125% browser zoom |
| Touch targets | Manual tap on tablet emulation |
| Language | Switch all four languages; verify completeness |
| Keyboard | Tab through all controls (Phase 2) |

## Phase 0 Implementation

- Tailwind utility classes for size and contrast
- Status cards with text + color badges
- Language switcher with large buttons
- Navigation with text labels on every item

Future phases will add formal WCAG audit and user testing with railway staff representatives.
