import React, { useState } from 'react'
import { ChevronDown, ChevronUp, Check, Calendar } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/Card'
import { Badge } from '../ui/Badge'
import { SpikeMark } from '../ui/Icons'

export interface RoadmapItem {
  month: string
  focus: string
  tasks: string[]
  outcome: string
  weeks?: Array<{ week: string; milestone: string }>
}

export interface RoadmapSectionProps {
  roadmap: RoadmapItem[]
  aiNotes?: string | null
}

export const RoadmapSection: React.FC<RoadmapSectionProps> = ({ roadmap, aiNotes }) => {
  const [expandedMonths, setExpandedMonths] = useState<Record<string, boolean>>({
    'Month 1': true,
    'Month 2': true,
  })

  const toggleMonth = (month: string) => {
    setExpandedMonths((prev) => ({
      ...prev,
      [month]: !prev[month],
    }))
  }

  return (
    <Card variant="canvas" className="overflow-hidden">
      <CardHeader className="bg-surface-soft border-b border-hairline pb-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <SpikeMark className="h-4 w-4 fill-primary" />
              <CardTitle className="text-2xl md:text-3xl text-ink">
                AI Career Learning Roadmap
              </CardTitle>
            </div>
            <CardDescription>
              Sequenced milestone trajectory turning skill deficits into measurable public proof
            </CardDescription>
          </div>

          <Badge variant="coral">Actionable Timeline</Badge>
        </div>
      </CardHeader>

      <CardContent className="p-6 md:p-8 space-y-4">
        {roadmap.map((item, idx) => {
          const isExpanded = expandedMonths[item.month] !== false
          return (
            <div
              key={idx}
              className="rounded-md border border-hairline bg-surface-card overflow-hidden transition-colors"
            >
              <button
                type="button"
                onClick={() => toggleMonth(item.month)}
                className="w-full flex items-center justify-between p-5 text-left hover:bg-surface-cream-strong/70 transition-colors"
              >
                <div className="flex items-center gap-4">
                  <span className="font-mono text-xs font-semibold px-2.5 py-1 rounded-md bg-canvas text-primary border border-hairline">
                    {item.month}
                  </span>
                  <div>
                    <h4 className="font-serif text-xl font-normal text-ink">
                      {item.focus}
                    </h4>
                    <p className="text-xs text-muted line-clamp-1 mt-0.5">
                      Target: {item.outcome}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-2 text-muted">
                  {isExpanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                </div>
              </button>

              {isExpanded && (
                <div className="p-5 pt-0 border-t border-hairline space-y-4 bg-canvas animate-in fade-in">
                  {/* Tasks */}
                  <div className="space-y-2 pt-4">
                    <span className="text-[11px] font-semibold uppercase tracking-wider text-muted">
                      Core Competencies To Develop
                    </span>
                    <ul className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                      {item.tasks.map((task, tIdx) => (
                        <li key={tIdx} className="flex items-start gap-2 text-xs text-body">
                          <Check className="h-3.5 w-3.5 text-success shrink-0 mt-0.5" />
                          <span>{task}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Weekly Milestones */}
                  {item.weeks && item.weeks.length > 0 && (
                    <div className="space-y-2 pt-2 border-t border-hairline">
                      <span className="text-[11px] font-semibold uppercase tracking-wider text-muted flex items-center gap-1.5">
                        <Calendar className="h-3.5 w-3.5 text-primary" />
                        <span>Weekly Milestones</span>
                      </span>
                      <div className="space-y-1.5">
                        {item.weeks.map((w, wIdx) => (
                          <div
                            key={wIdx}
                            className="flex items-start gap-2 p-3 rounded-md bg-surface-card border border-hairline text-xs"
                          >
                            <span className="font-mono text-[11px] font-semibold text-primary shrink-0">
                              {w.week}:
                            </span>
                            <span className="text-ink">{w.milestone}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Outcome */}
                  <div className="p-3.5 rounded-md bg-surface-card border border-hairline text-xs text-[#246b5e] dark:text-[#5db8a6] flex items-center gap-2">
                    <SpikeMark className="h-3.5 w-3.5 fill-accent-teal shrink-0" />
                    <span>
                      <strong className="font-medium">Deliverable:</strong> {item.outcome}
                    </span>
                  </div>
                </div>
              )}
            </div>
          )
        })}

        {aiNotes && (
          <div className="p-5 rounded-md border border-hairline bg-surface-card space-y-1.5 mt-4">
            <span className="text-xs font-semibold uppercase tracking-wider text-primary flex items-center gap-1.5">
              <SpikeMark className="h-3 w-3 fill-primary" />
              <span>AI Mentor Coaching Synthesis</span>
            </span>
            <p className="text-xs text-body leading-relaxed whitespace-pre-wrap">
              {aiNotes}
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
