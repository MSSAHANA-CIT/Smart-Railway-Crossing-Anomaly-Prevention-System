import type { ReactNode } from 'react'

type StatusVariant = 'safe' | 'warning' | 'critical' | 'emergency' | 'neutral'

const variantStyles: Record<StatusVariant, string> = {
  safe: 'bg-[var(--color-safe)]/15 text-[var(--color-safe)] border-[var(--color-safe)]',
  warning: 'bg-[var(--color-warning)]/15 text-[var(--color-warning)] border-[var(--color-warning)]',
  critical: 'bg-[var(--color-critical)]/15 text-[var(--color-critical)] border-[var(--color-critical)]',
  emergency: 'bg-[var(--color-emergency)]/15 text-[var(--color-emergency)] border-[var(--color-emergency)]',
  neutral: 'bg-slate-500/15 text-slate-300 border-slate-500',
}

interface StatusBadgeProps {
  label: string
  variant?: StatusVariant
}

export function StatusBadge({ label, variant = 'neutral' }: StatusBadgeProps) {
  return (
    <span
      className={[
        'inline-flex items-center rounded-lg border-2 px-4 py-1.5 text-lg font-bold',
        variantStyles[variant],
      ].join(' ')}
    >
      {label}
    </span>
  )
}

interface StatusCardProps {
  title: string
  description: string
  badge?: ReactNode
  icon?: ReactNode
  accent?: 'gold' | 'blue' | 'green' | 'amber' | 'red'
}

const accentBorder: Record<NonNullable<StatusCardProps['accent']>, string> = {
  gold: 'border-l-[var(--color-rail-accent)]',
  blue: 'border-l-blue-500',
  green: 'border-l-[var(--color-safe)]',
  amber: 'border-l-[var(--color-warning)]',
  red: 'border-l-[var(--color-critical)]',
}

export function StatusCard({
  title,
  description,
  badge,
  icon,
  accent = 'gold',
}: StatusCardProps) {
  return (
    <article
      className={[
        'rounded-xl border border-[var(--color-rail-border)] border-l-4 bg-[var(--color-rail-panel)] p-6 shadow-lg',
        accentBorder[accent],
      ].join(' ')}
    >
      <div className="mb-4 flex items-start justify-between gap-4">
        <div className="flex items-center gap-3">
          {icon && (
            <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-lg bg-[var(--color-rail-dark)] text-2xl">
              {icon}
            </div>
          )}
          <h2 className="text-xl font-bold text-white">{title}</h2>
        </div>
        {badge}
      </div>
      <p className="text-lg leading-relaxed text-slate-300">{description}</p>
    </article>
  )
}
