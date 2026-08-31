import React from 'react'
import { cn } from './Button'

interface TabsContextType {
  activeTab: string
  setActiveTab: (val: string) => void
}

const TabsContext = React.createContext<TabsContextType | undefined>(undefined)

export const Tabs: React.FC<{
  defaultValue: string
  value?: string
  onValueChange?: (val: string) => void
  children: React.ReactNode
  className?: string
}> = ({ defaultValue, value, onValueChange, children, className }) => {
  const [active, setActive] = React.useState(value || defaultValue)

  React.useEffect(() => {
    if (value !== undefined) {
      setActive(value)
    }
  }, [value])

  const handleTabChange = (val: string) => {
    setActive(val)
    onValueChange?.(val)
  }

  return (
    <TabsContext.Provider value={{ activeTab: active, setActiveTab: handleTabChange }}>
      <div className={cn('w-full font-sans', className)}>{children}</div>
    </TabsContext.Provider>
  )
}

export const TabsList: React.FC<{
  className?: string
  children: React.ReactNode
}> = ({ className, children }) => (
  <div
    className={cn(
      'inline-flex items-center gap-1 rounded-md bg-surface-card p-1 border border-hairline',
      className
    )}
  >
    {children}
  </div>
)

export const TabsTrigger: React.FC<{
  value: string
  className?: string
  children: React.ReactNode
}> = ({ value, className, children }) => {
  const context = React.useContext(TabsContext)
  if (!context) throw new Error('TabsTrigger must be within Tabs')

  const isActive = context.activeTab === value

  return (
    <button
      type="button"
      onClick={() => context.setActiveTab(value)}
      className={cn(
        'inline-flex items-center justify-center whitespace-nowrap rounded-md px-3.5 py-1.5 text-xs sm:text-sm font-medium transition-all duration-150',
        isActive
          ? 'bg-canvas text-ink shadow-xs font-semibold'
          : 'text-muted hover:text-ink hover:bg-canvas/50',
        className
      )}
    >
      {children}
    </button>
  )
}

export const TabsContent: React.FC<{
  value: string
  className?: string
  children: React.ReactNode
}> = ({ value, className, children }) => {
  const context = React.useContext(TabsContext)
  if (!context) throw new Error('TabsContent must be within Tabs')

  if (context.activeTab !== value) return null

  return <div className={cn('mt-4 focus-visible:outline-none', className)}>{children}</div>
}
