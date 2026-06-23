import { useTranslation } from 'react-i18next'
import { StatusBadge, StatusCard } from '../components/StatusCard'

export function DashboardPage() {
  const { t } = useTranslation()

  return (
    <div className="space-y-6">
      <div>
        <h2 className="mb-2 text-3xl font-bold text-white">{t('nav.dashboard')}</h2>
        <p className="text-lg text-slate-400">{t('app.phaseNote')}</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <StatusCard
          title={t('cards.safetyStatus')}
          description={t('cards.safetyDescription')}
          badge={<StatusBadge label={t('status.safe')} variant="safe" />}
          icon="🛡️"
          accent="green"
        />
        <StatusCard
          title={t('cards.currentRisk')}
          description={t('cards.riskDescription')}
          badge={<StatusBadge label={t('status.warning')} variant="warning" />}
          icon="📈"
          accent="amber"
        />
        <StatusCard
          title={t('cards.systemHealth')}
          description={t('cards.healthDescription')}
          badge={<StatusBadge label={t('cards.operational')} variant="safe" />}
          icon="💚"
          accent="blue"
        />
        <StatusCard
          title={t('cards.alertPreview')}
          description={t('cards.alertDescription')}
          badge={<StatusBadge label={t('cards.noAlerts')} variant="neutral" />}
          icon="🔔"
          accent="gold"
        />
      </div>

      <section
        className="rounded-xl border-2 border-[var(--color-rail-border)] bg-[var(--color-rail-panel)] p-6"
        aria-label="Emergency reference"
      >
        <h3 className="mb-4 text-xl font-bold text-white">{t('status.emergency')}</h3>
        <div className="flex flex-wrap gap-4">
          <StatusBadge label={t('status.safe')} variant="safe" />
          <StatusBadge label={t('status.warning')} variant="warning" />
          <StatusBadge label={t('status.critical')} variant="critical" />
          <StatusBadge label={t('status.emergency')} variant="emergency" />
        </div>
        <p className="mt-4 text-base text-slate-400">
          {t('cards.alertDescription')}
        </p>
      </section>
    </div>
  )
}
