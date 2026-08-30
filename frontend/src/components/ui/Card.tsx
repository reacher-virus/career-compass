import React from 'react'
import { cn } from './Button'

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'cream' | 'canvas' | 'dark' | 'dark-elevated' | 'coral'
}

export const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, variant = 'cream', ...props }, ref) => {
    const variants = {
      cream: 'bg-surface-card text-ink border border-hairline',
      canvas: 'bg-canvas text-ink border border-hairline',
      dark: 'bg-[#181715] text-[#faf9f5] border border-[#262420]',
      'dark-elevated': 'bg-[#252320] text-[#faf9f5] border border-[#33312e]',
      coral: 'bg-primary text-white border-transparent',
    }

    return (
      <div
        ref={ref}
        className={cn(
          'rounded-lg transition-colors duration-150',
          variants[variant],
          className
        )}
        {...props}
      />
    )
  }
)
Card.displayName = 'Card'

export const CardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn('flex flex-col space-y-1.5 p-6 md:p-8', className)} {...props} />
))
CardHeader.displayName = 'CardHeader'

export const CardTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h3
    ref={ref}
    className={cn(
      'font-serif text-xl md:text-2xl font-normal tracking-[-0.02em] leading-tight text-inherit',
      className
    )}
    {...props}
  />
))
CardTitle.displayName = 'CardTitle'

export const CardDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn('text-sm text-muted leading-relaxed', className)}
    {...props}
  />
))
CardDescription.displayName = 'CardDescription'

export const CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn('p-6 md:p-8 pt-0 md:pt-0 text-inherit', className)} {...props} />
))
CardContent.displayName = 'CardContent'

export const CardFooter = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn('flex items-center p-6 md:p-8 pt-0 md:pt-0', className)}
    {...props}
  />
))
CardFooter.displayName = 'CardFooter'
