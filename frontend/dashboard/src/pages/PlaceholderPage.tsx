import { useTranslation } from 'react-i18next'

interface PlaceholderPageProps {
  titleKey: string
}

export function PlaceholderPage({ titleKey }: PlaceholderPageProps) {
  const { t } = useTranslation()

  return (
    <div className="rounded-xl border border-[var(--color-rail-border)] bg-[var(--color-rail-panel)] p-8">
      <h2 className="mb-4 text-3xl font-bold text-white">{t(titleKey)}</h2>
      <p className="text-lg text-slate-400">{t('app.phaseNote')}</p>
    </div>
  )
}
