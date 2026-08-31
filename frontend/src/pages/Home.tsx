import React from 'react'
import { Link } from 'react-router-dom'
import { ArrowRight, Check } from 'lucide-react'
import { useCareer } from '../context/CareerContext'
import { Button } from '../components/ui/Button'
import { Card } from '../components/ui/Card'
import { Badge } from '../components/ui/Badge'
import { SpikeMark } from '../components/ui/Icons'

export const Home: React.FC = () => {
  const { countriesList, recentSnapshots } = useCareer()

  const stats = [
    { value: '3,527', label: 'Grounded Careers', note: '15+ Professional Domains' },
    { value: `${countriesList.length || 93}`, label: 'Global Markets', note: 'Localized Salary & Visa Data' },
    { value: '100%', label: 'Deterministic Scoring', note: 'Recruiter-Grade Logic' },
    { value: '5-Stage', label: 'Digital Career Twin', note: '1, 3, 5 & 10 Year Milestones' },
  ]

  const featureCards = [
    {
      title: 'Digital Career Twin Simulation',
      description:
        'Project your career trajectory 1, 3, 5, and 10 years forward with calibrated compensation targets, milestone competencies, and proof requirements.',
      tag: 'Core Simulation',
    },
    {
      title: 'Global Market & Visa Dynamics',
      description:
        'Explore local salary compensation bands (entry, mid, senior), hiring velocity, visa difficulty, and active employer ecosystems across 93 countries.',
      tag: '93 Markets',
    },
    {
      title: 'Deterministic Skill Gap Matrix',
      description:
        'Benchmark verified competencies against role benchmarks. Uncover exact missing requirements and prioritized highest-ROI next skills.',
      tag: 'Role Fit',
    },
    {
      title: 'Multi-Format Resume & ATS Parser',
      description:
        'Extract skills, experiences, projects, and credentials from PDF/DOCX resumes with recruiter-grade ATS scoring and automatic field autofill.',
      tag: 'ATS Proof',
    },
    {
      title: 'GitHub Portfolio Intelligence',
      description:
        'Evaluate public repository code quality, language distribution, commit frequency, and open-source impact for engineering roles.',
      tag: 'Code Signal',
    },
    {
      title: 'Context-Aware AI Career Mentor',
      description:
        'Receive personalized guidance grounded in your resume, target country, study hours, and salary milestones through multi-turn conversation.',
      tag: 'Mentorship',
    },
  ]

  const engines = [
    {
      name: 'Career Engine 3.5k',
      headline: 'Universal Taxonomy & Grounded Knowledge',
      description:
        'Spans 3,527 roles across Tech, Healthcare, Finance, Management, Design, Legal, and Aviation with exact ATS keywords, licensing, and KPIs.',
      cta: 'Explore Taxonomy',
      badge: 'Grounded Catalog',
    },
    {
      name: 'Global Market Intel',
      headline: '93 Country Compensation & Policy',
      description:
        'Dynamic currency normalization, visa complexity classifications, regional interview cultures, and real hiring employer ecosystems.',
      cta: 'Explore Markets',
      badge: '93 Countries',
    },
    {
      name: 'Twin Simulation Matrix',
      headline: '5-Stage Progression & Milestone Sprints',
      description:
        'Calculates transition probabilities, compensation curves, and weekly sprint tasks calibrated to your exact available study hours.',
      cta: 'Simulate Twin',
      badge: 'Simulation',
    },
  ]

  return (
    <div className="space-y-24 py-12 md:py-20 font-sans">
      {/* 1. HERO BAND (Editorial Grid) */}
      <section className="container">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-16 items-center">
          {/* Left Hero Column: Serif Display */}
          <div className="lg:col-span-7 space-y-6">
            <div className="inline-flex items-center gap-2 rounded-full border border-hairline bg-surface-card px-3.5 py-1 text-xs font-medium text-ink">
              <SpikeMark className="h-3.5 w-3.5 fill-primary" />
              <span>Grounded Career Intelligence Platform</span>
            </div>

            <h1 className="font-serif text-5xl sm:text-6xl md:text-7xl font-normal text-ink tracking-[-0.03em] leading-[1.04]">
              See the future version of your career before you live it.
            </h1>

            <p className="text-base sm:text-lg text-body leading-relaxed max-w-xl">
              Simulate your Digital Career Twin. Benchmark your resume against 3,500+ global careers, uncover exact skill deficits, explore localized salary bands, and follow a milestone learning roadmap.
            </p>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 pt-2">
              <Link to="/setup">
                <Button size="lg" variant="primary" className="w-full sm:w-auto gap-2 px-6">
                  <SpikeMark className="h-4 w-4 fill-white" />
                  <span>Build Your Digital Twin</span>
                </Button>
              </Link>

              <Link to="/setup">
                <Button size="lg" variant="secondary" className="w-full sm:w-auto">
                  <span>Enter Profile Manually</span>
                </Button>
              </Link>
            </div>

            <div className="flex flex-wrap items-center gap-4 pt-4 text-xs text-muted">
              <span className="flex items-center gap-1.5">
                <Check className="h-3.5 w-3.5 text-success" /> No signup required
              </span>
              <span>•</span>
              <span>100% Client-Safe Resume Parsing</span>
              <span>•</span>
              <span>Instant PDF Report Download</span>
            </div>
          </div>

          {/* Right Hero Column: Dark Product Mockup Card */}
          <div className="lg:col-span-5">
            <div className="rounded-xl border border-[#2e2b27] bg-[#181715] text-[#faf9f5] shadow-2xl p-6 space-y-5 font-mono text-xs">
              {/* Terminal Header */}
              <div className="flex items-center justify-between pb-3 border-b border-[#2e2b27]">
                <div className="flex items-center gap-2">
                  <span className="h-2.5 w-2.5 rounded-full bg-error" />
                  <span className="h-2.5 w-2.5 rounded-full bg-accent-amber" />
                  <span className="h-2.5 w-2.5 rounded-full bg-success" />
                  <span className="text-[11px] text-[#a09d96] ml-2">career-twin-engine // v2.0</span>
                </div>
                <Badge variant="coral" className="text-[10px] py-0 px-2">
                  LIVE
                </Badge>
              </div>

              {/* Code output lines */}
              <div className="space-y-2 text-[11px] leading-relaxed">
                <div className="text-[#a09d96]">
                  <span className="text-primary">$</span> simulate --target="AI Engineer" --country="USA"
                </div>
                <div className="text-success">
                  ✔ Loaded 3,527 roles taxonomy & 93 market matrices.
                </div>
                <div className="text-[#faf9f5] bg-[#252320] p-3 rounded-md border border-[#33312e] space-y-1">
                  <div className="text-[#a09d96]">// 5-STAGE TWIN TRAJECTORY PROJECTION</div>
                  <div>Current: Associate → 1yr: AI Engineer ($130k)</div>
                  <div>3yr: Senior AI Engineer ($175k) → 5yr: Staff ($225k)</div>
                  <div className="text-primary font-semibold">10yr: Principal AI Architect ($310k)</div>
                </div>
                <div className="text-[#a09d96]">
                  <span className="text-primary">$</span> evaluate-readiness --ats-strict
                </div>
                <div className="text-[#faf9f5]">
                  Readiness Score: <span className="text-success font-semibold">82%</span> | Skill Coverage: <span className="text-accent-teal font-semibold">14/18 Core</span>
                </div>
              </div>

              {/* Terminal Footer Action */}
              <div className="pt-2 border-t border-[#2e2b27] flex items-center justify-between text-[11px]">
                <span className="text-[#a09d96]">Ready for candidate input</span>
                <Link to="/setup" className="text-primary hover:underline flex items-center gap-1 font-sans">
                  <span>Launch Simulation</span>
                  <ArrowRight className="h-3 w-3" />
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 2. NUMERICAL STATS BAND */}
      <section className="container">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 p-8 rounded-xl border border-hairline bg-surface-card">
          {stats.map((st, idx) => (
            <div key={idx} className="space-y-1 text-center md:text-left">
              <div className="font-serif text-3xl sm:text-4xl font-normal text-ink tracking-tight">
                {st.value}
              </div>
              <div className="text-xs font-semibold text-ink">{st.label}</div>
              <div className="text-[11px] text-muted">{st.note}</div>
            </div>
          ))}
        </div>
      </section>

      {/* 3. FEATURE CARDS GRID */}
      <section className="container space-y-12">
        <div className="space-y-3 max-w-2xl">
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-primary">
            <SpikeMark className="h-3.5 w-3.5 fill-primary" />
            <span>Architecture & Capabilities</span>
          </div>
          <h2 className="font-serif text-4xl sm:text-5xl font-normal text-ink tracking-[-0.02em] leading-tight">
            Six interconnected intelligence engines built for every stage of your career.
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {featureCards.map((feat, idx) => (
            <Card key={idx} variant="cream" className="p-8 space-y-4 flex flex-col justify-between">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <Badge variant="outline" className="text-[11px]">
                    {feat.tag}
                  </Badge>
                  <SpikeMark className="h-3 w-3 fill-primary" />
                </div>
                <h3 className="font-serif text-2xl font-normal text-ink">
                  {feat.title}
                </h3>
                <p className="text-xs text-body leading-relaxed">
                  {feat.description}
                </p>
              </div>
            </Card>
          ))}
        </div>
      </section>

      {/* 4. MODEL / ENGINE COMPARISON */}
      <section className="container space-y-12">
        <div className="space-y-3 max-w-2xl">
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-primary">
            <SpikeMark className="h-3.5 w-3.5 fill-primary" />
            <span>Specialized Intelligence Engines</span>
          </div>
          <h2 className="font-serif text-4xl sm:text-5xl font-normal text-ink tracking-[-0.02em] leading-tight">
            Grounded data models engineered for career precision.
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {engines.map((eng, idx) => (
            <div
              key={idx}
              className="p-8 rounded-xl border border-hairline bg-canvas space-y-6 flex flex-col justify-between"
            >
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs font-semibold text-primary">
                    {eng.name}
                  </span>
                  <Badge variant="teal" className="text-[10px]">
                    {eng.badge}
                  </Badge>
                </div>
                <h3 className="font-serif text-2xl font-normal text-ink leading-snug">
                  {eng.headline}
                </h3>
                <p className="text-xs text-body leading-relaxed">
                  {eng.description}
                </p>
              </div>

              <div className="pt-4 border-t border-hairline">
                <Link to="/setup" className="text-xs font-medium text-primary hover:underline flex items-center gap-1.5">
                  <span>{eng.cta}</span>
                  <ArrowRight className="h-3.5 w-3.5" />
                </Link>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 5. RECENT SNAPSHOTS (if available) */}
      {recentSnapshots.length > 0 && (
        <section className="container space-y-6">
          <div className="flex items-center justify-between">
            <h3 className="font-serif text-2xl text-ink font-normal flex items-center gap-2">
              <SpikeMark className="h-4 w-4 fill-primary" />
              <span>Recent Career Twin Simulations</span>
            </h3>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {recentSnapshots.slice(0, 3).map((item, idx) => (
              <div
                key={idx}
                className="p-5 rounded-md border border-hairline bg-surface-card flex items-center justify-between gap-4 text-xs"
              >
                <div>
                  <div className="font-medium text-ink">{item.name || 'Candidate'}</div>
                  <div className="text-muted">
                    {item.career_goal} • {item.target_country}
                  </div>
                </div>
                <Badge variant="teal">
                  {item.readiness_score}% Readiness
                </Badge>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* 6. FULL-BLEED CORAL CALLOUT CARD */}
      <section className="container">
        <div className="rounded-xl bg-primary text-white p-8 md:p-14 space-y-6 shadow-xl">
          <div className="max-w-2xl space-y-3">
            <div className="flex items-center gap-2 text-xs font-mono uppercase tracking-wider text-white/80">
              <SpikeMark className="h-3.5 w-3.5 fill-white" />
              <span>Next Step in Your Career Trajectory</span>
            </div>
            <h2 className="font-serif text-3xl sm:text-4xl md:text-5xl font-normal text-white tracking-[-0.02em] leading-tight">
              Ready to generate your Digital Career Twin?
            </h2>
            <p className="text-sm md:text-base text-white/90 leading-relaxed">
              Upload your resume or fill in your background to compute recruiter readiness, benchmark local salaries, and generate your 5-stage milestone progression roadmap.
            </p>
          </div>

          <div className="pt-2">
            <Link to="/setup">
              <Button size="lg" variant="coral-inverted" className="gap-2 px-8">
                <SpikeMark className="h-4 w-4 fill-primary" />
                <span>Begin Free Simulation</span>
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}
