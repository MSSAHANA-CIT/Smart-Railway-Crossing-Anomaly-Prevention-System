import type { ReactNode } from 'react'
import { useTranslation } from 'react-i18next'
import { LanguageSwitcher } from '../components/LanguageSwitcher'
import { Sidebar } from '../components/Sidebar'

interface AppLayoutProps {
  children: ReactNode
}

export function AppLayout({ children }: AppLayoutProps) {
  const { t } = useTranslation()

  return (
    <div className="min-h-screen bg-[var(--color-rail-dark)]">
      <header className="border-b border-[var(--color-rail-border)] bg-[var(--color-rail-panel)]">
        <div className="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-5 lg:flex-row lg:items-center lg:justify-between lg:px-8">
          <div>
            <div className="mb-1 flex items-center gap-2">
              <span className="text-2xl" aria-hidden="true">
                🚂
              </span>
              <h1 className="text-2xl font-bold text-white lg:text-3xl">
                {t('app.title')}
              </h1>
            </div>
            <p className="text-base text-slate-400 lg:text-lg">{t('app.subtitle')}</p>
          </div>
          <LanguageSwitcher />
        </div>
      </header>

      <div className="mx-auto flex max-w-7xl flex-col gap-6 px-4 py-6 lg:flex-row lg:px-8">
        <aside className="lg:sticky lg:top-6 lg:self-start">
          <Sidebar />
        </aside>
        <main className="min-w-0 flex-1">{children}</main>
      </div>

      <footer className="border-t border-[var(--color-rail-border)] px-4 py-4 text-center text-sm text-slate-500">
        {t('common.version')} · {t('app.phaseNote')}
      </footer>
    </div>
  )
}
