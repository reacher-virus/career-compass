import React, { useState } from 'react'
import { Terminal, Check, AlertCircle } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/Card'
import { Button } from '../ui/Button'
import { Textarea } from '../ui/Textarea'
import { Badge } from '../ui/Badge'
import { CircularProgress } from './CircularProgress'
import { SpikeMark } from '../ui/Icons'
import { matchJobDescription } from '../../api/client'
import type { JobDescriptionMatchResult, ResumeData } from '../../types'

export interface JobDescriptionMatcherProps {
  resumeData?: ResumeData | null
  resumeText?: string
}

export const JobDescriptionMatcher: React.FC<JobDescriptionMatcherProps> = ({
  resumeData,
  resumeText,
}) => {
  const [jdText, setJdText] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [matchResult, setMatchResult] = useState<JobDescriptionMatchResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleCompare = async () => {
    if (!jdText.trim()) {
      setError('Please paste a job description text to compare.')
      return
    }

    const textToCompare = resumeData?.text || resumeText || ''
    if (!textToCompare) {
      setError('No resume text available. Please upload a resume in Profile Setup first.')
      return
    }

    setIsLoading(true)
    setError(null)
    try {
      const res = await matchJobDescription({
        resume_text: textToCompare,
        resume_data: resumeData,
        job_description_text: jdText.trim(),
      })
      setMatchResult(res)
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Comparison failed.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Card variant="dark" className="overflow-hidden border border-[#262420]">
      <CardHeader className="bg-[#181715] border-b border-[#262420] pb-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <Terminal className="h-4 w-4 text-[#cc785c]" />
              <CardTitle className="text-2xl md:text-3xl text-[#faf9f5]">
                Live Job Posting Fit Evaluator
              </CardTitle>
            </div>
            <CardDescription className="text-[#a09d96]">
              Paste any live job specification to run real-time semantic & keyword alignment
            </CardDescription>
          </div>

          <Badge variant="coral">Interactive Tool</Badge>
        </div>
      </CardHeader>

      <CardContent className="p-6 md:p-8 space-y-6 bg-[#181715]">
        <div className="space-y-3">
          <textarea
            placeholder="Paste target job posting requirements text here (e.g. Senior AI Engineer qualifications, stack, deliverables)..."
            value={jdText}
            onChange={(e) => setJdText(e.target.value)}
            rows={4}
            className="w-full rounded-md border border-[#33312e] bg-[#1f1e1b] p-3.5 text-xs text-[#faf9f5] font-mono placeholder:text-[#6c6a64] focus:border-[#cc785c] focus:outline-none focus:ring-2 focus:ring-[#cc785c]/20 transition-colors"
          />

          {error && <p className="text-xs font-medium text-[#c64545]">{error}</p>}

          <div className="flex justify-end">
            <Button
              type="button"
              onClick={handleCompare}
              isLoading={isLoading}
              variant="primary"
              className="gap-2"
            >
              <SpikeMark className="h-3.5 w-3.5 fill-white" />
              <span>Evaluate Fit vs Job Posting</span>
            </Button>
          </div>
        </div>

        {matchResult && (
          <div className="space-y-6 pt-6 border-t border-[#2e2b27] animate-in fade-in">
            {/* Circular Gauges on Dark Surface */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 p-6 rounded-md border border-[#2e2b27] bg-[#1f1e1b]">
              <CircularProgress
                score={matchResult.keyword_match}
                size={96}
                label="ATS Keyword Fit"
                sublabel="Exact token alignment"
                isDark
              />
              <CircularProgress
                score={matchResult.semantic_match}
                size={96}
                label="Semantic Context"
                sublabel="Domain comprehension"
                isDark
              />
              <CircularProgress
                score={matchResult.technical_match}
                size={96}
                label="Technical Stack"
                sublabel="Tool & framework fit"
                isDark
              />
            </div>

            {/* Recommendation on Dark */}
            <div className="p-5 rounded-md border border-[#2e2b27] bg-[#252320] flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <span className="text-[10px] font-mono uppercase tracking-wider text-[#a09d96]">
                  Hiring Decision Forecast
                </span>
                <div className="font-serif text-xl text-[#faf9f5] mt-0.5">
                  {matchResult.hiring_recommendation}
                </div>
              </div>
              <div className="flex items-center gap-4 text-xs font-mono text-[#a09d96]">
                <span>Exp: {matchResult.experience_match}%</span>
                <span>Edu: {matchResult.education_match}%</span>
                <span>Cert: {matchResult.certification_match}%</span>
              </div>
            </div>

            {/* Keyword pills */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-4 rounded-md border border-[#2e2b27] bg-[#1f1e1b] space-y-2">
                <span className="text-xs font-mono text-[#5db872] flex items-center gap-1.5">
                  <Check className="h-3.5 w-3.5" />
                  <span>MATCHED_KEYWORDS ({matchResult.matched_keywords.length})</span>
                </span>
                <div className="flex flex-wrap gap-1.5">
                  {matchResult.matched_keywords.map((kw, idx) => (
                    <span
                      key={idx}
                      className="inline-flex items-center rounded-md bg-[#252320] border border-[#33312e] px-2 py-0.5 text-xs font-mono text-[#5db872]"
                    >
                      {kw}
                    </span>
                  ))}
                </div>
              </div>

              <div className="p-4 rounded-md border border-[#2e2b27] bg-[#1f1e1b] space-y-2">
                <span className="text-xs font-mono text-[#e8a55a] flex items-center gap-1.5">
                  <AlertCircle className="h-3.5 w-3.5" />
                  <span>MISSING_KEYWORDS ({matchResult.missing_keywords.length})</span>
                </span>
                <div className="flex flex-wrap gap-1.5">
                  {matchResult.missing_keywords.map((kw, idx) => (
                    <span
                      key={idx}
                      className="inline-flex items-center rounded-md bg-[#252320] border border-[#33312e] px-2 py-0.5 text-xs font-mono text-[#e8a55a]"
                    >
                      +{kw}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
