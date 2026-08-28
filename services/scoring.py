from __future__ import annotations


NORMAL_CAPS = {
    "resume_strength": 88,
    "resume_completeness": 95,
    "ats_readiness": 93,
    "industry_readiness": 88,
    "overall_career_readiness": 88,
    "technical_skills": 92,
    "soft_skills": 88,
    "projects": 90,
    "experience": 90,
    "education": 90,
    "certifications": 90,
    "github": 92,
    "career_match": 92,
    "ai_confidence": 93,
    "success_probability": 90,
    "market_readiness": 90,
    "portfolio_strength": 92,
    "roadmap_progress": 92,
}


EXCEPTIONAL_CAPS = {
    **NORMAL_CAPS,
    "resume_strength": 95,
    "industry_readiness": 94,
    "overall_career_readiness": 95,
    "technical_skills": 96,
    "projects": 96,
    "experience": 96,
    "certifications": 95,
    "github": 96,
    "career_match": 96,
    "success_probability": 94,
    "market_readiness": 94,
    "portfolio_strength": 95,
    "roadmap_progress": 95,
}


def calibrated_score(metric: str, value: float, *, exceptional: bool = False, floor: int = 0) -> int:
    caps = EXCEPTIONAL_CAPS if exceptional else NORMAL_CAPS
    cap = caps.get(metric, 93 if exceptional else 90)
    return max(floor, min(round(value), cap))


def calibrated_ratio_score(
    metric: str,
    numerator: int,
    denominator: int,
    *,
    exceptional: bool = False,
    evidence_floor: int = 35,
) -> int:
    if denominator <= 0 or numerator <= 0:
        return 0
    cap = (EXCEPTIONAL_CAPS if exceptional else NORMAL_CAPS).get(metric, 90)
    raw = numerator / denominator * cap
    return max(evidence_floor, min(round(raw), cap))


def has_senior_evidence(years: int, projects: int, certifications: int, achievements: list[str] | None = None) -> bool:
    achievement_text = " ".join(achievements or []).casefold()
    return (
        years >= 10
        or projects >= 6
        or certifications >= 5
        or any(term in achievement_text for term in ["patent", "publication", "award", "leadership", "managed", "revenue", "research", "industry impact"])
    )

