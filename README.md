# Career Twin AI

Career Twin AI is an AI-powered career intelligence platform that analyzes resumes, GitHub profiles, and career goals to generate personalized career recommendations, learning roadmaps, skill-gap analysis, and country-specific career insights.

The platform combines resume parsing, portfolio analysis, and large language models to provide users with actionable career guidance based on their current profile.

---

## Features

### Resume Analysis

* Resume parsing from PDF, DOCX, and image formats
* Automatic extraction of education, experience, projects, certifications, skills, and achievements
* OCR support for image-based resumes
* Current designation identification
* Structured resume profile generation

### GitHub Profile Analysis

* Public repository analysis
* Programming language distribution
* Technical skill extraction
* Portfolio strength evaluation
* Repository quality assessment
* Activity and contribution insights

### Career Recommendation Engine

* Resume-aware career recommendations
* Career progression based on current designation
* Skill-gap analysis
* Top 5 personalized career suggestions
* Explainable recommendation reasoning

### Career Intelligence

* Country-specific career insights
* Salary estimates
* Job market demand
* Required technical skills
* Visa difficulty
* Industry growth information

Supported regions include:

* India
* Germany
* United States
* Canada
* Australia

### AI Mentor

The integrated AI mentor assists users with

* Career planning
* Skill development
* Learning recommendations
* Interview preparation
* Career roadmap generation

### Resume Match Score

The platform evaluates:

* Technical Skills
* Soft Skills
* Experience
* Projects
* Education
* Certifications
* ATS Compatibility
* Industry Readiness

### Reports

* Professional PDF reports
* JSON export

---

## Technology Stack

| Component         | Technology                               |
| ----------------- | ---------------------------------------- |
| Frontend          | Streamlit                                |
| Backend           | Python                                   |
| AI                | Google Gemini API                        |
| Database          | SQLite                                   |
| Resume Processing | PyPDF2, python-docx, pytesseract, Pillow |
| Data Analysis     | Pandas, NumPy                            |
| Visualization     | Plotly                                   |
| APIs              | GitHub REST API, Gemini API              |

---

## Project Structure

```text
Career-Twin-AI/
│
├── assets/
├── data/
├── database/
├── models/
├── prompts/
├── services/
├── app.py
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/reacher-virus/Career-Twin-AI.git
```

Move into the project directory

```bash
cd Career-Twin-AI
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

## Project Workflow

1. Upload a resume or complete the manual profile.
2. Optionally connect a GitHub username.
3. Extract professional information from the resume.
4. Analyze GitHub repositories and technical skills.
5. Generate personalized career recommendations.
6. Produce a career roadmap and skill-gap analysis.
7. Export the generated report.

---

## Future Enhancements

* LinkedIn profile integration
* Interview preparation module
* Job recommendation engine
* ATS resume optimization
* Mock interview system
* Company-specific hiring insights
* Multi-language resume support

---

## Screenshots

The following sections can be included after deployment:

* Landing Page
* Resume Analysis
* GitHub Dashboard
* Career Recommendations
* AI Mentor
* Career Roadmap
* Country Intelligence
* PDF Report

---
