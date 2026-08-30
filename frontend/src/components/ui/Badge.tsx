import React from 'react'
import { cn } from './Button'

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?:
    | 'default'
    | 'cream'
    | 'coral'
    | 'teal'
    | 'amber'
    | 'dark'
    | 'success'
    | 'destructive'
    | 'outline'
    | 'secondary'
    | 'info'
    | 'warning'
}

export const Badge: React.FC<BadgeProps> = ({
  className,
  variant = 'default',
  ...props
}) => {
  const variants = {
    default: 'bg-surface-card text-ink border border-hairline',
    cream: 'bg-surface-card text-ink border border-hairline',
    coral: 'bg-primary text-white border-transparent',
    teal: 'bg-accent-teal/15 text-[#246b5e] dark:text-[#5db8a6] border border-accent-teal/30',
    amber: 'bg-accent-amber/20 text-[#8c5214] dark:text-[#e8a55a] border border-accent-amber/40',
    dark: 'bg-surface-dark-elevated text-on-dark border border-[#33312e]',
    success: 'bg-success/15 text-[#226634] dark:text-[#5db872] border border-success/30',
    destructive: 'bg-error/15 text-[#992626] dark:text-[#f87171] border border-error/30',
    outline: 'bg-transparent text-body border border-hairline',
    secondary: 'bg-surface-soft text-body border border-hairline',
    info: 'bg-accent-teal/15 text-[#246b5e] dark:text-[#5db8a6] border border-accent-teal/30',
    warning: 'bg-accent-amber/20 text-[#8c5214] dark:text-[#e8a55a] border border-accent-amber/40',
  }

  return (
    <div
      className={cn(
        'inline-flex items-center rounded-full px-3 py-1 text-xs font-medium tracking-normal transition-colors select-none font-sans',
        variants[variant],
        className
      )}
      {...props}
    />
  )
}
