import React, { useState } from 'react'
import { ChevronDown, ChevronUp, Check, FileText } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/Card'
import { Badge } from '../ui/Badge'
import { Progress } from '../ui/Progress'
import { SpikeMark } from '../ui/Icons'
import type { ResumeData } from '../../types'

export interface ResumeAnalysisCardProps {
  resume: ResumeData
}

export const ResumeAnalysisCard: React.FC<ResumeAnalysisCardProps> = ({ resume }) => {
  const [showRawText, setShowRawText] = useState(false)

  return (
    <Card variant="cream" className="overflow-hidden">
      <CardHeader className="bg-surface-soft border-b border-hairline pb-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <FileText className="h-5 w-5 text-primary" />
              <CardTitle className="text-2xl md:text-3xl text-ink">
                Resume Analysis & ATS Readiness
              </CardTitle>
            </div>
            <CardDescription>
              Detected Domain:{' '}
              <span className="text-ink font-medium">{resume.detected_domain}</span> (
              {Math.round((resume.domain_confidence || 0.8) * 100)}% confidence)
            </CardDescription>
          </div>

          <Badge variant={resume.extraction_status === 'Success' ? 'teal' : 'amber'}>
            Status: {resume.extraction_status}
          </Badge>
        </div>
      </CardHeader>

      <CardContent className="p-6 md:p-8 space-y-6">
        {/* Metric Cards Row */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="p-4 rounded-md border border-hairline bg-canvas space-y-1">
            <span className="text-xs text-muted">Strength Score</span>
            <div className="font-serif text-3xl font-normal text-ink">
              {resume.strength_score}%
            </div>
            <Progress value={resume.strength_score} />
          </div>

          <div className="p-4 rounded-md border border-primary/30 bg-canvas space-y-1 shadow-subtle">
            <span className="text-xs font-medium text-primary">ATS Readiness</span>
            <div className="font-serif text-3xl font-normal text-primary">
              {resume.ats_readiness_score}%
            </div>
            <Progress value={resume.ats_readiness_score} />
          </div>

          <div className="p-4 rounded-md border border-hairline bg-canvas space-y-1">
            <span className="text-xs text-muted">Completeness</span>
            <div className="font-serif text-3xl font-normal text-ink">
              {resume.completeness_score}%
            </div>
            <Progress value={resume.completeness_score} />
          </div>

          <div className="p-4 rounded-md border border-hairline bg-canvas space-y-1">
            <span className="text-xs text-muted">Industry Proof</span>
            <div className="font-serif text-3xl font-normal text-ink">
              {resume.industry_readiness_score}%
            </div>
            <Progress value={resume.industry_readiness_score} />
          </div>
        </div>

        {/* Categorized Skills */}
        {resume.skill_categories && Object.keys(resume.skill_categories).length > 0 && (
          <div className="space-y-3">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-muted flex items-center gap-2">
              <SpikeMark className="h-3 w-3 fill-primary" />
              <span>Extracted Skill Bank by Category</span>
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {Object.entries(resume.skill_categories).map(([cat, skills]) => {
                if (!skills || skills.length === 0) return null
                return (
                  <div key={cat} className="p-4 rounded-md border border-hairline bg-canvas space-y-2">
                    <span className="text-xs font-semibold text-ink">{cat}</span>
                    <div className="flex flex-wrap gap-1">
                      {skills.map((s, idx) => (
                        <span
                          key={idx}
                          className="inline-flex items-center rounded-md bg-surface-card px-2 py-0.5 text-[11px] text-ink"
                        >
                          {s}
                        </span>
                      ))}
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        )}

        {/* Experience & Projects */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5 pt-2">
          {resume.structured_experience && resume.structured_experience.length > 0 && (
            <div className="p-5 rounded-md border border-hairline bg-canvas space-y-3">
              <h4 className="text-xs font-semibold uppercase tracking-wider text-muted">
                Detected Experience
              </h4>
              <div className="space-y-3">
                {resume.structured_experience.slice(0, 3).map((exp, idx) => (
                  <div key={idx} className="text-xs space-y-0.5 border-b border-hairline pb-2 last:border-0 last:pb-0">
                    <div className="font-semibold text-ink">{exp.role || 'Role'}</div>
                    <div className="text-muted">
                      {exp.company || ''} {exp.duration ? `• ${exp.duration}` : ''}
                    </div>
                    {exp.achievements && (
                      <div className="text-[#246b5e] dark:text-[#5db8a6] font-medium mt-1">Impact: {exp.achievements}</div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {resume.structured_projects && resume.structured_projects.length > 0 && (
            <div className="p-5 rounded-md border border-hairline bg-canvas space-y-3">
              <h4 className="text-xs font-semibold uppercase tracking-wider text-muted">
                Detected Projects
              </h4>
              <div className="space-y-3">
                {resume.structured_projects.slice(0, 3).map((proj, idx) => (
                  <div key={idx} className="text-xs space-y-0.5 border-b border-hairline pb-2 last:border-0 last:pb-0">
                    <div className="font-semibold text-ink">{proj.name || 'Project'}</div>
                    {proj.tech_stack && <div className="text-muted">Stack: {proj.tech_stack}</div>}
                    {proj.impact && (
                      <div className="text-[#246b5e] dark:text-[#5db8a6] font-medium mt-1">Outcome: {proj.impact}</div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Diagnostic Notes */}
        {resume.insights && resume.insights.length > 0 && (
          <div className="p-5 rounded-md border border-hairline bg-canvas space-y-2">
            <span className="text-xs font-semibold uppercase tracking-wider text-muted">
              Resume Diagnostic Feedback
            </span>
            <ul className="space-y-1.5">
              {resume.insights.map((note, idx) => (
                <li key={idx} className="text-xs text-body flex items-start gap-2">
                  <Check className="h-3.5 w-3.5 text-success shrink-0 mt-0.5" />
                  <span>{note}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* View Raw Extracted Text */}
        <div className="pt-2 text-xs">
          <button
            type="button"
            onClick={() => setShowRawText(!showRawText)}
            className="text-primary hover:underline font-medium flex items-center gap-1"
          >
            <span>{showRawText ? 'Hide extracted text' : 'View raw extracted resume text'}</span>
            {showRawText ? <ChevronUp className="h-3.5 w-3.5" /> : <ChevronDown className="h-3.5 w-3.5" />}
          </button>
        </div>

        {showRawText && (
          <div className="p-4 rounded-md border border-hairline bg-surface-dark text-on-dark animate-in fade-in">
            <pre className="text-xs font-mono whitespace-pre-wrap max-h-64 overflow-y-auto dark-scroll">
              {resume.text}
            </pre>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
