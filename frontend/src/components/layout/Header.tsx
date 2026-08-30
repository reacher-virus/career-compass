import React, { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Menu, X } from 'lucide-react'
import { SpikeMark } from '../ui/Icons'
import { Button } from '../ui/Button'
import { Badge } from '../ui/Badge'
import { useCareer } from '../../context/CareerContext'

export const Header: React.FC = () => {
  const { analysisResult } = useCareer()
  const location = useLocation()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const navLinks = [
    { label: 'Overview', path: '/' },
    { label: 'Profile Setup', path: '/setup' },
    {
      label: 'Digital Twin',
      path: '/dashboard',
      badge: analysisResult ? 'Active' : undefined,
    },
    { label: 'Feedback', path: '/feedback' },
  ]

  return (
    <header className="sticky top-0 z-40 w-full border-b border-[#e6dfd8] bg-[#faf9f5]/95 backdrop-blur-xs transition-all">
      <div className="container flex h-16 items-center justify-between">
        {/* Brand Wordmark with Anthropic Spike-Mark */}
        <Link
          to="/"
          className="flex items-center gap-2.5 group select-none"
          onClick={() => setMobileMenuOpen(false)}
        >
          <div className="flex h-7 w-7 items-center justify-center text-[#141413]">
            <SpikeMark className="h-5 w-5 fill-[#141413] transition-transform duration-200 group-hover:scale-110 group-hover:rotate-45" />
          </div>
          <div className="flex items-baseline gap-1">
            <span className="font-serif text-2xl font-normal tracking-[-0.03em] text-[#141413]">
              Career Twin
            </span>
            <span className="h-1.5 w-1.5 rounded-full bg-[#cc785c]" />
          </div>
        </Link>

        {/* Desktop Navigation Links */}
        <nav className="hidden md:flex items-center gap-6">
          {navLinks.map((item) => {
            const isActive = location.pathname === item.path
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`text-sm font-medium transition-colors flex items-center gap-1.5 py-1 ${
                  isActive
                    ? 'text-[#141413] font-semibold border-b-2 border-[#141413]'
                    : 'text-[#6c6a64] hover:text-[#141413]'
                }`}
              >
                <span>{item.label}</span>
                {item.badge && (
                  <span className="rounded-full bg-[#5db872]/20 text-[#226634] text-[10px] px-2 py-0.2 font-medium">
                    {item.badge}
                  </span>
                )}
              </Link>
            )
          })}
        </nav>

        {/* Right CTA cluster */}
        <div className="flex items-center gap-3">
          {location.pathname !== '/setup' ? (
            <Link to="/setup" className="hidden sm:inline-flex">
              <Button size="default" variant="primary" className="gap-2">
                <SpikeMark className="h-3.5 w-3.5 fill-white" />
                <span>Build Twin</span>
              </Button>
            </Link>
          ) : (
            <Link to="/dashboard" className="hidden sm:inline-flex">
              <Button size="default" variant="secondary">
                <span>View Dashboard</span>
              </Button>
            </Link>
          )}

          {/* Mobile hamburger toggle */}
          <button
            type="button"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 rounded-md text-[#141413] hover:bg-[#efe9de] transition-colors"
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-[#e6dfd8] bg-[#faf9f5] px-4 py-5 space-y-3 animate-in slide-in-from-top-2">
          {navLinks.map((item) => {
            const isActive = location.pathname === item.path
            return (
              <Link
                key={item.path}
                to={item.path}
                onClick={() => setMobileMenuOpen(false)}
                className={`flex items-center justify-between px-3 py-2.5 rounded-md text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-[#efe9de] text-[#141413] font-semibold'
                    : 'text-[#6c6a64] hover:bg-[#efe9de] hover:text-[#141413]'
                }`}
              >
                <span>{item.label}</span>
                {item.badge && (
                  <Badge variant="teal" className="text-[10px]">
                    {item.badge}
                  </Badge>
                )}
              </Link>
            )
          })}
          <div className="pt-3 border-t border-[#e6dfd8] flex flex-col gap-2">
            <Link
              to="/setup"
              onClick={() => setMobileMenuOpen(false)}
              className="w-full block"
            >
              <Button size="lg" variant="primary" className="w-full justify-center gap-2">
                <SpikeMark className="h-4 w-4 fill-white" />
                <span>Get Started with Career Twin</span>
              </Button>
            </Link>
          </div>
        </div>
      )}
    </header>
  )
}
