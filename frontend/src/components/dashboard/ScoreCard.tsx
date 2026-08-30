import React, { useState } from 'react'
import { ChevronDown, ChevronUp, Check, AlertCircle } from 'lucide-react'
import { Card, CardContent } from '../ui/Card'
import { Progress } from '../ui/Progress'
import { Badge } from '../ui/Badge'
import type { ScorecardData } from '../../types'

export interface ScoreCardProps {
  title: string
  data: ScorecardData
  icon?: React.ReactNode
}

export const ScoreCard: React.FC<ScoreCardProps> = ({ title, data }) => {
  const [isExpanded, setIsExpanded] = useState(false)
  const score = Math.max(0, Math.min(Math.round(data.score), 100))

  const getScoreBadge = (s: number) => {
    if (s >= 80) return <Badge variant="teal">Advanced</Badge>
    if (s >= 65) return <Badge variant="coral">Industry Ready</Badge>
    if (s >= 50) return <Badge variant="amber">Developing</Badge>
    return <Badge variant="destructive">Foundation</Badge>
  }

  const getProgressColor = (s: number) => {
    if (s >= 80) return 'bg-success'
    if (s >= 65) return 'bg-primary'
    if (s >= 50) return 'bg-accent-amber'
    return 'bg-error'
  }

  return (
    <Card variant="cream" className="flex flex-col justify-between overflow-hidden">
      <CardContent className="p-6 space-y-4">
        <div className="flex items-start justify-between gap-3">
          <div className="space-y-0.5">
            <h4 className="text-sm font-medium text-ink">{title}</h4>
            <span className="text-xs text-muted">{data.label || 'Assessed Metric'}</span>
          </div>
          <div className="text-right">
            <span className="font-serif text-3xl font-normal text-ink tracking-tight">
              {score}%
            </span>
          </div>
        </div>

        <div className="space-y-2">
          <Progress value={score} indicatorClassName={getProgressColor(score)} />
        </div>

        <div className="flex items-center justify-between pt-1">
          <div>{getScoreBadge(score)}</div>
          <button
            type="button"
            onClick={() => setIsExpanded(!isExpanded)}
            className="flex items-center gap-1 text-xs text-primary hover:text-primary-active font-medium focus:outline-none"
          >
            <span>{isExpanded ? 'Hide factors' : 'View factors'}</span>
            {isExpanded ? <ChevronUp className="h-3.5 w-3.5" /> : <ChevronDown className="h-3.5 w-3.5" />}
          </button>
        </div>

        {isExpanded && (
          <div className="pt-3 border-t border-hairline space-y-3 animate-in fade-in">
            {data.why && (
              <div className="text-xs text-body bg-canvas p-3 rounded-md border border-hairline leading-relaxed">
                {data.why}
              </div>
            )}

            {data.positives && data.positives.length > 0 && (
              <div className="space-y-1.5">
                <span className="text-[11px] font-semibold uppercase tracking-wider text-[#226634] dark:text-[#5db872]">
                  Strength Signals
                </span>
                <ul className="space-y-1">
                  {data.positives.map((pos, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-xs text-body">
                      <Check className="h-3.5 w-3.5 text-success shrink-0 mt-0.5" />
                      <span>{pos}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {data.improvements && data.improvements.length > 0 && (
              <div className="space-y-1.5">
                <span className="text-[11px] font-semibold uppercase tracking-wider text-[#8c5214] dark:text-[#e8a55a]">
                  Priorities to Improve
                </span>
                <ul className="space-y-1">
                  {data.improvements.map((imp, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-xs text-body">
                      <AlertCircle className="h-3.5 w-3.5 text-accent-amber shrink-0 mt-0.5" />
                      <span>{imp}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  )
}
