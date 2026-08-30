from __future__ import annotations

from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException
from database.db import recent_profiles, save_profile
from models.user import UserProfile
from api.schemas import SaveProfileRequest

router = APIRouter(prefix="/api/profiles", tags=["Profiles"])


@router.get("/recent")
def get_recent_profiles(limit: int = 6) -> List[Dict[str, Any]]:
    try:
        return recent_profiles(limit=limit)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database error: {str(exc)}")


@router.post("/save")
def save_profile_snapshot(request: SaveProfileRequest) -> Dict[str, Any]:
    p = request.profile
    profile = UserProfile(
        name=p.name,
        age=p.age,
        degree=p.degree,
        branch=p.branch,
        current_year=p.current_year,
        gpa=p.gpa,
        skills=p.skills,
        projects=p.projects,
        certifications=p.certifications,
        internships=p.internships,
        languages=p.languages,
        achievements=p.achievements,
        weekly_study_hours=p.weekly_study_hours,
        career_goal=p.career_goal,
        target_country=p.target_country,
    )
    try:
        save_profile(profile, request.analysis, request.success_probability)
        return {"status": "success", "message": "Profile snapshot saved successfully."}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to save profile: {str(exc)}")
