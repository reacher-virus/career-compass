import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { CareerProvider } from './context/CareerContext'
import { Layout } from './components/layout/Layout'
import { Home } from './pages/Home'
import { ProfileSetup } from './pages/ProfileSetup'
import { Dashboard } from './pages/Dashboard'
import { Feedback } from './pages/Feedback'
import { NotFound } from './pages/NotFound'

export const App: React.FC = () => {
  return (
    <CareerProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Home />} />
            <Route path="setup" element={<ProfileSetup />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="feedback" element={<Feedback />} />
            <Route path="*" element={<NotFound />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </CareerProvider>
  )
}

export default App
