import React from 'react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/Card'
import { Badge } from '../ui/Badge'
import { SpikeMark } from '../ui/Icons'

export interface ActionPlanItem {
  week: string
  task: string
}

export interface ActionPlanSectionProps {
  actionPlan: ActionPlanItem[]
  weeklyHours: number
}

export const ActionPlanSection: React.FC<ActionPlanSectionProps> = ({
  actionPlan,
  weeklyHours,
}) => {
  return (
    <Card variant="cream" className="overflow-hidden">
      <CardHeader className="bg-surface-soft border-b border-hairline pb-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <SpikeMark className="h-4 w-4 fill-primary" />
              <CardTitle className="text-2xl md:text-3xl text-ink">
                Tactical Weekly Sprints
              </CardTitle>
            </div>
            <CardDescription>
              Immediate action items paced for your commitment of {weeklyHours} hours / week
            </CardDescription>
          </div>

          <Badge variant="default" className="font-mono text-xs">
            {actionPlan.length} Sprints
          </Badge>
        </div>
      </CardHeader>

      <CardContent className="p-6 md:p-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {actionPlan.map((action, idx) => (
            <div
              key={idx}
              className="p-5 rounded-md border border-hairline bg-canvas space-y-2.5 flex flex-col justify-between"
            >
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-semibold px-2 py-0.5 rounded-md bg-surface-card text-primary border border-hairline">
                  {action.week}
                </span>
                <span className="text-[11px] text-muted-soft">Sprint #{idx + 1}</span>
              </div>
              <p className="text-xs text-ink leading-relaxed flex-1">
                {action.task}
              </p>
              <div className="pt-2 border-t border-hairline text-[11px] text-muted flex items-center gap-1.5">
                <span className="h-1.5 w-1.5 rounded-full bg-success" />
                <span>Verify progress on public portfolio</span>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
