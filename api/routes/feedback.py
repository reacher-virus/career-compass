from __future__ import annotations

from typing import Any, Dict
from fastapi import APIRouter
from api.schemas import FeedbackRequest

router = APIRouter(prefix="/api/feedback", tags=["Feedback"])


@router.post("")
def submit_feedback(request: FeedbackRequest) -> Dict[str, Any]:
    # Store or log feedback
    return {
        "status": "success",
        "message": "Thank you for your feedback! It helps improve Career Twin AI.",
        "data": request.model_dump(),
    }
