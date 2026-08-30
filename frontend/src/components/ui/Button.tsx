import React from 'react'
import { clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: any[]) {
  return twMerge(clsx(inputs))
}

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?:
    | 'default'
    | 'primary'
    | 'secondary'
    | 'secondary-on-dark'
    | 'coral-inverted'
    | 'outline'
    | 'ghost'
    | 'link'
    | 'destructive'
  size?: 'default' | 'sm' | 'lg' | 'icon'
  isLoading?: boolean
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      className,
      variant = 'default',
      size = 'default',
      isLoading = false,
      children,
      disabled,
      ...props
    },
    ref
  ) => {
    const baseStyles =
      'inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/30 disabled:pointer-events-none disabled:opacity-50 active:scale-[0.99] select-none font-sans'

    const variants = {
      default: 'bg-primary text-white hover:bg-primary-active active:bg-[#964c34]',
      primary: 'bg-primary text-white hover:bg-primary-active active:bg-[#964c34]',
      secondary:
        'bg-canvas text-ink border border-hairline hover:bg-surface-card active:bg-surface-cream-strong',
      'secondary-on-dark':
        'bg-surface-dark-elevated text-on-dark border border-[#33312e] hover:bg-[#2e2b27] active:bg-[#1a1917]',
      'coral-inverted':
        'bg-canvas text-ink hover:bg-surface-card shadow-sm font-medium',
      outline:
        'border border-hairline bg-transparent text-ink hover:bg-surface-card',
      ghost: 'text-body hover:bg-surface-card hover:text-ink',
      link: 'text-primary underline-offset-4 hover:underline p-0 h-auto',
      destructive:
        'bg-error text-white hover:bg-[#aa3838] active:bg-[#942e2e]',
    }

    const sizes = {
      default: 'h-10 px-4 py-2 text-sm',
      sm: 'h-8 rounded-sm px-3 text-xs',
      lg: 'h-11 rounded-md px-6 text-base',
      icon: 'h-9 w-9 p-0',
    }

    return (
      <button
        ref={ref}
        className={cn(baseStyles, variants[variant], sizes[size], className)}
        disabled={disabled || isLoading}
        {...props}
      >
        {isLoading ? (
          <span className="flex items-center gap-2">
            <svg
              className="h-4 w-4 animate-spin"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="3"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
            {children}
          </span>
        ) : (
          children
        )}
      </button>
    )
  }
)

Button.displayName = 'Button'
