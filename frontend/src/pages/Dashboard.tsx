import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { Download, UserCheck, ArrowRight } from 'lucide-react'
import { useCareer } from '../context/CareerContext'
import { Button } from '../components/ui/Button'
import { Badge } from '../components/ui/Badge'
import { Card, CardContent } from '../components/ui/Card'
import { SpikeMark } from '../components/ui/Icons'
import { ScoreCard } from '../components/dashboard/ScoreCard'
import { DigitalTwinTimeline } from '../components/dashboard/DigitalTwinTimeline'
import { CountryIntelligenceCard } from '../components/dashboard/CountryIntelligenceCard'
import { CareerIntelligenceCard } from '../components/dashboard/CareerIntelligenceCard'
import { SkillGapSection } from '../components/dashboard/SkillGapSection'
import { ResumeAnalysisCard } from '../components/dashboard/ResumeAnalysisCard'
import { ResumeMatchSection } from '../components/dashboard/ResumeMatchSection'
import { JobDescriptionMatcher } from '../components/dashboard/JobDescriptionMatcher'
import { GitHubAnalysisSection } from '../components/dashboard/GitHubAnalysisSection'
import { RoadmapSection } from '../components/dashboard/RoadmapSection'
import { ActionPlanSection } from '../components/dashboard/ActionPlanSection'
import { ReportsExportModal } from '../components/dashboard/ReportsExportModal'

export const Dashboard: React.FC = () => {
  const {
    profile,
    resumeData,
    githubAnalysis,
    analysisResult,
    isAnalyzing,
    executeAnalysis,
  } = useCareer()

  const [isExportModalOpen, setIsExportModalOpen] = useState(false)
  const [activeNav, setActiveNav] = useState('overview')

  if (!analysisResult) {
    return (
      <div className="container max-w-2xl py-24 px-4 text-center space-y-6 font-sans">
        <div className="flex h-12 w-12 items-center justify-center rounded-full bg-surface-card text-ink mx-auto border border-hairline">
          <SpikeMark className="h-6 w-6 fill-primary" />
        </div>
        <h2 className="font-serif text-4xl font-normal text-ink tracking-tight">
          No Active Career Twin Simulation
        </h2>
        <p className="text-sm text-muted max-w-md mx-auto leading-relaxed">
          Upload your resume or set up your profile to simulate your digital career twin, compute readiness scores, and generate milestone roadmaps.
        </p>
        <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
          <Link to="/setup">
            <Button size="lg" variant="primary" className="gap-2 px-6">
              <SpikeMark className="h-4 w-4 fill-white" />
              <span>Configure Career Profile</span>
            </Button>
          </Link>
          <Button
            size="lg"
            variant="secondary"
            onClick={() => executeAnalysis()}
            isLoading={isAnalyzing}
          >
            Load Sample Simulation
          </Button>
        </div>
      </div>
    )
  }

  const {
    career_goal,
    target_country,
    readiness,
    success_probability,
    coach_scores,
    career_knowledge,
    country_intelligence,
    digital_twin,
    roadmap,
    action_plan,
    resume_match,
    github_relevant,
    recommended_careers,
  } = analysisResult

  const navItems = [
    { id: 'overview', label: 'Executive KPIs' },
    { id: 'coach-scores', label: 'Coach Scores' },
    { id: 'digital-twin', label: 'Digital Twin' },
    { id: 'country-intel', label: 'Country Intel' },
    { id: 'career-intel', label: 'Role Blueprint' },
    { id: 'skill-gap', label: 'Skill Gap' },
    ...(resumeData ? [{ id: 'resume-analysis', label: 'Resume Analysis' }] : []),
    ...(resume_match ? [{ id: 'resume-match', label: 'Role Fit' }] : []),
    { id: 'job-matcher', label: 'Job Posting Matcher' },
    ...(githubAnalysis && github_relevant ? [{ id: 'github-intel', label: 'GitHub Proof' }] : []),
    { id: 'roadmap', label: 'Learning Roadmap' },
    { id: 'action-plan', label: 'Weekly Sprints' },
  ]

  const scrollToSection = (id: string) => {
    setActiveNav(id)
    const el = document.getElementById(id)
    if (el) {
      const yOffset = -80
      const y = el.getBoundingClientRect().top + window.pageYOffset + yOffset
      window.scrollTo({ top: y, behavior: 'smooth' })
    }
  }

  return (
    <div className="min-h-screen pb-24 font-sans">
      {/* Sticky Top Executive Bar */}
      <div className="sticky top-16 z-30 border-b border-hairline bg-canvas/95 backdrop-blur-xs transition-colors duration-200">
        <div className="container py-3.5 px-4 flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <span className="text-2xl">{country_intelligence?.flag || '🌐'}</span>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="font-serif text-2xl font-normal text-ink tracking-[-0.02em] line-clamp-1">
                  {career_goal}
                </h1>
                <Badge variant="coral" className="text-[10px]">
                  {target_country}
                </Badge>
              </div>
              <span className="text-xs text-muted">
                Candidate: <span className="font-medium text-ink">{profile.name || 'Anonymous'}</span>
              </span>
            </div>
          </div>

          <div className="flex items-center gap-2.5 flex-wrap">
            <Button
              size="sm"
              variant="secondary"
              onClick={() => setIsExportModalOpen(true)}
              className="gap-1.5"
            >
              <Download className="h-3.5 w-3.5" />
              <span>Export Report</span>
            </Button>
            <Link to="/setup">
              <Button size="sm" variant="secondary" className="gap-1.5">
                <UserCheck className="h-3.5 w-3.5" />
                <span>Edit Profile</span>
              </Button>
            </Link>
          </div>
        </div>

        {/* Horizontal Navigation Pills */}
        <div className="container px-4 overflow-x-auto scrollbar-none pb-2">
          <div className="flex items-center gap-1.5 w-max">
            {navItems.map((item) => (
              <button
                key={item.id}
                type="button"
                onClick={() => scrollToSection(item.id)}
                className={`text-xs px-3.5 py-1 rounded-full font-medium transition-colors ${
                  activeNav === item.id
                    ? 'bg-ink text-canvas font-semibold'
                    : 'bg-surface-card text-muted hover:text-ink'
                }`}
              >
                {item.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="container max-w-5xl py-10 px-4 space-y-16">
        {/* Section 1: Executive KPI Cards */}
        <section id="overview" className="space-y-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Card variant="cream">
              <CardContent className="p-6 space-y-1">
                <span className="text-xs text-primary font-semibold uppercase tracking-wider">
                  Readiness Score
                </span>
                <div className="font-serif text-4xl font-normal text-ink">{readiness.score}%</div>
                <span className="text-xs text-body">{readiness.label} level</span>
              </CardContent>
            </Card>

            <Card variant="cream">
              <CardContent className="p-6 space-y-1">
                <span className="text-xs text-[#226634] dark:text-[#5db872] font-semibold uppercase tracking-wider">
                  Success Probability
                </span>
                <div className="font-serif text-4xl font-normal text-ink">{success_probability}%</div>
                <span className="text-xs text-body">Career trajectory forecast</span>
              </CardContent>
            </Card>

            <Card variant="cream">
              <CardContent className="p-6 space-y-1">
                <span className="text-xs text-muted font-semibold uppercase tracking-wider">
                  Skill Coverage
                </span>
                <div className="font-serif text-4xl font-normal text-ink">
                  {readiness.matched_skills.length}
                  <span className="text-base text-muted">
                    {' '}/ {readiness.required_skills.length}
                  </span>
                </div>
                <span className="text-xs text-muted">Role core requirements</span>
              </CardContent>
            </Card>

            <Card variant="cream">
              <CardContent className="p-6 space-y-1">
                <span className="text-xs text-muted font-semibold uppercase tracking-wider">
                  Weekly Commitment
                </span>
                <div className="font-serif text-4xl font-normal text-ink">{profile.weekly_study_hours}h</div>
                <span className="text-xs text-muted">Pacing multiplier</span>
              </CardContent>
            </Card>
          </div>
        </section>

        {/* Section 2: Coach Scorecards Grid */}
        <section id="coach-scores" className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="font-serif text-3xl font-normal text-ink flex items-center gap-2.5">
              <SpikeMark className="h-4 w-4 fill-primary" />
              <span>Professional Coach Scorecards</span>
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {coach_scores && (
              <>
                <ScoreCard title="Career Readiness" data={coach_scores.readiness} />
                <ScoreCard title="Success Probability" data={coach_scores.success_probability} />
                <ScoreCard title="AI Confidence" data={coach_scores.ai_confidence} />
                <ScoreCard title="Skill Coverage" data={coach_scores.skill_coverage} />
                <ScoreCard title="Portfolio Strength" data={coach_scores.portfolio_strength} />
                <ScoreCard title="Market Readiness" data={coach_scores.market_readiness} />
              </>
            )}
          </div>
        </section>

        {/* Section 3: Digital Twin Timeline (Dark Product Surface) */}
        <section id="digital-twin">
          <DigitalTwinTimeline stages={digital_twin} careerGoal={career_goal} />
        </section>

        {/* Section 4: Country Market Dynamics */}
        <section id="country-intel">
          <CountryIntelligenceCard intelligence={country_intelligence as any} />
        </section>

        {/* Section 5: Universal Career Blueprint */}
        <section id="career-intel">
          <CareerIntelligenceCard careerName={career_goal} knowledge={career_knowledge} />
        </section>

        {/* Section 6: Skill Gap Matrix */}
        <section id="skill-gap">
          <SkillGapSection
            matchedSkills={readiness.matched_skills}
            missingSkills={readiness.missing_skills}
            recommendedSkills={readiness.recommended_next_skills}
            skillCoverage={readiness.skill_coverage}
            totalRequired={readiness.required_skills.length}
          />
        </section>

        {/* Section 7: Resume Analysis (if uploaded) */}
        {resumeData && (
          <section id="resume-analysis">
            <ResumeAnalysisCard resume={resumeData} />
          </section>
        )}

        {/* Section 8: Resume vs Role Fit (if available) */}
        {resume_match && (
          <section id="resume-match">
            <ResumeMatchSection resumeMatch={resume_match} />
          </section>
        )}

        {/* Section 9: Live Job Posting Matcher (Dark Surface) */}
        <section id="job-matcher">
          <JobDescriptionMatcher
            resumeData={resumeData}
            resumeText={resumeData?.text || profile.skills.join(', ')}
          />
        </section>

        {/* Section 10: GitHub Portfolio Signals (if available) */}
        {githubAnalysis && github_relevant && (
          <section id="github-intel">
            <GitHubAnalysisSection analysis={githubAnalysis} />
          </section>
        )}

        {/* Section 11: Career Roadmap */}
        <section id="roadmap">
          <RoadmapSection roadmap={roadmap} aiNotes={analysisResult.ai_roadmap} />
        </section>

        {/* Section 12: Action Plan */}
        <section id="action-plan">
          <ActionPlanSection actionPlan={action_plan} weeklyHours={profile.weekly_study_hours} />
        </section>

        {/* Recommended Alternative Roles */}
        {recommended_careers && recommended_careers.length > 0 && (
          <section className="space-y-6 pt-6 border-t border-hairline">
            <div className="space-y-1">
              <h3 className="font-serif text-3xl font-normal text-ink flex items-center gap-2">
                <SpikeMark className="h-4 w-4 fill-primary" />
                <span>Adjacent Alternative Roles</span>
              </h3>
              <p className="text-xs text-muted">
                Related career paths matching your verified competencies and academic domain
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
              {recommended_careers.map((rec, idx) => (
                <div
                  key={idx}
                  className="p-6 rounded-md border border-hairline bg-surface-card space-y-3 flex flex-col justify-between"
                >
                  <div className="space-y-1.5">
                    <div className="flex items-start justify-between gap-2">
                      <h4 className="font-serif text-xl font-normal text-ink">{rec.career}</h4>
                      <Badge variant="teal">{rec.fit_score}% Fit</Badge>
                    </div>
                    <p className="text-xs text-body line-clamp-2 leading-relaxed">{rec.explanation}</p>
                  </div>
                  <div className="pt-2 flex justify-end">
                    <button
                      type="button"
                      onClick={() => {
                        const updated = { ...profile, career_goal: rec.career }
                        executeAnalysis(updated)
                      }}
                      className="text-xs text-primary hover:underline font-medium flex items-center gap-1"
                    >
                      <span>Simulate This Role</span>
                      <ArrowRight className="h-3 w-3" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}
      </div>

      {/* Export Report Modal */}
      <ReportsExportModal
        isOpen={isExportModalOpen}
        onClose={() => setIsExportModalOpen(false)}
        analysis={analysisResult}
      />
    </div>
  )
}
