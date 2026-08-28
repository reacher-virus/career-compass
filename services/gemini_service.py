from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv

from models.user import UserProfile
from prompts.career_prompt import CAREER_EXPLANATION_PROMPT
from prompts.future_prompt import FUTURE_SIMULATION_PROMPT
from prompts.roadmap_prompt import ROADMAP_PROMPT


load_dotenv()


def _model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        return genai.GenerativeModel("gemini-1.5-flash")
    except Exception:
        return None


def _profile_context(profile: UserProfile, analysis: dict[str, Any]) -> str:
    return f"""
Name: {profile.name}
Age: {profile.age}
Degree: {profile.degree}
Branch: {profile.branch}
Current year: {profile.current_year}
GPA: {profile.gpa}
Skills: {", ".join(profile.skills)}
Projects: {", ".join(profile.projects)}
Certifications: {", ".join(profile.certifications)}
Internships: {", ".join(profile.internships)}
Weekly study hours: {profile.weekly_study_hours}
Career goal: {profile.career_goal}
Target country: {profile.target_country}
Readiness score: {analysis.get("score")}
Matched skills: {", ".join(analysis.get("matched_skills", []))}
Missing skills: {", ".join(analysis.get("missing_skills", []))}
"""


def generate_text(system_prompt: str, profile: UserProfile, analysis: dict[str, Any]) -> str | None:
    model = _model()
    if model is None:
        return None

    prompt = f"{system_prompt}\n\nUser profile and calculated analysis:\n{_profile_context(profile, analysis)}"
    try:
        response = model.generate_content(prompt)
        return response.text.strip() if response and response.text else None
    except Exception:
        return None


def generate_roadmap(profile: UserProfile, analysis: dict[str, Any]) -> str | None:
    return generate_text(ROADMAP_PROMPT, profile, analysis)


def generate_future_simulation(profile: UserProfile, analysis: dict[str, Any]) -> str | None:
    return generate_text(FUTURE_SIMULATION_PROMPT, profile, analysis)


def generate_explanation(profile: UserProfile, analysis: dict[str, Any]) -> str | None:
    return generate_text(CAREER_EXPLANATION_PROMPT, profile, analysis)
