from __future__ import annotations

from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException
from services.ai_mentor import (
    answer_mentor_question,
    get_mentor_question_library,
)
from api.schemas import MentorChatRequest, MentorChatResponse

router = APIRouter(prefix="/api/mentor", tags=["AI Mentor"])


@router.get("/questions")
def get_mentor_questions() -> Dict[str, Any]:
    library = get_mentor_question_library()
    quick_prompts = [
        "Review my resume and suggest top improvements.",
        "What should I learn next to increase my match score?",
        "Which certifications give the highest ROI for this role?",
        "Prepare typical technical and behavioral interview questions.",
        "How can I improve my portfolio / GitHub to stand out?",
        "What is the salary outlook and visa path for my target country?",
    ]
    return {
        "quick_prompts": quick_prompts,
        "library": library,
        "total_questions": len(library),
    }


@router.post("/chat", response_model=MentorChatResponse)
def mentor_chat(request: MentorChatRequest) -> MentorChatResponse:
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    # Ensure standard context defaults
    context = dict(request.context)
    context.setdefault("name", "there")
    context.setdefault("career_goal", "your target career")
    context.setdefault("country", "your target country")
    context.setdefault("weekly_study_hours", 10)
    context.setdefault("detected_domain", "Technology")
    context.setdefault("missing_skills", [])
    context.setdefault("matched_skills", [])
    context.setdefault("roadmap", [])
    context.setdefault("critical_missing", context.get("missing_skills", [])[:3])
    context.setdefault("projects", [])
    context.setdefault("experience", [])
    context.setdefault("certifications", [])

    try:
        answer = answer_mentor_question(
            question=request.question.strip(),
            context=context,
            history=request.history,
        )
        return MentorChatResponse(answer=answer)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"AI Mentor error: {str(exc)}")
