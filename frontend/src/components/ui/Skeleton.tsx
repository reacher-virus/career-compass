import React from 'react'
import { cn } from './Button'

export const Skeleton: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({
  className,
  ...props
}) => {
  return (
    <div
      className={cn('animate-pulse rounded-md bg-muted/70 dark:bg-muted/40', className)}
      {...props}
    />
  )
}
