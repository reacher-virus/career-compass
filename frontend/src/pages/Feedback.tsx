import React, { useState } from 'react'
import { Star, Send, Check } from 'lucide-react'
import { Card, CardContent } from '../components/ui/Card'
import { Input } from '../components/ui/Input'
import { Textarea } from '../components/ui/Textarea'
import { Select } from '../components/ui/Select'
import { Button } from '../components/ui/Button'
import { SpikeMark, GitHubIcon } from '../components/ui/Icons'
import { submitFeedback } from '../api/client'

export const Feedback: React.FC = () => {
  const [feedbackType, setFeedbackType] = useState('General Feedback')
  const [rating, setRating] = useState(5)
  const [subject, setSubject] = useState('')
  const [message, setMessage] = useState('')
  const [email, setEmail] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isSuccess, setIsSuccess] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!message.trim()) return

    setIsLoading(true)
    try {
      await submitFeedback({
        feedback_type: feedbackType,
        rating,
        subject,
        message,
        email: email || undefined,
      })
      setIsSuccess(true)
      setSubject('')
      setMessage('')
      setEmail('')
    } catch (err) {
      console.error('Feedback submit error', err)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="container max-w-2xl py-16 px-4 space-y-10 font-sans">
      <div className="text-center space-y-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-full bg-surface-card text-ink mx-auto border border-hairline">
          <SpikeMark className="h-5 w-5 fill-primary" />
        </div>
        <h1 className="font-serif text-4xl sm:text-5xl font-normal text-ink tracking-[-0.02em]">
          Feedback & Inquiries
        </h1>
        <p className="text-sm text-muted max-w-md mx-auto leading-relaxed">
          Share bug reports, feature suggestions, or market corrections directly with the developer.
        </p>
      </div>

      <Card variant="canvas">
        <CardContent className="p-8 space-y-6">
          {isSuccess ? (
            <div className="text-center py-10 space-y-3 animate-in fade-in">
              <div className="p-3 rounded-full bg-success/15 text-[#226634] dark:text-[#5db872] w-fit mx-auto border border-success/30">
                <Check className="h-6 w-6 text-success" />
              </div>
              <h3 className="font-serif text-2xl text-ink">
                Thank You for Your Feedback
              </h3>
              <p className="text-xs text-muted max-w-sm mx-auto leading-relaxed">
                Your feedback has been registered and helps refine the Career Twin AI intelligence algorithms.
              </p>
              <div className="pt-2">
                <Button
                  type="button"
                  variant="secondary"
                  size="sm"
                  onClick={() => setIsSuccess(false)}
                >
                  Submit Another Response
                </Button>
              </div>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              <Select
                label="Feedback Category"
                value={feedbackType}
                onChange={(e) => setFeedbackType(e.target.value)}
                options={[
                  'General Feedback',
                  'Bug Report',
                  'Feature Request',
                  'Career Taxonomy / Salary Correction',
                  'Resume Parsing Optimization',
                  'GitHub Analysis Feedback',
                ]}
              />

              <div className="space-y-1.5">
                <label className="text-xs font-medium text-ink">Experience Rating (1 to 5 Stars)</label>
                <div className="flex items-center gap-1.5">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <button
                      key={star}
                      type="button"
                      onClick={() => setRating(star)}
                      className="p-1 text-accent-amber hover:scale-110 transition-transform"
                    >
                      <Star
                        className={`h-5 w-5 ${
                          star <= rating ? 'fill-current text-accent-amber' : 'text-muted-soft opacity-40'
                        }`}
                      />
                    </button>
                  ))}
                  <span className="text-xs font-mono font-medium text-ink ml-2">
                    {rating} / 5 Stars
                  </span>
                </div>
              </div>

              <Input
                label="Subject"
                placeholder="Brief summary of feedback or issue"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
              />

              <Textarea
                label="Message"
                placeholder="Describe your feedback, thoughts, or suggestions in detail..."
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                rows={4}
                required
              />

              <Input
                label="Your Email (Optional)"
                type="email"
                placeholder="alex@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                helperText="Provide your email if you would like a direct reply."
              />

              <div className="pt-2">
                <Button
                  type="submit"
                  variant="primary"
                  isLoading={isLoading}
                  className="w-full gap-2 font-medium"
                >
                  <Send className="h-4 w-4" />
                  <span>Submit Feedback</span>
                </Button>
              </div>
            </form>
          )}

          <div className="pt-6 border-t border-hairline text-center space-y-2 text-xs text-muted">
            <div>
              Developer Contact:{' '}
              <a
                href="mailto:yashpree237915@gmail.com"
                className="text-primary hover:underline font-medium"
              >
                yashpree237915@gmail.com
              </a>
            </div>
            <div className="flex items-center justify-center gap-2">
              <span>Developed by Yash Agnihotri</span>
              <span>•</span>
              <a
                href="https://github.com/REACHER-VIRUS"
                target="_blank"
                rel="noreferrer"
                className="text-ink hover:text-primary inline-flex items-center gap-1 font-medium"
              >
                <GitHubIcon className="h-3 w-3" />
                <span>GitHub Profile</span>
              </a>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
