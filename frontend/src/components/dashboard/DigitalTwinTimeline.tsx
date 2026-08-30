import React, { useState } from 'react'
import { ArrowRight, Terminal } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/Card'
import { Badge } from '../ui/Badge'
import { SpikeMark } from '../ui/Icons'
import type { DigitalTwinStage } from '../../types'

export interface DigitalTwinTimelineProps {
  stages: DigitalTwinStage[]
  careerGoal: string
}

export const DigitalTwinTimeline: React.FC<DigitalTwinTimelineProps> = ({ stages, careerGoal }) => {
  const [selectedStageIndex, setSelectedStageIndex] = useState<number>(0)
  const activeStage = stages[selectedStageIndex] || stages[0]

  return (
    <Card variant="dark" className="overflow-hidden border border-[#262420]">
      {/* Header bar mimicking developer product chrome */}
      <CardHeader className="bg-[#181715] border-b border-[#262420] pb-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-[#5db872]" />
              <CardTitle className="text-2xl md:text-3xl text-[#faf9f5]">
                Digital Career Twin Simulation
              </CardTitle>
            </div>
            <CardDescription className="text-[#a09d96]">
              Deterministic 5-stage career simulation calibrated for:{' '}
              <span className="text-[#faf9f5] font-medium">{careerGoal}</span>
            </CardDescription>
          </div>

          <div className="flex items-center gap-2">
            <Badge variant="coral">AI Trajectory</Badge>
            <Badge variant="dark" className="font-mono text-[11px]">
              {stages.length} Milestones
            </Badge>
          </div>
        </div>
      </CardHeader>

      <CardContent className="p-6 md:p-8 space-y-8 bg-[#181715]">
        {/* Stage Timeline Navigation Tabs */}
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2.5">
          {stages.map((stage, idx) => {
            const isSelected = selectedStageIndex === idx
            return (
              <button
                key={idx}
                type="button"
                onClick={() => setSelectedStageIndex(idx)}
                className={`flex flex-col items-start text-left p-3.5 rounded-md border transition-all duration-150 ${
                  isSelected
                    ? 'bg-[#252320] border-[#cc785c] text-[#faf9f5]'
                    : 'bg-[#1f1e1b] border-[#2e2b27] text-[#a09d96] hover:text-[#faf9f5] hover:bg-[#252320]'
                }`}
              >
                <div className="flex items-center justify-between w-full">
                  <span className="text-[11px] font-mono uppercase text-[#cc785c]">
                    {stage.label}
                  </span>
                  <span className="text-[10px] text-[#6c6a64]">{stage.career_stage}</span>
                </div>
                <span className="text-xs font-medium text-[#faf9f5] mt-1.5 line-clamp-1">
                  {stage.role}
                </span>
                <span className="font-serif text-sm text-[#faf9f5] mt-0.5 font-normal">
                  {stage.salary}
                </span>
              </button>
            )
          })}
        </div>

        {/* Selected Stage Detail Hero (Dark Product Surface) */}
        <div className="rounded-lg border border-[#2e2b27] bg-[#1f1e1b] p-6 md:p-8 space-y-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 pb-6 border-b border-[#2e2b27]">
            <div className="space-y-1.5">
              <div className="flex items-center gap-2 text-xs font-mono text-[#cc785c]">
                <SpikeMark className="h-3 w-3 fill-[#cc785c]" />
                <span>
                  {activeStage.label} • {activeStage.career_stage}
                </span>
              </div>
              <h3 className="font-serif text-3xl md:text-4xl text-[#faf9f5] font-normal tracking-[-0.02em]">
                {activeStage.role}
              </h3>
            </div>

            <div className="flex flex-wrap items-center gap-4">
              <div className="p-4 rounded-md bg-[#252320] border border-[#33312e] space-y-0.5">
                <span className="text-[10px] uppercase font-mono tracking-wider text-[#a09d96]">
                  Target Compensation
                </span>
                <div className="font-serif text-2xl text-[#5db872] font-normal">
                  {activeStage.salary}
                </div>
              </div>

              <div className="p-4 rounded-md bg-[#252320] border border-[#33312e] flex items-center gap-4">
                <div>
                  <span className="text-[10px] uppercase font-mono tracking-wider text-[#a09d96]">
                    Confidence
                  </span>
                  <div className="font-serif text-2xl text-[#cc785c] font-normal">
                    {activeStage.confidence}%
                  </div>
                </div>
                <div className="h-8 w-px bg-[#33312e]" />
                <div>
                  <span className="text-[10px] uppercase font-mono tracking-wider text-[#a09d96]">
                    Success Prob
                  </span>
                  <div className="font-serif text-2xl text-[#5db8a6] font-normal">
                    {activeStage.probability}%
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Competency requirements code panel */}
          <div className="space-y-3">
            <div className="flex items-center gap-2 text-xs font-mono text-[#a09d96]">
              <Terminal className="h-3.5 w-3.5 text-[#cc785c]" />
              <span>REQUIRED_PROOFS_AND_COMPETENCIES:</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {activeStage.skills.map((skill, sIdx) => (
                <span
                  key={sIdx}
                  className="inline-flex items-center rounded-md bg-[#252320] border border-[#33312e] px-3 py-1.5 text-xs font-mono text-[#faf9f5]"
                >
                  <span className="text-[#cc785c] mr-1.5">$</span>
                  {skill}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Milestone Progression Road */}
        <div className="space-y-4 pt-2">
          <h4 className="text-xs font-mono uppercase tracking-wider text-[#a09d96] flex items-center gap-2">
            <SpikeMark className="h-3 w-3 fill-[#cc785c]" />
            <span>PROGRESSION_SEQUENCE</span>
          </h4>

          <div className="space-y-2">
            {stages.map((stage, idx) => (
              <div
                key={idx}
                onClick={() => setSelectedStageIndex(idx)}
                className={`p-4 rounded-md border flex flex-col sm:flex-row sm:items-center justify-between gap-3 cursor-pointer transition-colors ${
                  selectedStageIndex === idx
                    ? 'bg-[#252320] border-[#cc785c]'
                    : 'bg-[#1f1e1b] border-[#2e2b27] hover:bg-[#252320]'
                }`}
              >
                <div className="flex items-center gap-3">
                  <span className="text-xs font-mono text-[#cc785c] w-20">
                    {stage.label}
                  </span>
                  <div>
                    <span className="text-sm font-medium text-[#faf9f5]">
                      {stage.role}
                    </span>
                    <p className="text-xs text-[#a09d96] line-clamp-1 mt-0.5">
                      Focus: {stage.skills.slice(0, 3).join(', ')}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-4 shrink-0 justify-between sm:justify-end">
                  <span className="font-serif text-sm text-[#faf9f5]">{stage.salary}</span>
                  <ArrowRight className="h-4 w-4 text-[#cc785c]" />
                </div>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
