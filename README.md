# Career Twin AI — Intelligent Career Simulation Platform

Career Twin AI is an AI-powered career intelligence platform that analyzes resumes, GitHub profiles, and career goals to generate personalized career recommendations, digital twin projections (1, 3, 5, 10 years), learning roadmaps, skill-gap analysis, and country-specific career insights across 3,500+ careers and 93 global markets.

---

## ✨ Features & Capabilities

### 1. Digital Career Twin Simulation
* 5-stage milestone trajectory projection (Current, 1-Year, 3-Year, 5-Year, and 10-Year horizons).
* Compensation milestone curves ($/yr or local currency).
* Core deliverable proof requirements and transition probabilities.

### 2. Multi-Format Resume & ATS Parser
* Deterministic parsing for PDF, DOCX, and TXT resumes.
* Automatic extraction of skills, experience, projects, certifications, and achievements.
* ATS readiness score and completeness evaluations with instant autofill.

### 3. GitHub Portfolio Intelligence
* Repository code quality assessment and language distribution.
* Star/fork count analysis and open-source contribution level verification.
* Actionable portfolio recommendations for engineering candidates.

### 4. 93 Global Market Intelligence
* Localized salary compensation bands (entry, mid, senior).
* Visa complexity evaluation (Low, Medium, High).
* Active hiring companies, major industries, and regional interview cultures.

### 5. Deterministic Skill Gap & ROI Matrix
* Direct comparison of verified competencies vs 3,527 role benchmarks.
* Priority identification of missing requirements and highest-ROI next skills.

### 6. Interactive AI Career Mentor
* Multi-turn conversational mentor grounded in the user's specific resume and targets.
* Quick prompts for interview tips, compensation negotiations, and study planning.

### 7. Executive Reports & Exports
* Professional vector PDF report download.
* Complete structured JSON data export.
* Local profile history persistence.

---

## 🛠️ Architecture & Tech Stack

| Component | Technology |
|---|---|
| **Frontend** | React 19, TypeScript, Vite, Tailwind CSS, Lucide Icons |
| **Design System** | Claude.com Warm Editorial Design System (Cream `#faf9f5`, Coral `#cc785c`, Serif Display) |
| **Backend API** | FastAPI, Python 3.10+, Uvicorn, Pydantic |
| **Document Processing** | PyMuPDF (fitz), python-docx, Pillow, ReportLab |
| **Data & Storage** | SQLite, Pandas, NumPy |
| **AI Integration** | Google Gemini API (with deterministic fallback engine) |

---

## 📂 Project Structure

```
career-compass/
├── api/                        # FastAPI REST API endpoints
│   ├── main.py                 # Core FastAPI application & routes
│   └── test_api.py             # Complete test suite for all endpoints
│
├── frontend/                   # React + Vite Modern Frontend
│   ├── src/
│   │   ├── api/                # Axios API client & typed endpoints
│   │   ├── components/
│   │   │   ├── ui/             # Reusable UI components (Button, Card, Badge, Modal, Tabs)
│   │   │   ├── layout/         # Header, Footer, Main Layout
│   │   │   └── dashboard/      # ScoreCard, DigitalTwinTimeline, SkillGap, etc.
│   │   ├── context/            # CareerContext state manager
│   │   ├── pages/              # Home, ProfileSetup, Dashboard, Feedback, NotFound
│   │   └── index.css           # Claude.com design system CSS & typography
│   ├── package.json
│   └── vite.config.ts
│
├── services/                   # Career Intelligence & Knowledge Base
├── database/                   # SQLite database storage & queries
├── run_api.py                  # API launcher
└── app.py                      # Streamlit application
```

---

## 🚀 Quick Start Guide

### 1. Start the Backend API (FastAPI)

Make sure dependencies are installed, then start the FastAPI server:
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

## 👨‍💻 Author & Attribution
* **Developer**: Yash Agnihotri
* **Frontend Redesign & Architecture**: Career Twin AI Team
