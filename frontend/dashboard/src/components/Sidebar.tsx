import { NavLink } from 'react-router-dom'
import { useTranslation } from 'react-i18next'

const navItems = [
  { key: 'nav.dashboard', path: '/', icon: '📊' },
  { key: 'nav.liveMonitoring', path: '/monitoring', icon: '📡' },
  { key: 'nav.riskLevel', path: '/risk', icon: '⚠️' },
  { key: 'nav.sensorStatus', path: '/sensors', icon: '🔧' },
  { key: 'nav.alerts', path: '/alerts', icon: '🔔' },
  { key: 'nav.reports', path: '/reports', icon: '📋' },
  { key: 'nav.settings', path: '/settings', icon: '⚙️' },
] as const

export function Sidebar() {
  const { t } = useTranslation()

  return (
    <nav
      className="flex w-full flex-col gap-1 lg:w-64 lg:shrink-0"
      aria-label="Main navigation"
    >
      {navItems.map(({ key, path, icon }) => (
        <NavLink
          key={path}
          to={path}
          end={path === '/'}
          className={({ isActive }) =>
            [
              'flex min-h-[48px] items-center gap-3 rounded-lg px-4 py-3 text-lg font-semibold transition-colors',
              isActive
                ? 'bg-[var(--color-rail-accent)]/20 text-[var(--color-rail-accent)]'
                : 'text-slate-300 hover:bg-[var(--color-rail-panel)] hover:text-white',
            ].join(' ')
          }
        >
          <span aria-hidden="true" className="text-xl">
            {icon}
          </span>
          <span>{t(key)}</span>
        </NavLink>
      ))}
    </nav>
  )
}
