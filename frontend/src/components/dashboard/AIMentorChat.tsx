import React, { useState, useEffect, useRef } from 'react'
import { Send, X, Trash2, Copy, Check, Terminal } from 'lucide-react'
import { useCareer } from '../../context/CareerContext'
import { sendMentorMessage, fetchMentorQuestions } from '../../api/client'
import { Button } from '../ui/Button'
import { Badge } from '../ui/Badge'
import { SpikeMark } from '../ui/Icons'

interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  timestamp?: string
}

export const AIMentorChat: React.FC = () => {
  const { profile, resumeData, githubAnalysis, analysisResult } = useCareer()
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: 'assistant',
      content: `Hello ${profile.name || 'there'}! I am your AI Career Mentor. I have full context on your target career (${profile.career_goal || 'Software Engineer'}), readiness scores, resume, and skill gaps. How can I assist you today?`,
    },
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [quickPrompts, setQuickPrompts] = useState<string[]>([])
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    fetchMentorQuestions()
      .then((res) => {
        setQuickPrompts(res.quick_prompts || [])
      })
      .catch((e) => console.warn('Could not load mentor questions', e))
  }, [])

  useEffect(() => {
    if (isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }
  }, [messages, isOpen])

  const handleSend = async (questionText?: string) => {
    const text = (questionText || input).trim()
    if (!text || isLoading) return

    const userMsg: ChatMessage = { role: 'user', content: text }
    const updatedMessages = [...messages, userMsg]
    setMessages(updatedMessages)
    setInput('')
    setIsLoading(true)

    // Build context object
    const mentorContext = {
      name: profile.name || 'there',
      career_goal: profile.career_goal || 'Software Engineer',
      country: profile.target_country || 'USA',
      weekly_study_hours: profile.weekly_study_hours || 10,
      resume_strength: resumeData?.strength_score,
      resume_skills: resumeData?.skills || profile.skills,
      projects: resumeData?.structured_projects?.map((p) => p.name || '') || profile.projects,
      experience: resumeData?.structured_experience?.map((e) => e.role || '') || profile.internships,
      certifications: resumeData?.structured_certifications?.map((c) => c.name || '') || profile.certifications,
      github_score: githubAnalysis?.github_score,
      github_recommendations: githubAnalysis?.recommendations || [],
      country_demand: analysisResult?.country_intelligence?.demand_level || '',
      country_skills: analysisResult?.country_intelligence?.most_required_skills || [],
      roadmap: analysisResult?.roadmap || [],
      missing_skills: analysisResult?.readiness?.missing_skills || [],
      resume_match: analysisResult?.resume_match?.overall_match,
      critical_missing: analysisResult?.readiness?.missing_skills?.slice(0, 3) || [],
      important_skills: analysisResult?.readiness?.missing_skills?.slice(3, 7) || [],
      career_knowledge: analysisResult?.career_knowledge || {},
      detected_domain: resumeData?.detected_domain || analysisResult?.career_knowledge?.domain || 'Technology',
    }

    try {
      const res = await sendMentorMessage({
        question: text,
        context: mentorContext,
        history: updatedMessages.map((m) => ({ role: m.role, content: m.content })),
      })
      setMessages((prev) => [...prev, { role: 'assistant', content: res.answer }])
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: 'Sorry, I encountered an issue generating advice. Please try asking again.',
        },
      ])
    } finally {
      setIsLoading(false)
    }
  }

  const handleCopy = (text: string, index: number) => {
    navigator.clipboard.writeText(text)
    setCopiedIndex(index)
    setTimeout(() => setCopiedIndex(null), 2000)
  }

  const handleClear = () => {
    setMessages([
      {
        role: 'assistant',
        content: `Conversation reset. Ask me anything regarding your ${profile.career_goal || 'target career'} trajectory or resume improvements.`,
      },
    ])
  }

  return (
    <>
      {/* Floating launcher button in signature Claude coral */}
      <div className="fixed bottom-6 right-6 z-50">
        <button
          type="button"
          onClick={() => setIsOpen(!isOpen)}
          className="flex items-center gap-2.5 px-4 py-3 rounded-full bg-[#cc785c] text-white shadow-xl hover:bg-[#a9583e] active:scale-95 transition-all duration-150 focus:outline-none focus:ring-4 focus:ring-[#cc785c]/20"
          aria-label="Open AI Mentor"
        >
          <SpikeMark className="h-4 w-4 fill-white" />
          <span className="text-sm font-medium hidden sm:inline">AI Career Mentor</span>
          <span className="h-2 w-2 rounded-full bg-[#5db872]" />
        </button>
      </div>

      {/* Floating Chat Window (Dark Product Surface #181715) */}
      {isOpen && (
        <div className="fixed bottom-20 right-4 sm:right-6 z-50 w-[94vw] sm:w-[440px] h-[580px] max-h-[85vh] rounded-xl border border-[#2e2b27] bg-[#181715] text-[#faf9f5] shadow-2xl flex flex-col overflow-hidden animate-in slide-in-from-bottom-3 duration-200">
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-[#2e2b27] bg-[#1f1e1b]">
            <div className="flex items-center gap-2.5">
              <div className="p-1.5 rounded-md bg-[#252320] text-[#cc785c]">
                <SpikeMark className="h-4 w-4 fill-[#cc785c]" />
              </div>
              <div>
                <h3 className="font-serif text-lg text-[#faf9f5] font-normal leading-tight">
                  AI Career Mentor
                </h3>
                <span className="text-[11px] text-[#a09d96] line-clamp-1">
                  Target: {profile.career_goal || 'Software Engineer'} • {profile.target_country || 'USA'}
                </span>
              </div>
            </div>
            <div className="flex items-center gap-1">
              <button
                type="button"
                onClick={handleClear}
                title="Clear Chat"
                className="p-1.5 rounded-md text-[#a09d96] hover:bg-[#252320] hover:text-[#faf9f5] transition-colors"
              >
                <Trash2 className="h-4 w-4" />
              </button>
              <button
                type="button"
                onClick={() => setIsOpen(false)}
                className="p-1.5 rounded-md text-[#a09d96] hover:bg-[#252320] hover:text-[#faf9f5] transition-colors"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          </div>

          {/* Quick Prompts Carousel */}
          <div className="flex items-center gap-1.5 overflow-x-auto p-2.5 border-b border-[#2e2b27] bg-[#1f1e1b] scrollbar-none">
            {quickPrompts.slice(0, 5).map((prompt, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => handleSend(prompt)}
                disabled={isLoading}
                className="whitespace-nowrap px-3 py-1 rounded-full bg-[#252320] border border-[#33312e] text-[11px] text-[#faf9f5] hover:border-[#cc785c] hover:text-[#cc785c] transition-colors shrink-0"
              >
                {prompt}
              </button>
            ))}
          </div>

          {/* Messages Log */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3.5 dark-scroll">
            {messages.map((msg, idx) => {
              const isUser = msg.role === 'user'
              return (
                <div key={idx} className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}>
                  <div
                    className={`max-w-[88%] rounded-lg p-3.5 text-xs leading-relaxed ${
                      isUser
                        ? 'bg-[#cc785c] text-white rounded-br-xs font-medium'
                        : 'bg-[#252320] border border-[#33312e] text-[#faf9f5] rounded-bl-xs'
                    }`}
                  >
                    <div className="whitespace-pre-wrap">{msg.content}</div>
                  </div>

                  {!isUser && (
                    <button
                      type="button"
                      onClick={() => handleCopy(msg.content, idx)}
                      className="mt-1 ml-1 flex items-center gap-1 text-[10px] text-[#a09d96] hover:text-[#faf9f5] transition-colors"
                    >
                      {copiedIndex === idx ? (
                        <>
                          <Check className="h-3 w-3 text-[#5db872]" />
                          <span className="text-[#5db872]">Copied</span>
                        </>
                      ) : (
                        <>
                          <Copy className="h-3 w-3" />
                          <span>Copy</span>
                        </>
                      )}
                    </button>
                  )}
                </div>
              )
            })}
            {isLoading && (
              <div className="flex items-center gap-2 p-3 rounded-lg bg-[#252320] border border-[#33312e] text-xs text-[#a09d96] w-max">
                <SpikeMark className="h-3.5 w-3.5 fill-[#cc785c] animate-spin" />
                <span>Generating advice...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Bar */}
          <form
            onSubmit={(e) => {
              e.preventDefault()
              handleSend()
            }}
            className="p-3 border-t border-[#2e2b27] bg-[#1f1e1b] flex items-center gap-2"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about salary, skills, roadmap, interview patterns..."
              disabled={isLoading}
              className="flex-1 h-9 px-3.5 rounded-md border border-[#33312e] bg-[#252320] text-xs text-[#faf9f5] placeholder:text-[#6c6a64] focus:outline-none focus:border-[#cc785c] transition-colors"
            />
            <Button
              type="submit"
              size="sm"
              variant="primary"
              disabled={!input.trim() || isLoading}
              className="h-9 px-3.5 gap-1"
            >
              <Send className="h-3.5 w-3.5" />
            </Button>
          </form>
        </div>
      )}
    </>
  )
}
