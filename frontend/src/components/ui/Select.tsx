import React from 'react'
import { cn } from './Button'

export interface SelectOption {
  label: string
  value: string
  sublabel?: string
}

export interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string
  error?: string
  helperText?: string
  options?: Array<SelectOption | string>
}

export const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
  ({ className, label, error, helperText, options = [], id, children, ...props }, ref) => {
    const inputId = id || (label ? label.toLowerCase().replace(/\s+/g, '-') : undefined)

    return (
      <div className="w-full space-y-1.5 font-sans">
        {label && (
          <label htmlFor={inputId} className="text-xs font-medium text-ink">
            {label}
          </label>
        )}
        <div className="relative">
          <select
            id={inputId}
            ref={ref}
            className={cn(
              'flex h-10 w-full appearance-none rounded-md border border-hairline bg-canvas px-3.5 py-2 text-sm text-ink transition-colors focus:border-primary focus:outline-none focus:ring-3 focus:ring-primary/15 disabled:cursor-not-allowed disabled:bg-surface-soft disabled:opacity-60 pr-9',
              error && 'border-error focus:border-error focus:ring-error/15',
              className
            )}
            {...props}
          >
            {options.map((opt, idx) => {
              if (typeof opt === 'string') {
                return (
                  <option key={idx} value={opt} className="bg-canvas text-ink">
                    {opt}
                  </option>
                )
              }
              return (
                <option key={idx} value={opt.value} className="bg-canvas text-ink">
                  {opt.label} {opt.sublabel ? `(${opt.sublabel})` : ''}
                </option>
              )
            })}
            {children}
          </select>
          <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-muted">
            <svg className="h-4 w-4 fill-current" viewBox="0 0 20 20">
              <path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />
            </svg>
          </div>
        </div>
        {helperText && !error && <p className="text-xs text-muted">{helperText}</p>}
        {error && <p className="text-xs font-medium text-error">{error}</p>}
      </div>
    )
  }
)
Select.displayName = 'Select'
