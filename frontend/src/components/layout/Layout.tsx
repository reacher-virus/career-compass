import React from 'react'
import { Outlet } from 'react-router-dom'
import { Header } from './Header'
import { Footer } from './Footer'
import { AIMentorChat } from '../dashboard/AIMentorChat'

export const Layout: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col bg-[#faf9f5] text-[#141413] antialiased selection:bg-[#cc785c]/20 selection:text-[#141413] font-sans">
      <Header />
      <main className="flex-1">
        <Outlet />
      </main>
      <Footer />
      <AIMentorChat />
    </div>
  )
}
