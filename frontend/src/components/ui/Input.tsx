import React from 'react'
import { cn } from './Button'

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  helperText?: string
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type = 'text', label, error, helperText, id, ...props }, ref) => {
    const inputId = id || (label ? label.toLowerCase().replace(/\s+/g, '-') : undefined)

    return (
      <div className="w-full space-y-1.5 font-sans">
        {label && (
          <label
            htmlFor={inputId}
            className="text-xs font-medium text-ink flex items-center justify-between"
          >
            <span>{label}</span>
          </label>
        )}
        <input
          id={inputId}
          type={type}
          ref={ref}
          className={cn(
            'flex h-10 w-full rounded-md border border-hairline bg-canvas px-3.5 py-2 text-sm text-ink placeholder:text-muted-soft transition-colors focus:border-primary focus:outline-none focus:ring-3 focus:ring-primary/15 disabled:cursor-not-allowed disabled:bg-surface-soft disabled:opacity-60',
            error && 'border-error focus:border-error focus:ring-error/15',
            className
          )}
          {...props}
        />
        {helperText && !error && <p className="text-xs text-muted">{helperText}</p>}
        {error && <p className="text-xs font-medium text-error">{error}</p>}
      </div>
    )
  }
)
Input.displayName = 'Input'
