import React from 'react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/Card'
import { Badge } from '../ui/Badge'
import { SpikeMark } from '../ui/Icons'

export interface CareerIntelligenceCardProps {
  careerName: string
  knowledge: Record<string, any>
}

export const CareerIntelligenceCard: React.FC<CareerIntelligenceCardProps> = ({
  careerName,
  knowledge,
}) => {
  return (
    <Card variant="cream" className="overflow-hidden">
      <CardHeader className="bg-surface-soft border-b border-hairline pb-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <SpikeMark className="h-4 w-4 fill-primary" />
              <CardTitle className="text-2xl md:text-3xl text-ink">
                Universal Career Blueprint
              </CardTitle>
            </div>
            <CardDescription>
              Grounded recruiter expectations and core responsibilities for{' '}
              <span className="text-ink font-medium">{careerName}</span>
            </CardDescription>
          </div>

          {knowledge.domain && <Badge variant="dark">{knowledge.domain}</Badge>}
        </div>
      </CardHeader>

      <CardContent className="p-6 md:p-8 space-y-6">
        {knowledge.description && (
          <p className="text-sm text-body leading-relaxed bg-canvas p-5 rounded-md border border-hairline">
            {knowledge.description}
          </p>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Daily Responsibilities */}
          {knowledge.daily_responsibilities && knowledge.daily_responsibilities.length > 0 && (
            <div className="space-y-3">
              <h4 className="text-xs font-semibold uppercase tracking-wider text-muted flex items-center gap-2">
                <SpikeMark className="h-3 w-3 fill-primary" />
                <span>Primary Day-to-Day Responsibilities</span>
              </h4>
              <ul className="space-y-2">
                {knowledge.daily_responsibilities.slice(0, 5).map((item: string, idx: number) => (
                  <li key={idx} className="text-xs text-body flex items-start gap-2.5">
                    <span className="h-1.5 w-1.5 rounded-full bg-primary mt-1.5 shrink-0" />
                    <span className="leading-relaxed">{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* KPIs */}
          {knowledge.kpis && knowledge.kpis.length > 0 && (
            <div className="space-y-3">
              <h4 className="text-xs font-semibold uppercase tracking-wider text-muted flex items-center gap-2">
                <SpikeMark className="h-3 w-3 fill-primary" />
                <span>Key Performance Indicators (KPIs)</span>
              </h4>
              <ul className="space-y-2">
                {knowledge.kpis.slice(0, 5).map((item: string, idx: number) => (
                  <li key={idx} className="text-xs text-body flex items-start gap-2.5">
                    <span className="h-1.5 w-1.5 rounded-full bg-accent-teal mt-1.5 shrink-0" />
                    <span className="leading-relaxed">{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {/* ATS Keywords & Certifications */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4 border-t border-hairline">
          {knowledge.ats_keywords && knowledge.ats_keywords.length > 0 && (
            <div className="space-y-2.5">
              <h4 className="text-xs font-semibold uppercase tracking-wider text-muted">
                High-Impact ATS Keywords
              </h4>
              <div className="flex flex-wrap gap-1.5">
                {knowledge.ats_keywords.slice(0, 10).map((kw: string, idx: number) => (
                  <span
                    key={idx}
                    className="inline-flex items-center rounded-md bg-canvas border border-hairline px-2.5 py-1 text-xs text-ink"
                  >
                    {kw}
                  </span>
                ))}
              </div>
            </div>
          )}

          {knowledge.preferred_certifications && knowledge.preferred_certifications.length > 0 && (
            <div className="space-y-2.5">
              <h4 className="text-xs font-semibold uppercase tracking-wider text-muted">
                Recommended Certifications
              </h4>
              <div className="flex flex-wrap gap-1.5">
                {knowledge.preferred_certifications.slice(0, 4).map((cert: string, idx: number) => (
                  <Badge key={idx} variant="teal">
                    {cert}
                  </Badge>
                ))}
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}
