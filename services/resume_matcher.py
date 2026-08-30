from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from models.user import UserProfile
from services.github_analyzer import GitHubAnalysis
from services.resume_parser import ResumeParseResult, build_skill_bank, detect_skills
from services.scoring import calibrated_ratio_score, calibrated_score


STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "be",
    "for",
    "in",
    "of",
    "on",
    "or",
    "our",
    "the",
    "to",
    "with",
    "you",
    "your",
}


@dataclass
class ResumeMatchAnalysis:
    overall_match: int
    weighted_scores: dict[str, int | str]
    strengths: list[str]
    weaknesses: list[str]
    critical_missing_skills: list[str]
    important_skills: list[str]
    nice_to_have_skills: list[str]
    improvement_suggestions: list[dict[str, str]]


@dataclass
class JobDescriptionMatch:
    keyword_match: int
    semantic_match: int
    matched_keywords: list[str]
    missing_keywords: list[str]
    experience_match: int
    education_match: int
    certification_match: int
    technical_match: int
    hiring_recommendation: str
    highlighted_missing_keywords: list[str] = field(default_factory=list)


def analyze_resume_match(
    resume: ResumeParseResult,
    profile: UserProfile,
    career_definition: dict[str, Any],
    github_analysis: GitHubAnalysis | None = None,
) -> ResumeMatchAnalysis:
    required_skills = career_definition.get("required_skills", [])
    resume_skill_values = resume.skills or profile.skills
    matched_required = {skill for skill in required_skills if semantic_contains(skill, resume_skill_values)}
    missing_required = [skill for skill in required_skills if skill not in matched_required]
    required_skill_set = set(canonical_term(skill) for skill in required_skills)

    technical = calibrated_ratio_score("technical_skills", len(matched_required), len(required_skill_set))
    soft = soft_skill_score(resume)
    projects = calibrated_ratio_score("projects", len(resume.structured_projects or resume.projects), 4)
    experience_count = len(resume.structured_experience or resume.experience)
    experience = calibrated_ratio_score("experience", experience_count, 4)
    has_professional_experience = experience_count > 0 and not all("intern" in item.casefold() for item in resume.experience)
    internships: int | str = "N/A" if has_professional_experience else (88 if any("intern" in item.casefold() for item in resume.experience) else 0)
    education = calibrated_score("education", 86 if resume.degree or resume.education else 0)
    certifications = calibrated_ratio_score("certifications", len(resume.structured_certifications or resume.certifications), 3)
    github_relevant = is_github_relevant(career_definition)
    github: int | str = calibrated_score("github", github_analysis.github_score) if github_analysis and github_relevant else ("N/A" if not github_relevant else 0)
    ats = resume.ats_readiness_score
    industry = resume.industry_readiness_score

    weighted_scores = {
        "Technical Skills": round(technical),
        "Soft Skills": round(soft),
        "Projects": round(projects),
        "Experience": round(experience),
        "Internships": internships if isinstance(internships, str) else round(internships),
        "Education": round(education),
        "Certifications": round(certifications),
        "GitHub": github if isinstance(github, str) else round(github),
        "ATS Compatibility": round(ats),
        "Industry Readiness": round(industry),
    }
    weights = {
        "Technical Skills": 0.22,
        "Soft Skills": 0.06,
        "Projects": 0.14,
        "Experience": 0.12,
        "Internships": 0.06,
        "Education": 0.08,
        "Certifications": 0.07,
        "GitHub": 0.05,
        "ATS Compatibility": 0.10,
        "Industry Readiness": 0.10,
    }
    applicable = {key: value for key, value in weighted_scores.items() if isinstance(value, int)}
    applicable_weight_total = sum(weights[key] for key in applicable)
    overall = round(sum(applicable[key] * weights[key] for key in applicable) / applicable_weight_total) if applicable_weight_total else 0

    critical, important, nice = split_missing_skills(missing_required)
    strengths = build_strengths(weighted_scores, matched_required, required_skills)
    weaknesses = build_weaknesses(weighted_scores, missing_required)
    suggestions = build_suggestions(weighted_scores, critical, important, nice, profile.career_goal)

    return ResumeMatchAnalysis(
        overall_match=calibrated_score("career_match", overall),
        weighted_scores=weighted_scores,
        strengths=strengths,
        weaknesses=weaknesses,
        critical_missing_skills=critical,
        important_skills=important,
        nice_to_have_skills=nice,
        improvement_suggestions=suggestions,
    )


def compare_resume_to_job_description(
    resume: ResumeParseResult,
    job_description_text: str,
    careers: dict[str, dict[str, Any]],
) -> JobDescriptionMatch:
    normalized_jd = normalize_text(job_description_text)
    if not normalized_jd:
        return JobDescriptionMatch(0, 0, [], [], 0, 0, 0, 0, "Needs Improvement", [])

    skill_bank = build_skill_bank(careers)
    jd_skills = detect_skills(normalized_jd, skill_bank)
    matched_keywords = [skill for skill in jd_skills if semantic_contains(skill, resume.skills)]
    missing_keywords = [skill for skill in jd_skills if not semantic_contains(skill, resume.skills)]

    keyword_match = percent(len(matched_keywords), len(jd_skills))
    semantic_match = semantic_overlap(resume.text, normalized_jd)
    experience_match = section_match(resume.experience, normalized_jd, ["experience", "intern", "years", "worked", "responsible"])
    education_match = section_match(resume.education + [resume.degree, resume.branch], normalized_jd, ["degree", "bachelor", "master", "education", "graduate"])
    certification_match = section_match(resume.certifications, normalized_jd, ["certification", "certificate", "certified"])
    technical_match = keyword_match
    recommendation = hiring_recommendation(keyword_match, semantic_match, experience_match, education_match, technical_match)

    return JobDescriptionMatch(
        keyword_match=keyword_match,
        semantic_match=semantic_match,
        matched_keywords=matched_keywords,
        missing_keywords=missing_keywords,
        experience_match=experience_match,
        education_match=education_match,
        certification_match=certification_match,
        technical_match=technical_match,
        hiring_recommendation=recommendation,
        highlighted_missing_keywords=missing_keywords[:12],
    )


def normalize(value: str) -> str:
    return canonical_term(value)


SEMANTIC_EQUIVALENTS = {
    "construction supervision": {"site supervision", "site execution", "construction management"},
    "financial reporting": {"financial statements", "financial statement analysis", "reporting"},
    "autocad": {"autocad civil", "auto cad"},
    "python": {"python programming", "python development"},
    "communication": {"communication skills", "verbal communication"},
    "rest apis": {"rest api", "api development", "api design"},
    "machine learning": {"ml", "predictive modeling"},
    "recruitment": {"talent acquisition", "sourcing"},
    "patient care": {"patient handling", "clinical care"},
    "legal research": {"case law research"},
}


def canonical_term(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9+#. ]", " ", value.casefold())
    normalized = re.sub(r"\s+", " ", normalized).strip()
    for canonical, variants in SEMANTIC_EQUIVALENTS.items():
        if normalized == canonical or normalized in variants:
            return canonical
    return normalized


def semantic_contains(required: str, available_values: list[str]) -> bool:
    required_key = canonical_term(required)
    variants = {required_key, *SEMANTIC_EQUIVALENTS.get(required_key, set())}
    available = {canonical_term(value) for value in available_values}
    if variants & available:
        return True
    joined = " ".join(available_values).casefold()
    return any(re.search(r"(?<![a-z0-9])" + re.escape(variant) + r"(?![a-z0-9])", joined) for variant in variants)


def is_github_relevant(career_definition: dict[str, Any]) -> bool:
    domain = str(career_definition.get("domain", "")).casefold()
    career_text = " ".join(
        [
            str(career_definition.get("name", "")),
            str(career_definition.get("description", "")),
            " ".join(career_definition.get("required_skills", [])),
            " ".join(career_definition.get("technical_skills", [])),
        ]
    ).casefold()
    if domain in {"technology"}:
        return True
    return any(term in career_text for term in ["software", "developer", "data", "ai", "machine learning", "cyber", "cloud", "devops", "programming"])


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def percent(numerator: int, denominator: int) -> int:
    if denominator <= 0:
        return 0
    return round(numerator / denominator * 100)


def soft_skill_score(resume: ResumeParseResult) -> int:
    soft_skills = resume.skill_categories.get("Soft Skills", [])
    return calibrated_ratio_score("soft_skills", len(soft_skills), 4)


def split_missing_skills(missing_skills: list[str]) -> tuple[list[str], list[str], list[str]]:
    return missing_skills[:3], missing_skills[3:7], missing_skills[7:]


def build_strengths(weighted_scores: dict[str, int | str], matched_required: set[str], required_skills: list[str]) -> list[str]:
    strengths = []
    if matched_required:
        strengths.append(f"Matches {len(matched_required)} target-career technical skill(s), which directly improves role fit.")
    for label, score in weighted_scores.items():
        if isinstance(score, int) and score >= 75:
            strengths.append(f"{label} is strong because the resume provides enough evidence in this area.")
    return strengths[:6] or ["The resume has enough structure to begin matching against the selected career."]


def build_weaknesses(weighted_scores: dict[str, int | str], missing_skills: list[str]) -> list[str]:
    weaknesses = []
    if missing_skills:
        weaknesses.append(f"{len(missing_skills)} required skill(s) are missing from the resume, reducing technical match.")
    for label, score in weighted_scores.items():
        if isinstance(score, int) and score < 45:
            weaknesses.append(f"{label} is weak because the resume has limited visible proof for this category.")
    return weaknesses[:6]


def build_suggestions(
    weighted_scores: dict[str, int | str],
    critical: list[str],
    important: list[str],
    nice: list[str],
    career_goal: str,
) -> list[dict[str, str]]:
    suggestions = []
    for skill in critical:
        suggestions.append(
            {
                "suggestion": f"Add a project or bullet proving {skill}.",
                "why": f"{skill} is a critical missing skill for {career_goal}, so adding proof will raise the technical match score.",
            }
        )
    if isinstance(weighted_scores["Projects"], int) and weighted_scores["Projects"] < 70:
        suggestions.append(
            {
                "suggestion": "Add one role-specific portfolio project with tools, problem, and measurable result.",
                "why": "Project evidence is weighted heavily because recruiters need proof that skills were applied.",
            }
        )
    if isinstance(weighted_scores["ATS Compatibility"], int) and weighted_scores["ATS Compatibility"] < 70:
        suggestions.append(
            {
                "suggestion": "Use standard resume headings and include exact role keywords.",
                "why": "ATS compatibility is low when key sections or target keywords are hard to find.",
            }
        )
    if important:
        suggestions.append(
            {
                "suggestion": f"Add important supporting skills: {', '.join(important[:4])}.",
                "why": "These skills are not always blockers, but they improve shortlist probability.",
            }
        )
    if nice:
        suggestions.append(
            {
                "suggestion": f"Use nice-to-have skills as differentiators: {', '.join(nice[:4])}.",
                "why": "Nice-to-have skills help the resume stand out after core requirements are covered.",
            }
        )
    return suggestions[:8]


def semantic_overlap(resume_text: str, jd_text: str) -> int:
    resume_terms = meaningful_terms(resume_text)
    jd_terms = meaningful_terms(jd_text)
    if not jd_terms:
        return 0
    return calibrated_score("career_match", percent(len(resume_terms & jd_terms), len(jd_terms)))


def meaningful_terms(text: str) -> set[str]:
    terms = re.findall(r"[a-zA-Z][a-zA-Z+#.]{2,}", text.casefold())
    return {term for term in terms if term not in STOP_WORDS}


def section_match(resume_values: list[str], jd_text: str, jd_markers: list[str]) -> int:
    jd_lower = jd_text.casefold()
    if not any(marker in jd_lower for marker in jd_markers):
        return 82
    resume_text = " ".join(value for value in resume_values if value).casefold()
    if not resume_text:
        return 0
    return semantic_overlap(resume_text, jd_text)


def hiring_recommendation(*scores: int) -> str:
    average = round(sum(scores) / len(scores)) if scores else 0
    if average >= 80:
        return "Excellent"
    if average >= 65:
        return "Good"
    if average >= 45:
        return "Average"
    return "Needs Improvement"
