from __future__ import annotations

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database.db import init_db
from api.routes.careers import router as careers_router
from api.routes.countries import router as countries_router
from api.routes.resume import router as resume_router
from api.routes.github import router as github_router
from api.routes.analysis import router as analysis_router
from api.routes.mentor import router as mentor_router
from api.routes.reports import router as reports_router
from api.routes.profiles import router as profiles_router
from api.routes.feedback import router as feedback_router

load_dotenv()

# Initialize SQLite database schema
init_db()

app = FastAPI(
    title="Career Twin AI API",
    description="REST API backend for Career Twin AI - Career Intelligence, Resume Analysis, GitHub Signals, Roadmap Generation, and AI Mentorship.",
    version="2.0.0",
)

# CORS Configuration
allowed_origins_raw = os.getenv("CORS_ORIGINS", "*")
allowed_origins = [origin.strip() for origin in allowed_origins_raw.split(",") if origin.strip()]
is_wildcard = allowed_origins == ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if is_wildcard else allowed_origins,
    allow_credentials=False if is_wildcard else True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all modular routers
app.include_router(careers_router)
app.include_router(countries_router)
app.include_router(resume_router)
app.include_router(github_router)
app.include_router(analysis_router)
app.include_router(mentor_router)
app.include_router(reports_router)
app.include_router(profiles_router)
app.include_router(feedback_router)


@app.get("/api/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "app": "Career Twin AI API",
        "version": "2.0.0",
    }


@app.get("/", tags=["Health"])
def root_redirect():
    return {
        "message": "Welcome to Career Twin AI API. Documentation available at /docs",
        "status": "online",
    }
