import { useTranslation } from 'react-i18next'

const LANGUAGES = [
  { code: 'en', labelKey: 'language.en' },
  { code: 'hi', labelKey: 'language.hi' },
  { code: 'ta', labelKey: 'language.ta' },
  { code: 'ml', labelKey: 'language.ml' },
] as const

export function LanguageSwitcher() {
  const { t, i18n } = useTranslation()

  return (
    <div className="flex flex-col gap-2">
      <span className="text-sm font-semibold uppercase tracking-wide text-slate-400">
        {t('language.label')}
      </span>
      <div className="flex flex-wrap gap-2">
        {LANGUAGES.map(({ code, labelKey }) => {
          const isActive = i18n.language === code
          return (
            <button
              key={code}
              type="button"
              onClick={() => i18n.changeLanguage(code)}
              className={[
                'min-h-[44px] min-w-[88px] rounded-lg border-2 px-4 py-2 text-base font-semibold transition-colors',
                isActive
                  ? 'border-[var(--color-rail-accent)] bg-[var(--color-rail-accent)]/20 text-[var(--color-rail-accent)]'
                  : 'border-[var(--color-rail-border)] bg-[var(--color-rail-panel)] text-slate-200 hover:border-slate-500',
              ].join(' ')}
              aria-pressed={isActive}
            >
              {t(labelKey)}
            </button>
          )
        })}
      </div>
    </div>
  )
}
