import React, { useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Upload,
  UserCheck,
  FileText,
  Clock,
  AlertCircle,
  Search,
} from 'lucide-react'
import { useCareer } from '../context/CareerContext'
import { Button } from '../components/ui/Button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/Card'
import { Input } from '../components/ui/Input'
import { Textarea } from '../components/ui/Textarea'
import { Select } from '../components/ui/Select'
import { Badge } from '../components/ui/Badge'
import { SpikeMark, GitHubIcon } from '../components/ui/Icons'

export const ProfileSetup: React.FC = () => {
  const navigate = useNavigate()
  const {
    profile,
    setProfile,
    resumeData,
    githubUsername,
    setGithubUsername,
    githubAnalysis,
    careersList,
    popularCareers,
    countriesList,
    isResumeParsing,
    isGitHubAnalyzing,
    isAnalyzing,
    resumeError,
    githubError,
    analysisError,
    handleResumeUpload,
    handleGitHubAnalysis,
    executeAnalysis,
  } = useCareer()

  const [method, setMethod] = useState<'upload' | 'manual'>('upload')
  const [careerSearch, setCareerSearch] = useState('')
  const [dragActive, setDragActive] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  // Stringified inputs
  const [skillsText, setSkillsText] = useState(profile.skills.join(', '))
  const [projectsText, setProjectsText] = useState(profile.projects.join('\n'))
  const [certificationsText, setCertificationsText] = useState(profile.certifications.join('\n'))
  const [internshipsText, setInternshipsText] = useState(profile.internships.join('\n'))
  const [languagesText, setLanguagesText] = useState(profile.languages.join(', '))
  const [achievementsText, setAchievementsText] = useState(profile.achievements.join('\n'))

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0]
      const data = await handleResumeUpload(file)
      if (data) {
        setSkillsText(data.skills.join(', '))
        if (data.structured_projects.length > 0) {
          setProjectsText(
            data.structured_projects
              .map((p) => `${p.name || ''} - ${p.tech_stack || ''}: ${p.description || ''}`)
              .join('\n')
          )
        }
        if (data.structured_certifications.length > 0) {
          setCertificationsText(
            data.structured_certifications
              .map((c) => `${c.name || ''} (${c.provider || ''})`)
              .join('\n')
          )
        }
        if (data.structured_experience.length > 0) {
          setInternshipsText(
            data.structured_experience
              .map((exp) => `${exp.role || ''} at ${exp.company || ''} (${exp.duration || ''})`)
              .join('\n')
          )
        }
      }
    }
  }

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0]
      const data = await handleResumeUpload(file)
      if (data) {
        setSkillsText(data.skills.join(', '))
      }
    }
  }

  const filteredCareers = careersList.filter((c) =>
    c.toLowerCase().includes(careerSearch.toLowerCase())
  )

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    const parseList = (text: string) =>
      text
        .split(/[\n,]/)
        .map((s) => s.trim())
        .filter(Boolean)

    const updatedProfile = {
      ...profile,
      skills: parseList(skillsText),
      projects: projectsText.split('\n').map((s) => s.trim()).filter(Boolean),
      certifications: certificationsText.split('\n').map((s) => s.trim()).filter(Boolean),
      internships: internshipsText.split('\n').map((s) => s.trim()).filter(Boolean),
      languages: parseList(languagesText),
      achievements: achievementsText.split('\n').map((s) => s.trim()).filter(Boolean),
    }

    setProfile(updatedProfile)
    const res = await executeAnalysis(updatedProfile)
    if (res) {
      navigate('/dashboard')
    }
  }

  return (
    <div className="container max-w-4xl py-12 px-4 space-y-12 font-sans">
      {/* Editorial Page Header */}
      <div className="space-y-3 text-center max-w-2xl mx-auto">
        <div className="flex items-center justify-center gap-2 text-xs font-mono uppercase tracking-wider text-primary">
          <SpikeMark className="h-3.5 w-3.5 fill-primary" />
          <span>Profile Ingestion & Configuration</span>
        </div>
        <h1 className="font-serif text-4xl sm:text-5xl font-normal text-ink tracking-[-0.03em]">
          Configure your career profile.
        </h1>
        <p className="text-sm text-muted leading-relaxed">
          Upload your resume for instant deterministic extraction, or manually customize your background, target role, and regional market.
        </p>
      </div>

      {/* Creation Mode Tabs */}
      <div className="flex justify-center">
        <div className="inline-flex rounded-md bg-surface-card p-1 border border-hairline">
          <button
            type="button"
            onClick={() => setMethod('upload')}
            className={`flex items-center gap-2 px-5 py-2 rounded-md text-xs sm:text-sm font-medium transition-all ${
              method === 'upload'
                ? 'bg-canvas text-ink shadow-xs font-semibold'
                : 'text-muted hover:text-ink'
            }`}
          >
            <Upload className="h-3.5 w-3.5" />
            <span>Upload Resume (Recommended)</span>
          </button>
          <button
            type="button"
            onClick={() => setMethod('manual')}
            className={`flex items-center gap-2 px-5 py-2 rounded-md text-xs sm:text-sm font-medium transition-all ${
              method === 'manual'
                ? 'bg-canvas text-ink shadow-xs font-semibold'
                : 'text-muted hover:text-ink'
            }`}
          >
            <UserCheck className="h-3.5 w-3.5" />
            <span>Manual Input</span>
          </button>
        </div>
      </div>

      {/* Resume Upload Dropzone */}
      {method === 'upload' && (
        <div className="p-8 md:p-10 rounded-xl border border-dashed border-primary/40 bg-surface-card text-center space-y-4">
          <div
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            className="flex flex-col items-center justify-center p-6 space-y-3"
          >
            <div className="p-3 rounded-full bg-canvas border border-hairline text-primary">
              <Upload className="h-6 w-6" />
            </div>
            <h3 className="font-serif text-2xl font-normal text-ink">
              Drag and drop your resume file here
            </h3>
            <p className="text-xs text-muted max-w-sm leading-relaxed">
              Supports PDF, DOCX, and TXT files. Deterministic ATS parser extracts education, experience, and skills in seconds.
            </p>

            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.docx,.txt"
              onChange={handleFileChange}
              className="hidden"
            />

            <div className="pt-2">
              <Button
                type="button"
                variant="primary"
                size="default"
                onClick={() => fileInputRef.current?.click()}
                isLoading={isResumeParsing}
                className="gap-2 px-6"
              >
                <FileText className="h-4 w-4" />
                <span>Select Resume File</span>
              </Button>
            </div>
          </div>

          {resumeError && (
            <div className="p-3.5 rounded-md bg-error/15 border border-error/30 text-xs font-medium text-error max-w-md mx-auto flex items-center gap-2">
              <AlertCircle className="h-4 w-4 shrink-0 text-error" />
              <span>{resumeError}</span>
            </div>
          )}

          {resumeData && (
            <div className="p-4 rounded-md bg-canvas border border-hairline text-xs space-y-1 text-left max-w-lg mx-auto">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-ink">
                  {resumeData.name || 'Candidate Resume'}
                </span>
                <Badge variant="teal">Parsed {resumeData.skills.length} Skills</Badge>
              </div>
              <p className="text-muted">
                Domain: <strong className="text-ink">{resumeData.detected_domain}</strong> • Strength: {resumeData.strength_score}% • ATS: {resumeData.ats_readiness_score}%
              </p>
            </div>
          )}
        </div>
      )}

      {/* Main Profile Configuration Form */}
      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Step 1: Target Career & Region */}
        <Card variant="canvas">
          <CardHeader className="bg-surface-soft border-b border-hairline pb-5">
            <CardTitle className="text-xl md:text-2xl text-ink flex items-center gap-2">
              <SpikeMark className="h-3.5 w-3.5 fill-primary" />
              <span>Target Role & Country Preference</span>
            </CardTitle>
            <CardDescription>
              Select from 3,527 grounded careers and 93 regional market matrices
            </CardDescription>
          </CardHeader>

          <CardContent className="p-6 md:p-8 space-y-5">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              {/* Career Goal Search */}
              <div className="space-y-2">
                <label className="text-xs font-medium text-ink flex items-center justify-between">
                  <span>Target Career Goal</span>
                  <span className="text-[11px] text-muted">{careersList.length || 3527}+ roles catalog</span>
                </label>
                <div className="space-y-2">
                  <div className="relative">
                    <Search className="absolute left-3 top-2.5 h-4 w-4 text-muted-soft" />
                    <input
                      type="text"
                      placeholder="Search career (e.g. AI Engineer, Product Manager)..."
                      value={careerSearch}
                      onChange={(e) => setCareerSearch(e.target.value)}
                      className="h-10 w-full rounded-md border border-hairline bg-canvas pl-9 pr-3 text-xs text-ink focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20"
                    />
                  </div>

                  <Select
                    value={profile.career_goal}
                    onChange={(e) => setProfile({ ...profile, career_goal: e.target.value })}
                  >
                    {(careerSearch ? filteredCareers : careersList).slice(0, 100).map((c) => (
                      <option key={c} value={c}>
                        {c}
                      </option>
                    ))}
                  </Select>

                  {/* Popular Pills */}
                  <div className="flex flex-wrap gap-1.5 pt-1">
                    {popularCareers.slice(0, 5).map((pop) => (
                      <button
                        key={pop}
                        type="button"
                        onClick={() => setProfile({ ...profile, career_goal: pop })}
                        className={`text-[11px] px-2.5 py-0.5 rounded-full border transition-colors ${
                          profile.career_goal === pop
                            ? 'bg-primary text-white border-primary'
                            : 'bg-surface-card text-muted hover:text-ink border-hairline'
                        }`}
                      >
                        {pop}
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              {/* Country Selection */}
              <div className="space-y-2">
                <Select
                  label="Target Regional Market"
                  value={profile.target_country}
                  onChange={(e) => setProfile({ ...profile, target_country: e.target.value })}
                  options={countriesList.length > 0 ? countriesList : ['USA', 'India', 'Germany', 'Canada', 'United Kingdom']}
                />
                <p className="text-xs text-muted">
                  Governs local salary compensation benchmarks, currency conversions, and visa policies.
                </p>

                {/* Weekly Study Hours Slider */}
                <div className="space-y-2 pt-4">
                  <div className="flex items-center justify-between text-xs font-medium text-ink">
                    <span className="flex items-center gap-1.5">
                      <Clock className="h-3.5 w-3.5 text-primary" />
                      <span>Weekly Upskilling Effort Commitment:</span>
                    </span>
                    <span className="font-mono font-semibold text-primary">
                      {profile.weekly_study_hours} Hours / Week
                    </span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="40"
                    value={profile.weekly_study_hours}
                    onChange={(e) =>
                      setProfile({ ...profile, weekly_study_hours: parseInt(e.target.value) || 0 })
                    }
                    className="w-full h-1.5 bg-hairline rounded-lg appearance-none cursor-pointer accent-primary"
                  />
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Step 2: Candidate Background */}
        <Card variant="canvas">
          <CardHeader className="bg-surface-soft border-b border-hairline pb-5">
            <CardTitle className="text-xl md:text-2xl text-ink flex items-center gap-2">
              <SpikeMark className="h-3.5 w-3.5 fill-primary" />
              <span>Academic & Professional Credentials</span>
            </CardTitle>
            <CardDescription>Refine candidate personal profile and education</CardDescription>
          </CardHeader>

          <CardContent className="p-6 md:p-8 space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
              <Input
                label="Candidate Name"
                placeholder="e.g. Alex Smith"
                value={profile.name}
                onChange={(e) => setProfile({ ...profile, name: e.target.value })}
              />

              <Input
                label="Degree / Highest Qualification"
                placeholder="e.g. B.Tech Computer Science, MS"
                value={profile.degree}
                onChange={(e) => setProfile({ ...profile, degree: e.target.value })}
              />

              <Input
                label="Branch / Major"
                placeholder="e.g. Computer Science, AI, Finance"
                value={profile.branch}
                onChange={(e) => setProfile({ ...profile, branch: e.target.value })}
              />

              <Select
                label="Current Seniority / Stage"
                value={profile.current_year}
                onChange={(e) => setProfile({ ...profile, current_year: e.target.value })}
                options={[
                  'Not Specified',
                  '1st Year Student',
                  '2nd Year Student',
                  '3rd Year Student',
                  '4th Year Student',
                  'Recent Graduate',
                  'Working Professional (1-3 Yrs)',
                  'Mid-Level Professional (3-6 Yrs)',
                  'Senior Professional (6+ Yrs)',
                ]}
              />

              <Input
                label="GPA / CGPA (Optional)"
                type="number"
                step="0.1"
                placeholder="e.g. 3.8 or 8.5"
                value={profile.gpa || ''}
                onChange={(e) => setProfile({ ...profile, gpa: parseFloat(e.target.value) || 0 })}
              />

              <Input
                label="Age (Optional)"
                type="number"
                placeholder="e.g. 24"
                value={profile.age || ''}
                onChange={(e) => setProfile({ ...profile, age: parseInt(e.target.value) || null })}
              />
            </div>
          </CardContent>
        </Card>

        {/* Step 3: Skills & Artifacts */}
        <Card variant="canvas">
          <CardHeader className="bg-surface-soft border-b border-hairline pb-5">
            <CardTitle className="text-xl md:text-2xl text-ink flex items-center gap-2">
              <SpikeMark className="h-3.5 w-3.5 fill-primary" />
              <span>Skills, Projects & Practical Proof</span>
            </CardTitle>
            <CardDescription>Verified competencies used to compute exact role fit</CardDescription>
          </CardHeader>

          <CardContent className="p-6 md:p-8 space-y-4">
            <Textarea
              label="Technical & Core Competencies (Comma or Newline Separated)"
              placeholder="e.g. Python, Machine Learning, PyTorch, FastAPI, Docker, SQL, Kubernetes, React"
              value={skillsText}
              onChange={(e) => setSkillsText(e.target.value)}
              rows={3}
            />

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Textarea
                label="Projects (One per line)"
                placeholder="e.g. Autonomous Agent Framework - Python, LLMs, Vector DBs: Built agentic workflow tool with 99% task completion"
                value={projectsText}
                onChange={(e) => setProjectsText(e.target.value)}
                rows={3}
              />

              <Textarea
                label="Experience / Internships (One per line)"
                placeholder="e.g. AI Engineering Intern at Acme Corp (6 months): Deployed RAG search pipeline reducing latency by 40%"
                value={internshipsText}
                onChange={(e) => setInternshipsText(e.target.value)}
                rows={3}
              />

              <Textarea
                label="Certifications (One per line)"
                placeholder="e.g. AWS Certified Machine Learning Specialty (Amazon, 2025)"
                value={certificationsText}
                onChange={(e) => setCertificationsText(e.target.value)}
                rows={2}
              />

              <Textarea
                label="Achievements & Honors (One per line)"
                placeholder="e.g. 1st Place National Hackathon 2025; IEEE Paper Publication"
                value={achievementsText}
                onChange={(e) => setAchievementsText(e.target.value)}
                rows={2}
              />
            </div>
          </CardContent>
        </Card>

        {/* Step 4: GitHub Verification */}
        <Card variant="canvas">
          <CardHeader className="bg-surface-soft border-b border-hairline pb-5">
            <CardTitle className="text-xl md:text-2xl text-ink flex items-center gap-2">
              <GitHubIcon className="h-4 w-4 text-ink" />
              <span>GitHub Portfolio Signal (Optional)</span>
            </CardTitle>
            <CardDescription>Connect public code repositories for code quality verification</CardDescription>
          </CardHeader>

          <CardContent className="p-6 md:p-8 space-y-4">
            <div className="flex flex-col sm:flex-row items-center gap-3">
              <Input
                placeholder="GitHub Username (e.g. octocat)"
                value={githubUsername}
                onChange={(e) => setGithubUsername(e.target.value)}
                className="flex-1"
              />
              <Button
                type="button"
                variant="secondary"
                onClick={() => handleGitHubAnalysis()}
                isLoading={isGitHubAnalyzing}
                className="w-full sm:w-auto shrink-0 gap-2"
              >
                <GitHubIcon className="h-3.5 w-3.5" />
                <span>Verify GitHub</span>
              </Button>
            </div>

            {githubError && <p className="text-xs text-error font-medium">{githubError}</p>}

            {githubAnalysis && (
              <div className="p-4 rounded-md bg-success/15 border border-success/30 text-xs text-[#226634] dark:text-[#5db872] flex items-center gap-2">
                <span>
                  GitHub Score: {githubAnalysis.github_score}% • {githubAnalysis.repository_count} repos verified • Quality: {githubAnalysis.project_quality_score}%
                </span>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Submit Actions */}
        {analysisError && (
          <div className="p-4 rounded-md bg-error/15 border border-error/30 text-xs font-medium text-error flex items-center gap-2">
            <AlertCircle className="h-4 w-4 shrink-0 text-error" />
            <span>{analysisError}</span>
          </div>
        )}

        <div className="flex justify-center pt-4">
          <Button
            type="submit"
            size="lg"
            variant="primary"
            isLoading={isAnalyzing}
            className="w-full sm:w-auto px-10 text-base gap-2 shadow-lg"
          >
            <SpikeMark className="h-4 w-4 fill-white" />
            <span>Generate Digital Career Twin</span>
          </Button>
        </div>
      </form>
    </div>
  )
}
