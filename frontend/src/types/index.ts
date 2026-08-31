export interface UserProfile {
  name: string
  age?: number | null
  degree: string
  branch: string
  current_year: string
  gpa: number
  skills: string[]
  projects: string[]
  certifications: string[]
  internships: string[]
  languages: string[]
  achievements: string[]
  weekly_study_hours: number
  career_goal: string
  target_country: string
}

export interface ResumeData {
  text: string
  name: string
  email: string
  phone: string
  linkedin: string
  github: string
  portfolio: string
  location: string
  age?: number | null
  degree: string
  branch: string
  university: string
  start_year?: number | null
  graduation_year?: number | null
  current_year: string
  gpa?: number | null
  current_designation: string
  extraction_status: 'Success' | 'Partial' | 'Failed'
  strength_score: number
  completeness_score: number
  industry_readiness_score: number
  ats_readiness_score: number
  overall_career_readiness_score: number
  skills: string[]
  skill_categories: Record<string, string[]>
  structured_projects: Array<{
    name?: string
    tech_stack?: string
    description?: string
    impact?: string
    role?: string
  }>
  structured_experience: Array<{
    role?: string
    company?: string
    duration?: string
    responsibilities?: string
    skills_used?: string
    achievements?: string
  }>
  structured_certifications: Array<{
    name?: string
    provider?: string
    completion_year?: string
  }>
  field_confidence: Record<string, number>
  insights: string[]
  detected_domain: string
  domain_confidence: number
  autofill?: Record<string, any>
}

export interface GitHubRepo {
  name: string
  description: string
  language: string
  stars: number
  forks: number
  watchers: number
  open_issues: number
  size_kb: number
  topics: string[]
  updated_at: string
  url: string
  project_type: string
  difficulty_level: string
  has_license: boolean
  has_readme_signal: boolean
  has_releases_signal: boolean
  quality_score: number
}

export interface GitHubAnalysis {
  username: string
  repository_count: number
  total_stars: number
  total_forks: number
  followers: number
  following: number
  public_gists: number
  years_active: number
  language_counts: Record<string, number>
  category_counts: Record<string, number>
  quality_distribution: Record<string, number>
  technology_stack_counts: Record<string, number>
  top_skills: string[]
  activity_level: string
  github_score: number
  project_quality_score: number
  portfolio_strength: string
  most_starred_repository: string
  most_used_language: string
  open_source_contribution_level: string
  suitable_careers: Array<{ career: string; why: string }>
  strengths: string[]
  weaknesses: string[]
  recommendations: string[]
  repos: GitHubRepo[]
}

export interface DigitalTwinStage {
  label: string
  role: string
  salary: string
  skills: string[]
  career_stage: string
  confidence: number
  probability: number
  salary_value: number
}

export interface ScorecardData {
  score: number
  label: string
  positives: string[]
  improvements: string[]
  why: string
}

export interface AnalysisResult {
  profile: UserProfile
  career_goal: string
  target_country: string
  readiness: {
    score: number
    label: string
    matched_skills: string[]
    missing_skills: string[]
    required_skills: string[]
    skill_coverage: number
    recommended_next_skills: string[]
    positive_factors: string[]
    improvement_factors: string[]
    why: string
  }
  success_probability: number
  coach_scores: {
    readiness: ScorecardData
    success_probability: ScorecardData
    ai_confidence: ScorecardData
    skill_coverage: ScorecardData
    portfolio_strength: ScorecardData
    market_readiness: ScorecardData
  }
  career_knowledge: {
    domain?: string
    description?: string
    core_skills?: string[]
    soft_skills?: string[]
    typical_tools?: string[]
    daily_responsibilities?: string[]
    kpis?: string[]
    ats_keywords?: string[]
    licensing_requirements?: string[]
    career_path?: string[]
    preferred_certifications?: string[]
    top_hiring_companies?: string[]
    interview_pattern?: string[]
    [key: string]: any
  }
  country_intelligence: {
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
    top_hiring_companies: string[]
    major_hiring_industries: string[]
    most_required_skills: string[]
    most_valuable_certifications: string[]
    cost_of_living: string
    interview_style: string
    future_outlook: string
    [key: string]: any
  }
  digital_twin: DigitalTwinStage[]
  roadmap: Array<{
    month: string
    focus: string
    tasks: string[]
    outcome: string
    weeks?: Array<{ week: string; milestone: string }>
  }>
  action_plan: Array<{
    week: string
    task: string
  }>
  resume_match?: {
    overall_match: number
    weighted_scores: Record<string, any>
    strengths: string[]
    weaknesses: string[]
    critical_missing_skills: string[]
    important_skills: string[]
    nice_to_have_skills: string[]
    improvement_suggestions: Array<{ suggestion: string; why: string }>
  } | null
  github_analysis?: GitHubAnalysis | null
  github_relevant: boolean
  ai_explanation?: string | null
  ai_future?: string | null
  ai_roadmap?: string | null
  recommended_careers: Array<{
    career: string
    domain: string
    fit_score: number
    explanation: string
    matched_signals: string[]
  }>
  generated_at: string
}

export interface JobDescriptionMatchResult {
  keyword_match: number
  semantic_match: number
  technical_match: number
  experience_match: number
  education_match: number
  certification_match: number
  hiring_recommendation: string
  matched_keywords: string[]
  missing_keywords: string[]
  highlighted_missing_keywords: string[]
}

export interface SavedProfileSnapshot {
  created_at: string
  name: string
  career_goal: string
  target_country: string
  readiness_score: number
  success_probability: number
}
