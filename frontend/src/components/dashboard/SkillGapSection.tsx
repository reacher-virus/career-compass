import React from 'react'
import { Check, AlertCircle } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/Card'
import { Badge } from '../ui/Badge'
import { Progress } from '../ui/Progress'
import { SpikeMark } from '../ui/Icons'

export interface SkillGapSectionProps {
  matchedSkills: string[]
  missingSkills: string[]
  recommendedSkills?: string[]
  skillCoverage: number
  totalRequired: number
}

export const SkillGapSection: React.FC<SkillGapSectionProps> = ({
  matchedSkills,
  missingSkills,
  recommendedSkills = [],
  skillCoverage,
  totalRequired,
}) => {
  return (
    <Card variant="cream" className="overflow-hidden">
      <CardHeader className="bg-surface-soft border-b border-hairline pb-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <SpikeMark className="h-4 w-4 fill-primary" />
              <CardTitle className="text-2xl md:text-3xl text-ink">
                Skill Gap & Alignment Matrix
              </CardTitle>
            </div>
            <CardDescription>
              Candidate verified skills vs target role core requirements ({matchedSkills.length} of {totalRequired} covered)
            </CardDescription>
          </div>

          <div className="flex items-center gap-2">
            <Badge variant="coral">Coverage: {skillCoverage}%</Badge>
          </div>
        </div>
      </CardHeader>

      <CardContent className="p-6 md:p-8 space-y-6">
        {/* Progress Bar */}
        <div className="space-y-2">
          <div className="flex justify-between text-xs font-medium text-muted">
            <span>Role Alignment Progress</span>
            <span className="font-serif text-sm text-ink">{skillCoverage}% Matched</span>
          </div>
          <Progress
            value={skillCoverage}
            indicatorClassName={skillCoverage >= 70 ? 'bg-success' : 'bg-primary'}
          />
        </div>

        {/* 2-Column Matrix */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Matched Skills */}
          <div className="p-5 rounded-md border border-hairline bg-canvas space-y-3">
            <div className="flex items-center justify-between">
              <h4 className="text-xs font-semibold uppercase tracking-wider text-[#226634] dark:text-[#5db872] flex items-center gap-2">
                <Check className="h-4 w-4 text-success" />
                <span>Verified Matching Competencies</span>
              </h4>
              <Badge variant="teal">{matchedSkills.length}</Badge>
            </div>

            {matchedSkills.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {matchedSkills.map((skill, idx) => (
                  <Badge key={idx} variant="teal">
                    <Check className="h-3 w-3 mr-1 text-success" />
                    <span>{skill}</span>
                  </Badge>
                ))}
              </div>
            ) : (
              <p className="text-xs text-muted-soft italic">No matching competencies detected yet.</p>
            )}
          </div>

          {/* Missing Skills */}
          <div className="p-5 rounded-md border border-hairline bg-canvas space-y-3">
            <div className="flex items-center justify-between">
              <h4 className="text-xs font-semibold uppercase tracking-wider text-[#8c5214] dark:text-[#e8a55a] flex items-center gap-2">
                <AlertCircle className="h-4 w-4 text-accent-amber" />
                <span>Missing Role Requirements</span>
              </h4>
              <Badge variant="amber">{missingSkills.length}</Badge>
            </div>

            {missingSkills.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {missingSkills.map((skill, idx) => (
                  <Badge key={idx} variant="amber">
                    <span className="text-primary mr-1">+</span>
                    <span>{skill}</span>
                  </Badge>
                ))}
              </div>
            ) : (
              <p className="text-xs text-success font-medium">
                Outstanding! All core role requirements are covered.
              </p>
            )}
          </div>
        </div>

        {/* Highest ROI Recommended Skills */}
        {recommendedSkills.length > 0 && (
          <div className="p-5 rounded-md border border-primary/30 bg-canvas space-y-2.5">
            <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-primary">
              <SpikeMark className="h-3.5 w-3.5 fill-primary" />
              <span>Highest ROI Skills To Learn Next:</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {recommendedSkills.map((skill, idx) => (
                <span
                  key={idx}
                  className="inline-flex items-center rounded-md bg-surface-card border border-hairline px-3 py-1 text-xs font-medium text-ink"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
