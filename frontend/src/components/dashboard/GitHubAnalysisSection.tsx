import React from 'react'
import { Star, ExternalLink, Check } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/Card'
import { Badge } from '../ui/Badge'
import { Progress } from '../ui/Progress'
import { GitHubIcon, SpikeMark } from '../ui/Icons'
import type { GitHubAnalysis } from '../../types'

export interface GitHubAnalysisSectionProps {
  analysis: GitHubAnalysis
}

export const GitHubAnalysisSection: React.FC<GitHubAnalysisSectionProps> = ({ analysis }) => {
  return (
    <Card variant="canvas" className="overflow-hidden">
      <CardHeader className="bg-surface-soft border-b border-hairline pb-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2.5">
              <GitHubIcon className="h-5 w-5 text-ink" />
              <CardTitle className="text-2xl md:text-3xl text-ink">
                GitHub Portfolio Signals
              </CardTitle>
            </div>
            <CardDescription>
              Verified repository artifacts & open-source activity for{' '}
              <span className="font-mono text-xs text-ink">@{analysis.username}</span>
            </CardDescription>
          </div>

          <Badge variant="coral">GitHub Score: {analysis.github_score}%</Badge>
        </div>
      </CardHeader>

      <CardContent className="p-6 md:p-8 space-y-8">
        {/* Metric Cards Row */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="p-4 rounded-md border border-hairline bg-surface-card space-y-1">
            <span className="text-xs text-muted">Public Repositories</span>
            <div className="font-serif text-3xl font-normal text-ink">
              {analysis.repository_count}
            </div>
            <p className="text-[11px] text-muted-soft">{analysis.years_active} years active</p>
          </div>

          <div className="p-4 rounded-md border border-hairline bg-surface-card space-y-1">
            <span className="text-xs text-muted">Project Quality</span>
            <div className="font-serif text-3xl font-normal text-primary">
              {analysis.project_quality_score}%
            </div>
            <Progress value={analysis.project_quality_score} />
          </div>

          <div className="p-4 rounded-md border border-hairline bg-surface-card space-y-1">
            <span className="text-xs text-muted">Stars & Forks</span>
            <div className="font-serif text-2xl font-normal text-ink flex items-center gap-2">
              <span className="flex items-center gap-1 text-accent-amber">
                <Star className="h-4 w-4 fill-current" /> {analysis.total_stars}
              </span>
              <span className="text-xs text-muted-soft">/ {analysis.total_forks} forks</span>
            </div>
            <p className="text-[11px] text-muted-soft">
              Impact: {analysis.open_source_contribution_level}
            </p>
          </div>

          <div className="p-4 rounded-md border border-hairline bg-surface-card space-y-1">
            <span className="text-xs text-muted">Primary Language</span>
            <div className="font-serif text-2xl font-normal text-ink line-clamp-1">
              {analysis.most_used_language || 'Polyglot'}
            </div>
            <p className="text-[11px] text-muted-soft">
              Strength: {analysis.portfolio_strength}
            </p>
          </div>
        </div>

        {/* Repositories */}
        {analysis.repos && analysis.repos.length > 0 && (
          <div className="space-y-3">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-muted flex items-center gap-2">
              <SpikeMark className="h-3 w-3 fill-primary" />
              <span>Evaluated Repositories & Proof Artifacts</span>
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {analysis.repos.slice(0, 4).map((repo, idx) => (
                <div
                  key={idx}
                  className="p-5 rounded-md border border-hairline bg-surface-card space-y-3 flex flex-col justify-between"
                >
                  <div className="space-y-1.5">
                    <div className="flex items-start justify-between gap-2">
                      <span className="font-mono text-sm font-semibold text-ink line-clamp-1">
                        {repo.name}
                      </span>
                      <Badge variant="teal" className="text-[11px]">
                        Quality: {repo.quality_score}%
                      </Badge>
                    </div>
                    {repo.description && (
                      <p className="text-xs text-muted line-clamp-2 leading-relaxed">
                        {repo.description}
                      </p>
                    )}
                  </div>

                  <div className="flex items-center justify-between pt-3 border-t border-hairline text-xs text-muted">
                    <div className="flex items-center gap-3">
                      {repo.language && (
                        <span className="font-mono text-ink">{repo.language}</span>
                      )}
                      {repo.stars > 0 && (
                        <span className="flex items-center gap-1 text-accent-amber">
                          <Star className="h-3.5 w-3.5 fill-current" /> {repo.stars}
                        </span>
                      )}
                    </div>
                    {repo.url && (
                      <a
                        href={repo.url}
                        target="_blank"
                        rel="noreferrer"
                        className="text-primary hover:underline flex items-center gap-1 font-medium"
                      >
                        <span>View</span>
                        <ExternalLink className="h-3 w-3" />
                      </a>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Strengths & Recommendations */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5 pt-2">
          {analysis.strengths && analysis.strengths.length > 0 && (
            <div className="p-5 rounded-md border border-hairline bg-surface-card space-y-2">
              <span className="text-xs font-semibold uppercase tracking-wider text-[#226634] dark:text-[#5db872] flex items-center gap-2">
                <Check className="h-4 w-4 text-success" />
                <span>Portfolio Strengths</span>
              </span>
              <ul className="space-y-1.5">
                {analysis.strengths.map((st, idx) => (
                  <li key={idx} className="text-xs text-body flex items-start gap-2">
                    <span className="h-1.5 w-1.5 rounded-full bg-success mt-1.5 shrink-0" />
                    <span>{st}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {analysis.recommendations && analysis.recommendations.length > 0 && (
            <div className="p-5 rounded-md border border-hairline bg-surface-card space-y-2">
              <span className="text-xs font-semibold uppercase tracking-wider text-primary flex items-center gap-2">
                <SpikeMark className="h-3 w-3 fill-primary" />
                <span>Portfolio Recommendations</span>
              </span>
              <ul className="space-y-1.5">
                {analysis.recommendations.slice(0, 3).map((rec, idx) => (
                  <li key={idx} className="text-xs text-body flex items-start gap-2">
                    <span className="h-1.5 w-1.5 rounded-full bg-primary mt-1.5 shrink-0" />
                    <span>{rec}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}
