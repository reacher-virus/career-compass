import React, { useState } from 'react'
import { Download, FileText, Code, Save, Check, AlertCircle } from 'lucide-react'
import { Modal } from '../ui/Modal'
import { Button } from '../ui/Button'
import { exportPdfReport, saveProfileSnapshot } from '../../api/client'
import { useCareer } from '../../context/CareerContext'
import type { AnalysisResult } from '../../types'

export interface ReportsExportModalProps {
  isOpen: boolean
  onClose: () => void
  analysis: AnalysisResult
}

export const ReportsExportModal: React.FC<ReportsExportModalProps> = ({
  isOpen,
  onClose,
  analysis,
}) => {
  const { profile, refreshRecentSnapshots } = useCareer()
  const [isPdfLoading, setIsPdfLoading] = useState(false)
  const [isSaveLoading, setIsSaveLoading] = useState(false)
  const [saveStatus, setSaveStatus] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleDownloadPdf = async () => {
    setIsPdfLoading(true)
    setError(null)
    try {
      const blob = await exportPdfReport({
        generated_at: analysis.generated_at,
        profile: analysis.profile,
        readiness: analysis.readiness,
        success_probability: analysis.success_probability,
        country_intelligence: analysis.country_intelligence,
        career_intelligence: analysis.career_knowledge,
        roadmap: analysis.roadmap,
        resume: analysis.resume_match ? { ats_readiness: analysis.readiness.score } : null,
        github: analysis.github_analysis
          ? {
              username: analysis.github_analysis.username,
              score: analysis.github_analysis.github_score,
              repositories: analysis.github_analysis.repository_count,
            }
          : null,
      })

      const url = window.URL.createObjectURL(new Blob([blob], { type: 'application/pdf' }))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute(
        'download',
        `Career_Twin_Report_${analysis.career_goal.replace(/\s+/g, '_')}.pdf`
      )
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
    } catch (err: any) {
      setError('Failed to generate PDF report. Please try again.')
    } finally {
      setIsPdfLoading(false)
    }
  }

  const handleDownloadJson = () => {
    const dataStr =
      'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(analysis, null, 2))
    const link = document.createElement('a')
    link.href = dataStr
    link.setAttribute(
      'download',
      `Career_Twin_Export_${analysis.career_goal.replace(/\s+/g, '_')}.json`
    )
    document.body.appendChild(link)
    link.click()
    link.remove()
  }

  const handleSaveSnapshot = async () => {
    setIsSaveLoading(true)
    setError(null)
    try {
      await saveProfileSnapshot({
        profile: analysis.profile,
        analysis: analysis.readiness,
        success_probability: analysis.success_probability,
      })
      setSaveStatus('Snapshot saved successfully to local database.')
      refreshRecentSnapshots()
      setTimeout(() => setSaveStatus(null), 4000)
    } catch (err: any) {
      setError('Could not save snapshot to database.')
    } finally {
      setIsSaveLoading(false)
    }
  }

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Export Career Intelligence & Save Snapshot"
      description="Download your comprehensive career intelligence report or persist this profile snapshot."
      maxWidth="md"
    >
      <div className="space-y-4 font-sans">
        {saveStatus && (
          <div className="flex items-center gap-2 p-3.5 rounded-md bg-success/15 border border-success/30 text-xs font-medium text-[#226634] dark:text-[#5db872]">
            <Check className="h-4 w-4 shrink-0 text-success" />
            <span>{saveStatus}</span>
          </div>
        )}

        {error && (
          <div className="flex items-center gap-2 p-3.5 rounded-md bg-error/15 border border-error/30 text-xs font-medium text-error">
            <AlertCircle className="h-4 w-4 shrink-0 text-error" />
            <span>{error}</span>
          </div>
        )}

        <div className="space-y-3">
          {/* PDF */}
          <div className="p-4 rounded-md border border-hairline bg-surface-card flex items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-md bg-canvas text-primary">
                <FileText className="h-5 w-5" />
              </div>
              <div>
                <h4 className="text-sm font-medium text-ink">PDF Executive Report</h4>
                <p className="text-xs text-muted">
                  Vector PDF summary with readiness scorecards, roadmap, and salary bands
                </p>
              </div>
            </div>
            <Button
              type="button"
              onClick={handleDownloadPdf}
              isLoading={isPdfLoading}
              variant="primary"
              size="sm"
              className="shrink-0 gap-1.5"
            >
              <Download className="h-3.5 w-3.5" />
              <span>PDF</span>
            </Button>
          </div>

          {/* JSON */}
          <div className="p-4 rounded-md border border-hairline bg-surface-card flex items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-md bg-canvas text-ink">
                <Code className="h-5 w-5" />
              </div>
              <div>
                <h4 className="text-sm font-medium text-ink">JSON Data Export</h4>
                <p className="text-xs text-muted">Raw structured data object for programmatic use</p>
              </div>
            </div>
            <Button
              type="button"
              onClick={handleDownloadJson}
              variant="secondary"
              size="sm"
              className="shrink-0 gap-1.5"
            >
              <Download className="h-3.5 w-3.5" />
              <span>JSON</span>
            </Button>
          </div>

          {/* Save snapshot */}
          <div className="p-4 rounded-md border border-hairline bg-surface-card flex items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-md bg-canvas text-accent-teal">
                <Save className="h-5 w-5" />
              </div>
              <div>
                <h4 className="text-sm font-medium text-ink">Database Snapshot</h4>
                <p className="text-xs text-muted">Store this profile history to local SQLite database</p>
              </div>
            </div>
            <Button
              type="button"
              onClick={handleSaveSnapshot}
              isLoading={isSaveLoading}
              variant="secondary"
              size="sm"
              className="shrink-0 gap-1.5"
            >
              <Save className="h-3.5 w-3.5" />
              <span>Save</span>
            </Button>
          </div>
        </div>

        <div className="pt-3 flex justify-end">
          <Button type="button" onClick={onClose} variant="ghost" size="sm">
            Close
          </Button>
        </div>
      </div>
    </Modal>
  )
}
