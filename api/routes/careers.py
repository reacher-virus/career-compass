from __future__ import annotations

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query
from services.career_engine import load_careers
from services.career_knowledge import (
    career_search_suggestions,
    get_career_knowledge,
    recommend_careers_for_profile,
)
from models.user import UserProfile
from api.schemas import UserProfileSchema

router = APIRouter(prefix="/api/careers", tags=["Careers"])


@router.get("")
def get_all_careers() -> Dict[str, Any]:
    careers = load_careers()
    domains: Dict[str, List[str]] = {}
    for name, data in careers.items():
        domain = data.get("domain", "General")
        if domain not in domains:
            domains[domain] = []
        domains[domain].append(name)
    
    popular = [
        "AI Engineer",
        "Data Scientist",
        "Software Engineer",
        "Full-Stack Developer",
        "Product Manager",
        "Cybersecurity Analyst",
        "Cloud Architect",
        "DevOps Engineer",
        "UX/UI Designer",
        "Financial Analyst",
    ]
    popular_available = [c for c in popular if c in careers]
    
    return {
        "total_careers": len(careers),
        "careers": sorted(list(careers.keys())),
        "domains": {k: sorted(v) for k, v in domains.items()},
        "popular": popular_available,
    }


@router.get("/search")
def search_careers(q: str = Query(..., min_length=1)) -> List[str]:
    careers = load_careers()
    return career_search_suggestions(q, careers, limit=80)


@router.get("/details/{career_name}")
def get_career_details(career_name: str) -> Dict[str, Any]:
    careers = load_careers()
    if career_name not in careers:
        # Fallback to general lookup
        details = get_career_knowledge(career_name, {})
        return details
    return get_career_knowledge(career_name, careers[career_name])


@router.post("/recommend")
def recommend_careers(profile_data: UserProfileSchema) -> List[Dict[str, Any]]:
    careers = load_careers()
    profile = UserProfile(
        name=profile_data.name,
        age=profile_data.age,
        degree=profile_data.degree,
        branch=profile_data.branch,
        current_year=profile_data.current_year,
        gpa=profile_data.gpa,
        skills=profile_data.skills,
        projects=profile_data.projects,
        certifications=profile_data.certifications,
        internships=profile_data.internships,
        languages=profile_data.languages,
        achievements=profile_data.achievements,
        weekly_study_hours=profile_data.weekly_study_hours,
        career_goal=profile_data.career_goal,
        target_country=profile_data.target_country,
    )
    recommended = recommend_careers_for_profile(profile, None, careers, limit=6)
    return [
        {
            "career": r.career,
            "domain": r.domain,
            "fit_score": r.fit_score,
            "explanation": r.explanation,
            "matched_signals": r.matched_signals,
        }
        for r in recommended
    ]
