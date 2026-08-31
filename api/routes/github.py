from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict
import re
from fastapi import APIRouter, HTTPException, Path as FPath
from services.github_analyzer import analyze_github_profile, GitHubAnalysis
from api.schemas import GitHubAnalysisRequest

router = APIRouter(prefix="/api/github", tags=["GitHub"])


def clean_github_username(value: str) -> str:
    cleaned = (value or "").strip().rstrip("/")
    if not cleaned:
        return ""
    cleaned = re.sub(r"^https?://", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"^www\.", "", cleaned, flags=re.IGNORECASE)
    if cleaned.casefold().startswith("github.com/"):
        cleaned = cleaned.split("/", 1)[1]
    return re.split(r"[/#?]", cleaned, maxsplit=1)[0].strip()


def github_analysis_to_dict(analysis: GitHubAnalysis) -> Dict[str, Any]:
    return asdict(analysis)


@router.get("/{username}")
def get_github_analysis(username: str = FPath(..., description="GitHub username or profile URL")) -> Dict[str, Any]:
    cleaned = clean_github_username(username)
    if not cleaned:
        raise HTTPException(status_code=400, detail="Invalid GitHub username.")
    try:
        analysis = analyze_github_profile(cleaned)
        return github_analysis_to_dict(analysis)
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to analyze GitHub profile: {str(exc)}")


@router.post("/analyze")
def post_github_analysis(request: GitHubAnalysisRequest) -> Dict[str, Any]:
    cleaned = clean_github_username(request.username)
    if not cleaned:
        raise HTTPException(status_code=400, detail="Invalid GitHub username.")
    try:
        analysis = analyze_github_profile(cleaned)
        return github_analysis_to_dict(analysis)
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to analyze GitHub profile: {str(exc)}")
