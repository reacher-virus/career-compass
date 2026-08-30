import React, { createContext, useContext, useEffect, useState } from 'react'
import type {
  AnalysisResult,
  GitHubAnalysis,
  ResumeData,
  SavedProfileSnapshot,
  UserProfile,
} from '../types'
import {
  analyzeGitHub,
  fetchCareers,
  fetchCountries,
  fetchRecentProfiles,
  parseResume,
  runAnalysis,
} from '../api/client'

const defaultProfile: UserProfile = {
  name: '',
  age: null,
  degree: '',
  branch: '',
  current_year: 'Not Specified',
  gpa: 0,
  skills: [],
  projects: [],
  certifications: [],
  internships: [],
  languages: [],
  achievements: [],
  weekly_study_hours: 10,
  career_goal: 'AI Engineer',
  target_country: 'USA',
}

interface CareerContextType {
  profile: UserProfile
  setProfile: React.Dispatch<React.SetStateAction<UserProfile>>
  resumeData: ResumeData | null
  setResumeData: React.Dispatch<React.SetStateAction<ResumeData | null>>
  githubUsername: string
  setGithubUsername: (val: string) => void
  githubAnalysis: GitHubAnalysis | null
  setGithubAnalysis: React.Dispatch<React.SetStateAction<GitHubAnalysis | null>>
  analysisResult: AnalysisResult | null
  setAnalysisResult: React.Dispatch<React.SetStateAction<AnalysisResult | null>>
  careersList: string[]
  careersDomains: Record<string, string[]>
  popularCareers: string[]
  countriesList: string[]
  isLoadingMetadata: boolean
  isAnalyzing: boolean
  isResumeParsing: boolean
  isGitHubAnalyzing: boolean
  resumeError: string | null
  githubError: string | null
  analysisError: string | null
  theme: 'light' | 'dark'
  toggleTheme: () => void
  recentSnapshots: SavedProfileSnapshot[]
  refreshRecentSnapshots: () => Promise<void>
  executeAnalysis: (customProfile?: UserProfile) => Promise<AnalysisResult | null>
  handleResumeUpload: (file: File) => Promise<ResumeData | null>
  handleGitHubAnalysis: (username?: string) => Promise<GitHubAnalysis | null>
  resetSession: () => void
}

const CareerContext = createContext<CareerContextType | undefined>(undefined)

export const CareerProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [profile, setProfile] = useState<UserProfile>(defaultProfile)
  const [resumeData, setResumeData] = useState<ResumeData | null>(null)
  const [githubUsername, setGithubUsername] = useState<string>('')
  const [githubAnalysis, setGithubAnalysis] = useState<GitHubAnalysis | null>(null)
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null)

  const [careersList, setCareersList] = useState<string[]>([])
  const [careersDomains, setCareersDomains] = useState<Record<string, string[]>>({})
  const [popularCareers, setPopularCareers] = useState<string[]>([])
  const [countriesList, setCountriesList] = useState<string[]>([])
  const [recentSnapshots, setRecentSnapshots] = useState<SavedProfileSnapshot[]>([])

  const [isLoadingMetadata, setIsLoadingMetadata] = useState<boolean>(true)
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false)
  const [isResumeParsing, setIsResumeParsing] = useState<boolean>(false)
  const [isGitHubAnalyzing, setIsGitHubAnalyzing] = useState<boolean>(false)

  const [resumeError, setResumeError] = useState<string | null>(null)
  const [githubError, setGithubError] = useState<string | null>(null)
  const [analysisError, setAnalysisError] = useState<string | null>(null)

  const [theme, setTheme] = useState<'light' | 'dark'>('light')

  useEffect(() => {
    document.documentElement.classList.remove('dark')
    localStorage.removeItem('careertwin_theme')
  }, [])

  const toggleTheme = () => {}

  // Load initial careers & countries metadata
  useEffect(() => {
    let isMounted = true
    async function loadMeta() {
      try {
        setIsLoadingMetadata(true)
        const [cData, cntData, snapData] = await Promise.allSettled([
          fetchCareers(),
          fetchCountries(),
          fetchRecentProfiles(),
        ])

        if (!isMounted) return

        if (cData.status === 'fulfilled') {
          setCareersList(cData.value.careers || [])
          setCareersDomains(cData.value.domains || {})
          setPopularCareers(cData.value.popular || [])
        }
        if (cntData.status === 'fulfilled') {
          setCountriesList(cntData.value.countries || [])
        }
        if (snapData.status === 'fulfilled') {
          setRecentSnapshots(snapData.value || [])
        }
      } catch (err) {
        console.error('Failed to load initial metadata', err)
      } finally {
        if (isMounted) setIsLoadingMetadata(false)
      }
    }
    loadMeta()
    return () => {
      isMounted = false
    }
  }, [])

  const refreshRecentSnapshots = async () => {
    try {
      const data = await fetchRecentProfiles()
      setRecentSnapshots(data)
    } catch (err) {
      console.error('Failed to refresh snapshots', err)
    }
  }

  const handleResumeUpload = async (file: File): Promise<ResumeData | null> => {
    setIsResumeParsing(true)
    setResumeError(null)
    try {
      const data = await parseResume(file)
      setResumeData(data)

      // Auto-fill profile from resume data
      setProfile((prev) => ({
        ...prev,
        name: data.name || prev.name,
        age: data.age ?? prev.age,
        degree: data.degree || prev.degree,
        branch: data.branch || prev.branch,
        current_year: data.current_year !== 'Not Specified' ? data.current_year : prev.current_year,
        gpa: data.gpa ?? prev.gpa,
        skills: data.skills.length > 0 ? data.skills : prev.skills,
        projects:
          data.structured_projects.length > 0
            ? data.structured_projects.map((p) => `${p.name || ''} - ${p.tech_stack || ''}: ${p.description || ''}`)
            : prev.projects,
        certifications:
          data.structured_certifications.length > 0
            ? data.structured_certifications.map((c) => `${c.name || ''} (${c.provider || ''})`)
            : prev.certifications,
        internships:
          data.structured_experience.length > 0
            ? data.structured_experience.map((e) => `${e.role || ''} at ${e.company || ''} (${e.duration || ''})`)
            : prev.internships,
      }))

      // If GitHub profile was found in resume and not analyzed yet, trigger analyze
      if (data.github && !githubAnalysis) {
        const ghUser = data.github.replace(/^https?:\/\/(www\.)?github\.com\//, '').replace(/\/$/, '')
        if (ghUser) {
          setGithubUsername(ghUser)
          handleGitHubAnalysis(ghUser).catch((e) => console.warn('GitHub auto-analysis failed:', e))
        }
      }

      return data
    } catch (err: any) {
      const msg = err.response?.data?.detail || err.message || 'Failed to parse resume.'
      setResumeError(msg)
      return null
    } finally {
      setIsResumeParsing(false)
    }
  }

  const handleGitHubAnalysis = async (usernameOverride?: string): Promise<GitHubAnalysis | null> => {
    const targetUser = (usernameOverride || githubUsername).trim()
    if (!targetUser) {
      setGithubError('Please enter a GitHub username.')
      return null
    }

    setIsGitHubAnalyzing(true)
    setGithubError(null)
    try {
      const data = await analyzeGitHub(targetUser)
      setGithubAnalysis(data)
      setGithubUsername(targetUser)
      return data
    } catch (err: any) {
      const msg = err.response?.data?.detail || err.message || 'Failed to analyze GitHub profile.'
      setGithubError(msg)
      return null
    } finally {
      setIsGitHubAnalyzing(false)
    }
  }

  const executeAnalysis = async (customProfile?: UserProfile): Promise<AnalysisResult | null> => {
    const activeProfile = customProfile || profile
    setIsAnalyzing(true)
    setAnalysisError(null)
    try {
      const result = await runAnalysis({
        profile: activeProfile,
        resume: resumeData,
        github_username: githubUsername || undefined,
        github_analysis: githubAnalysis,
      })
      setAnalysisResult(result)
      return result
    } catch (err: any) {
      const msg = err.response?.data?.detail || err.message || 'Analysis failed. Please check inputs.'
      setAnalysisError(msg)
      return null
    } finally {
      setIsAnalyzing(false)
    }
  }

  const resetSession = () => {
    setProfile(defaultProfile)
    setResumeData(null)
    setGithubUsername('')
    setGithubAnalysis(null)
    setAnalysisResult(null)
    setResumeError(null)
    setGithubError(null)
    setAnalysisError(null)
  }

  return (
    <CareerContext.Provider
      value={{
        profile,
        setProfile,
        resumeData,
        setResumeData,
        githubUsername,
        setGithubUsername,
        githubAnalysis,
        setGithubAnalysis,
        analysisResult,
        setAnalysisResult,
        careersList,
        careersDomains,
        popularCareers,
        countriesList,
        isLoadingMetadata,
        isAnalyzing,
        isResumeParsing,
        isGitHubAnalyzing,
        resumeError,
        githubError,
        analysisError,
        theme,
        toggleTheme,
        recentSnapshots,
        refreshRecentSnapshots,
        executeAnalysis,
        handleResumeUpload,
        handleGitHubAnalysis,
        resetSession,
      }}
    >
      {children}
    </CareerContext.Provider>
  )
}

export const useCareer = () => {
  const context = useContext(CareerContext)
  if (!context) {
    throw new Error('useCareer must be used within a CareerProvider')
  }
  return context
}
