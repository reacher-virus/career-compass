import React from 'react'
import { Link } from 'react-router-dom'
import { SpikeMark, GitHubIcon } from '../ui/Icons'

export const Footer: React.FC = () => {
  return (
    <footer className="w-full bg-[#181715] text-[#a09d96] pt-16 pb-12 border-t border-[#262420] mt-auto font-sans">
      <div className="container space-y-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 lg:gap-12">
          {/* Brand & Wordmark Column */}
          <div className="space-y-4 md:col-span-1">
            <div className="flex items-center gap-2.5">
              <SpikeMark className="h-5 w-5 fill-[#faf9f5]" />
              <span className="font-serif text-2xl text-[#faf9f5] font-normal tracking-[-0.02em]">
                Career Twin
              </span>
            </div>
            <p className="text-xs text-[#a09d96] leading-relaxed max-w-xs">
              A warm, grounded career intelligence platform with recruiter-grade readiness scoring and interactive 5-stage career simulations.
            </p>
            <div className="pt-2">
              <a
                href="https://github.com/REACHER-VIRUS"
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-2 text-xs text-[#faf9f5] hover:text-[#cc785c] transition-colors"
              >
                <GitHubIcon className="h-4 w-4" />
                <span>GitHub Repository</span>
              </a>
            </div>
          </div>

          {/* Column 2: Intelligence Engines */}
          <div className="space-y-3">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-[#faf9f5]">
              Intelligence
            </h4>
            <ul className="space-y-2 text-xs">
              <li>
                <Link to="/setup" className="hover:text-[#faf9f5] transition-colors">
                  Digital Twin Simulator
                </Link>
              </li>
              <li>
                <Link to="/setup" className="hover:text-[#faf9f5] transition-colors">
                  Resume & ATS Parser
                </Link>
              </li>
              <li>
                <Link to="/setup" className="hover:text-[#faf9f5] transition-colors">
                  GitHub Portfolio Audit
                </Link>
              </li>
              <li>
                <Link to="/dashboard" className="hover:text-[#faf9f5] transition-colors">
                  Country Market Intelligence
                </Link>
              </li>
              <li>
                <Link to="/dashboard" className="hover:text-[#faf9f5] transition-colors">
                  Skill Gap & ROI Matrix
                </Link>
              </li>
            </ul>
          </div>

          {/* Column 3: Grounded Knowledge */}
          <div className="space-y-3">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-[#faf9f5]">
              Catalog & Coverage
            </h4>
            <ul className="space-y-2 text-xs">
              <li>
                <span className="text-[#a09d96]">3,527 Grounded Roles</span>
              </li>
              <li>
                <span className="text-[#a09d96]">93 Global Country Markets</span>
              </li>
              <li>
                <span className="text-[#a09d96]">15+ Professional Domains</span>
              </li>
              <li>
                <span className="text-[#a09d96]">Deterministic Readiness Scoring</span>
              </li>
              <li>
                <span className="text-[#a09d96]">PyMuPDF Executive Reports</span>
              </li>
            </ul>
          </div>

          {/* Column 4: Contact & Author */}
          <div className="space-y-3">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-[#faf9f5]">
              Developer
            </h4>
            <div className="space-y-2 text-xs">
              <p className="text-[#faf9f5] font-medium">Yash Agnihotri</p>
              <p className="text-[#a09d96]">Aspiring AI Engineer</p>
              <p>
                <a
                  href="mailto:yashpree237915@gmail.com"
                  className="text-[#cc785c] hover:underline"
                >
                  yashpree237915@gmail.com
                </a>
              </p>
              <div className="pt-2">
                <Link to="/feedback" className="text-xs text-[#faf9f5] underline hover:text-[#cc785c]">
                  Share Feedback or Bug Report →
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t border-[#262420] flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-[#8e8b82]">
          <p>© 2026 Career Twin AI. All rights reserved.</p>
          <div className="flex items-center gap-6">
            <Link to="/" className="hover:text-[#faf9f5]">
              Privacy & Local Storage
            </Link>
            <Link to="/feedback" className="hover:text-[#faf9f5]">
              Feedback
            </Link>
            <a
              href="https://github.com/REACHER-VIRUS"
              target="_blank"
              rel="noreferrer"
              className="hover:text-[#faf9f5]"
            >
              GitHub
            </a>
          </div>
        </div>
      </div>
    </footer>
  )
}
