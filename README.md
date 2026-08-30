# Career Twin AI - Next-Generation Career Intelligence Platform

Career Twin AI is a production-grade, AI-driven digital career twin simulator and intelligence platform. It analyzes resumes, GitHub repositories, and user profiles to generate personalized career recommendations, recruiter-grade readiness scorecards, interactive 5-stage career simulations, skill gap matrices, country market intelligence (90+ countries, 3,500+ careers), and a real-time AI career mentor.

---

## Architecture Overview

Career Twin AI has been modernized into a high-performance decoupled architecture:
- **Frontend**: Modern React 19 + TypeScript + Vite + Tailwind CSS + Lucide Icons (Fast, responsive, dark/light mode, mobile-first).
- **Backend API**: FastAPI REST API (`api/main.py`) exposing modular routers for careers, countries, resume parsing, GitHub intelligence, digital twin simulations, AI mentoring, PDF report generation, and SQLite snapshots.
- **Service Layer**: Grounded knowledge bases for 3,500+ careers across 15+ domains, 93 countries, ATS keyword extraction, and PyMuPDF vector PDF reporting.

```text
career-compass-main/
├── api/                        # FastAPI REST API
│   ├── routes/                 # Modular API endpoints
│   │   ├── careers.py          # 3,500+ careers catalog & recommendation
│   │   ├── countries.py        # 90+ countries market intelligence
│   │   ├── resume.py           # Multi-format resume parsing & JD matching
│   │   ├── github.py           # GitHub repo quality analysis
│   │   ├── analysis.py         # Digital Twin & Readiness engine
│   │   ├── mentor.py           # AI Mentor chat & question library
│   │   ├── reports.py          # PDF / JSON report generator
│   │   ├── profiles.py         # SQLite persistence & recent history
│   │   └── feedback.py         # Feedback submission
│   ├── main.py                 # FastAPI application entrypoint & CORS
│   ├── schemas.py              # Pydantic schemas
│   ├── report_utils.py         # PyMuPDF styled PDF report generator
│   └── test_api.py             # Automated API test suite
│
├── frontend/                   # Modern React + Vite + Tailwind frontend
│   ├── src/
│   │   ├── api/client.ts       # Axios client for all API routes
│   │   ├── context/            # React state management
│   │   ├── components/
│   │   │   ├── ui/             # Core accessible UI components
│   │   │   ├── layout/         # Header, Footer, Navigation
│   │   │   └── dashboard/      # ScoreCard, DigitalTwinTimeline, SkillGap, etc.
│   │   ├── pages/              # Home, ProfileSetup, Dashboard, Feedback, NotFound
│   │   └── App.tsx             # Root Router & Providers
│   ├── package.json
│   └── vite.config.ts
│
├── services/                   # Python Intelligence Engines & Grounded Knowledge
├── database/                   # SQLite database storage & queries
├── run_api.py                  # API launcher
└── app.py                      # Legacy Streamlit app
```

---

## Quick Start Guide

### 1. Start the Backend API (FastAPI)

Make sure dependencies are installed, then start the FastAPI server on port 8000:
```bash
python run_api.py
```
*API interactive documentation will be live at `http://127.0.0.1:8000/docs`.*

### 2. Start the Frontend (React + Vite)

In another terminal, navigate into the `frontend` folder and start the dev server:
```bash
cd frontend
npm install
npm run dev
```
*The web application will open at `http://localhost:3000` with automatic `/api` proxying.*

### 3. Run Automated Tests

To test the backend API layer and PDF report builder:
```bash
python api/test_api.py
```

To build and verify the frontend production bundle:
```bash
cd frontend
npm run build
```

---

## Core Features & Engines

1. **Digital Career Twin Simulation**:
   - 5-stage timeline: Current Profile -> 1 Year -> 3 Year -> 5 Year -> 10 Year future.
   - Stage-by-stage compensation milestones, confidence scoring, and required proof competencies.

2. **Recruiter-Grade Readiness Scoring**:
   - 6 Coach Scorecards: Readiness, Success Probability, AI Confidence, Skill Coverage, Portfolio Strength, and Market Readiness.
   - Categorized strength signals and prioritized improvement suggestions.

3. **Country Market Intelligence**:
   - 93 countries supported with local salary compensation bands (Entry, Mid, Senior).
   - Visa difficulty ratings, hiring trend velocity, remote work flexibility, and top employer ecosystems.

4. **Multi-Format Resume & ATS Parser**:
   - PDF, DOCX, TXT, and image OCR resume parsing.
   - Domain recognition, ATS keyword coverage, and automated profile autofill.

5. **Live Job Description Matcher**:
   - Compare your uploaded resume against any pasted job posting to get instant Keyword Match %, Semantic Match %, Technical Match %, and hiring recommendations.

6. **GitHub Portfolio Intelligence**:
   - Scans public repositories, code quality score, star/fork count, language distribution, and open-source impact.

7. **AI Career Mentor**:
   - Profession-aware multi-turn AI chat powered by your profile context, salary targets, and roadmap.

8. **Export & Reporting**:
   - Vector PDF reports generated with PyMuPDF with executive summaries and score bars.
   - JSON export and local SQLite database snapshot storage.

---

## Developer Contact
- **Author**: Yash Agnihotri
- **GitHub**: [github.com/REACHER-VIRUS](https://github.com/REACHER-VIRUS)
- **Email**: `yashpree237915@gmail.com`
