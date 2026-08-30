import React from 'react'
import { Check, AlertCircle } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/Card'
import { CircularProgress } from './CircularProgress'
import { SpikeMark } from '../ui/Icons'

export interface ResumeMatchSectionProps {
  resumeMatch: {
    overall_match: number
    weighted_scores: Record<string, any>
    strengths: string[]
    weaknesses: string[]
    critical_missing_skills: string[]
    important_skills: string[]
    nice_to_have_skills: string[]
    improvement_suggestions: Array<{ suggestion: string; why: string }>
  }
}

export const ResumeMatchSection: React.FC<ResumeMatchSectionProps> = ({ resumeMatch }) => {
  return (
    <Card variant="canvas" className="overflow-hidden">
      <CardHeader className="bg-surface-soft border-b border-hairline pb-6">
        <div className="flex items-center gap-2.5">
          <SpikeMark className="h-4 w-4 fill-primary" />
          <div>
            <CardTitle className="text-2xl md:text-3xl text-ink">
              Resume vs Role Alignment
            </CardTitle>
            <CardDescription>
              Weighted algorithmic fit across technical keywords, project proof, and domain seniority
            </CardDescription>
          </div>
        </div>
      </CardHeader>

      <CardContent className="p-6 md:p-8 space-y-8">
        {/* Gauge + Metrics Grid */}
        <div className="flex flex-col md:flex-row items-center justify-around gap-8 p-6 md:p-8 rounded-md border border-hairline bg-surface-card">
          <div className="flex flex-col items-center">
            <CircularProgress
              score={resumeMatch.overall_match}
              size={120}
              label="Overall Match Fit"
              sublabel="Calibrated role benchmark"
            />
          </div>

          {resumeMatch.weighted_scores && (
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3.5 flex-1">
              {Object.entries(resumeMatch.weighted_scores).map(([label, score]) => {
                if (typeof score !== 'number') return null
                return (
                  <div key={label} className="p-4 rounded-md border border-hairline bg-canvas text-center space-y-1">
                    <span className="text-[11px] text-muted line-clamp-1">{label}</span>
                    <div className="font-serif text-2xl font-normal text-ink">{score}%</div>
                  </div>
                )
              })}
            </div>
          )}
        </div>

        {/* Strengths & Weaknesses */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="p-5 rounded-md border border-hairline bg-surface-card space-y-3">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-[#226634] dark:text-[#5db872] flex items-center gap-2">
              <Check className="h-4 w-4 text-success" />
              <span>Alignment Highlights</span>
            </h4>
            <ul className="space-y-2">
              {resumeMatch.strengths.map((st, idx) => (
                <li key={idx} className="text-xs text-body flex items-start gap-2">
                  <span className="h-1.5 w-1.5 rounded-full bg-success mt-1.5 shrink-0" />
                  <span className="leading-relaxed">{st}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="p-5 rounded-md border border-hairline bg-surface-card space-y-3">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-[#8c5214] dark:text-[#e8a55a] flex items-center gap-2">
              <AlertCircle className="h-4 w-4 text-accent-amber" />
              <span>Detected Gaps & Misalignments</span>
            </h4>
            {resumeMatch.weaknesses && resumeMatch.weaknesses.length > 0 ? (
              <ul className="space-y-2">
                {resumeMatch.weaknesses.map((wk, idx) => (
                  <li key={idx} className="text-xs text-body flex items-start gap-2">
                    <span className="h-1.5 w-1.5 rounded-full bg-accent-amber mt-1.5 shrink-0" />
                    <span className="leading-relaxed">{wk}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-xs text-success font-medium">
                No major role misalignments detected.
              </p>
            )}
          </div>
        </div>

        {/* Actionable Suggestions */}
        {resumeMatch.improvement_suggestions && resumeMatch.improvement_suggestions.length > 0 && (
          <div className="space-y-3 pt-2 border-t border-hairline">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-muted flex items-center gap-2">
              <SpikeMark className="h-3 w-3 fill-primary" />
              <span>Strategic Enhancements to Improve Match</span>
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {resumeMatch.improvement_suggestions.map((item, idx) => (
                <div key={idx} className="p-4 rounded-md border border-hairline bg-canvas space-y-1">
                  <div className="text-xs font-semibold text-ink">{item.suggestion}</div>
                  <div className="text-xs text-muted leading-relaxed">{item.why}</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
