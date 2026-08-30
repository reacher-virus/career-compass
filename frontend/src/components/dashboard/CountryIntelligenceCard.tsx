import React from 'react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/Card'
import { Badge } from '../ui/Badge'
import { SpikeMark } from '../ui/Icons'

export interface CountryIntelligenceCardProps {
  intelligence: {
    country: string
    career: string
    flag: string
    currency: string
    demand_level: string
    entry_salary: string
    mid_level_salary: string
    senior_salary: string
    average_salary: string
    remote_work_availability: string
    visa_difficulty: string
    visa_overview: string
    market_growth: string
    hiring_trend: string
    top_hiring_companies?: string[]
    major_hiring_industries?: string[]
    most_required_skills?: string[]
    most_valuable_certifications?: string[]
    cost_of_living?: string
    interview_style?: string
    future_outlook?: string
  }
}

export const CountryIntelligenceCard: React.FC<CountryIntelligenceCardProps> = ({ intelligence }) => {
  const getVisaBadge = (diff: string) => {
    if (diff === 'High') return <Badge variant="destructive">Visa: High Complexity</Badge>
    if (diff === 'Medium') return <Badge variant="amber">Visa: Manageable</Badge>
    return <Badge variant="teal">Visa: Low Friction</Badge>
  }

  const getDemandBadge = (demand: string) => {
    if (demand === 'Very High') return <Badge variant="coral">Demand: Very High</Badge>
    if (demand === 'High') return <Badge variant="teal">Demand: High</Badge>
    return <Badge variant="default">Demand: Moderate</Badge>
  }

  return (
    <Card variant="canvas" className="overflow-hidden">
      <CardHeader className="bg-surface-soft border-b border-hairline pb-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="text-xl">{intelligence.flag}</span>
              <CardTitle className="text-2xl md:text-3xl text-ink">
                Country Market Dynamics: {intelligence.country}
              </CardTitle>
            </div>
            <CardDescription>
              Hiring velocity, localized compensation benchmarks, and visa policy for {intelligence.career}
            </CardDescription>
          </div>

          <div className="flex items-center gap-2 flex-wrap">
            {getDemandBadge(intelligence.demand_level)}
            {getVisaBadge(intelligence.visa_difficulty)}
          </div>
        </div>
      </CardHeader>

      <CardContent className="p-6 md:p-8 space-y-8">
        {/* Localized Salary Benchmark Cards */}
        <div className="space-y-3">
          <h4 className="text-xs font-semibold uppercase tracking-wider text-muted flex items-center gap-2">
            <SpikeMark className="h-3 w-3 fill-primary" />
            <span>Compensation Bands ({intelligence.currency})</span>
          </h4>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="p-5 rounded-md border border-hairline bg-surface-card space-y-1">
              <span className="text-xs text-muted">Entry-Level (0–2 Yrs)</span>
              <div className="font-serif text-2xl font-normal text-ink">
                {intelligence.entry_salary}
              </div>
              <p className="text-[11px] text-muted-soft">Foundation role base</p>
            </div>

            <div className="p-5 rounded-md border border-primary/40 bg-canvas space-y-1 shadow-subtle">
              <span className="text-xs font-medium text-primary">Mid-Level Target (3–5 Yrs)</span>
              <div className="font-serif text-3xl font-normal text-ink">
                {intelligence.mid_level_salary}
              </div>
              <p className="text-[11px] text-muted">Core market median</p>
            </div>

            <div className="p-5 rounded-md border border-hairline bg-surface-card space-y-1">
              <span className="text-xs text-muted">Senior / Staff (6+ Yrs)</span>
              <div className="font-serif text-2xl font-normal text-ink">
                {intelligence.senior_salary}
              </div>
              <p className="text-[11px] text-muted-soft">Lead & architect compensation</p>
            </div>
          </div>
        </div>

        {/* Market Vital Signs */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <div className="p-4 rounded-md border border-hairline bg-canvas space-y-0.5">
            <span className="text-[11px] text-muted">Hiring Trend</span>
            <div className="text-sm font-medium text-ink">{intelligence.hiring_trend}</div>
          </div>
          <div className="p-4 rounded-md border border-hairline bg-canvas space-y-0.5">
            <span className="text-[11px] text-muted">Market Growth</span>
            <div className="text-sm font-medium text-ink">{intelligence.market_growth}</div>
          </div>
          <div className="p-4 rounded-md border border-hairline bg-canvas space-y-0.5">
            <span className="text-[11px] text-muted">Remote Flexibility</span>
            <div className="text-sm font-medium text-ink">
              {intelligence.remote_work_availability}
            </div>
          </div>
          <div className="p-4 rounded-md border border-hairline bg-canvas space-y-0.5">
            <span className="text-[11px] text-muted">Cost of Living</span>
            <div className="text-sm font-medium text-ink">
              {intelligence.cost_of_living || 'Moderate'}
            </div>
          </div>
        </div>

        {/* Visa & Interview Pattern */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5 pt-2">
          <div className="p-5 rounded-md border border-hairline bg-surface-card space-y-2">
            <h5 className="text-xs font-semibold text-ink flex items-center gap-2">
              <SpikeMark className="h-3 w-3 fill-primary" />
              <span>Visa & Work Authorization Policy</span>
            </h5>
            <p className="text-xs text-body leading-relaxed">
              {intelligence.visa_overview}
            </p>
          </div>

          <div className="p-5 rounded-md border border-hairline bg-surface-card space-y-2">
            <h5 className="text-xs font-semibold text-ink flex items-center gap-2">
              <SpikeMark className="h-3 w-3 fill-primary" />
              <span>Interview & Evaluation Pattern</span>
            </h5>
            <p className="text-xs text-body leading-relaxed">
              {intelligence.interview_style ||
                'Technical screening, take-home systems design or portfolio review, followed by architectural panel.'}
            </p>
          </div>
        </div>

        {/* Top Hiring Employers */}
        {intelligence.top_hiring_companies && intelligence.top_hiring_companies.length > 0 && (
          <div className="space-y-3 pt-2 border-t border-hairline">
            <h5 className="text-xs font-semibold uppercase tracking-wider text-muted">
              Active Regional Employers & Ecosystem
            </h5>
            <div className="flex flex-wrap gap-2">
              {intelligence.top_hiring_companies.map((co, cIdx) => (
                <span
                  key={cIdx}
                  className="inline-flex items-center rounded-md bg-canvas border border-hairline px-3 py-1 text-xs text-ink"
                >
                  {co}
                </span>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
