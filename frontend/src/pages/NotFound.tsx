import React from 'react'
import { Link } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import { Button } from '../components/ui/Button'
import { SpikeMark } from '../components/ui/Icons'

export const NotFound: React.FC = () => {
  return (
    <div className="container max-w-md py-28 px-4 text-center space-y-6 font-sans">
      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-[#efe9de] text-[#141413] mx-auto border border-[#e6dfd8]">
        <SpikeMark className="h-6 w-6 fill-[#cc785c]" />
      </div>
      <h1 className="font-serif text-4xl sm:text-5xl font-normal text-[#141413] tracking-tight">
        404 — Page Not Found
      </h1>
      <p className="text-sm text-[#6c6a64] leading-relaxed">
        The page you requested does not exist or has been relocated.
      </p>
      <Link to="/">
        <Button variant="primary" className="gap-2">
          <ArrowLeft className="h-4 w-4" />
          <span>Return to Overview</span>
        </Button>
      </Link>
    </div>
  )
}
