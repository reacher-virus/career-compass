import axios from 'axios'
import type {
  AnalysisResult,
  GitHubAnalysis,
  JobDescriptionMatchResult,
  ResumeData,
  SavedProfileSnapshot,
  UserProfile,
} from '../types'

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export async function fetchHealth() {
  const res = await api.get('/health')
  return res.data
}

export async function fetchCareers(): Promise<{
  total_careers: number
  careers: string[]
  domains: Record<string, string[]>
  popular: string[]
}> {
  const res = await api.get('/careers')
  return res.data
}

export async function searchCareers(query: string): Promise<string[]> {
  const res = await api.get('/careers/search', { params: { q: query } })
  return res.data
}

export async function fetchCareerDetails(careerName: string) {
  const res = await api.get(`/careers/details/${encodeURIComponent(careerName)}`)
  return res.data
}

export async function fetchCountries(): Promise<{
  countries: string[]
  total: number
}> {
  const res = await api.get('/countries')
  return res.data
}

export async function fetchCountryIntelligence(country: string, career: string) {
  const res = await api.get('/countries/intelligence', {
    params: { country, career },
  })
  return res.data
}

export async function parseResume(file: File): Promise<ResumeData> {
  const formData = new FormData()
  formData.append('file', file)
  const res = await api.post('/resume/parse', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return res.data
}

export async function matchJobDescription(payload: {
  resume_text?: string
  resume_data?: any
  job_description_text: string
}): Promise<JobDescriptionMatchResult> {
  const res = await api.post('/resume/match-jd', payload)
  return res.data
}

export async function analyzeGitHub(username: string): Promise<GitHubAnalysis> {
  const res = await api.get(`/github/${encodeURIComponent(username)}`)
  return res.data
}

export async function runAnalysis(payload: {
  profile: UserProfile
  resume?: ResumeData | null
  github_username?: string
  github_analysis?: GitHubAnalysis | null
}): Promise<AnalysisResult> {
  const res = await api.post('/analysis', payload)
  return res.data
}

export async function fetchMentorQuestions(): Promise<{
  quick_prompts: string[]
  library: string[]
  total_questions: number
}> {
  const res = await api.get('/mentor/questions')
  return res.data
}

export async function sendMentorMessage(payload: {
  question: string
  context: Record<string, any>
  history: Array<{ role: string; content: string }>
}): Promise<{ answer: string }> {
  const res = await api.post('/mentor/chat', payload)
  return res.data
}

export async function exportPdfReport(reportData: any): Promise<Blob> {
  const res = await api.post('/reports/pdf', reportData, {
    responseType: 'blob',
  })
  return res.data
}

export async function saveProfileSnapshot(payload: {
  profile: UserProfile
  analysis: Record<string, any>
  success_probability: number
}): Promise<{ status: string; message: string }> {
  const res = await api.post('/profiles/save', payload)
  return res.data
}

export async function fetchRecentProfiles(): Promise<SavedProfileSnapshot[]> {
  const res = await api.get('/profiles/recent')
  return res.data
}

export async function submitFeedback(payload: {
  feedback_type: string
  rating: number
  subject: string
  message: string
  email?: string
}) {
  const res = await api.post('/feedback', payload)
  return res.data
}
