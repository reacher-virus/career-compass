from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from models.user import UserProfile


CAREERS_PATH = Path(__file__).resolve().parent.parent / "data" / "careers.json"


def load_careers() -> dict[str, dict[str, Any]]:
    with CAREERS_PATH.open("r", encoding="utf-8") as file:
        careers = json.load(file)

    from services.career_knowledge import get_career_catalog, get_career_knowledge

    catalog = get_career_catalog()
    for name, career in catalog.items():
        careers[name] = {**career, **careers.get(name, {})}
    for name, career in list(careers.items()):
        if not career.get("domain"):
            careers[name] = get_career_knowledge(name, career)
    return careers


def normalize_skill(skill: str) -> str:
    return skill.strip().casefold()


SKILL_ALIASES = {
    "js": "javascript",
    "ts": "typescript",
    "py": "python",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "powerbi": "power bi",
    "ms excel": "excel",
    "advanced excel": "excel",
    "postgres": "postgresql",
    "node": "node.js",
}


def canonical_skill(skill: str) -> str:
    normalized = normalize_skill(skill)
    normalized = normalized.replace("+ +", "++").replace(" ", " ")
    return SKILL_ALIASES.get(normalized, normalized)


def score_label(score: int) -> str:
    if score >= 90:
        return "Exceptional"
    if score >= 80:
        return "Advanced"
    if score >= 68:
        return "Industry Ready"
    if score >= 52:
        return "Developing"
    if score >= 38:
        return "Foundation"
    return "Beginner"


def split_multiline_or_csv(value: str) -> list[str]:
    if not value:
        return []
    normalized = value.replace("\n", ",")
    return [item.strip() for item in normalized.split(",") if item.strip()]


def calculate_readiness(profile: UserProfile, career: dict[str, Any]) -> dict[str, Any]:
    required = career.get("required_skills", [])
    user_skills = {canonical_skill(skill) for skill in profile.skills}
    matched = [skill for skill in required if canonical_skill(skill) in user_skills]
    missing = [skill for skill in required if canonical_skill(skill) not in user_skills]

    skill_coverage = len(matched) / len(required) if required else min(len(user_skills) / 8, 1)
    skill_score = skill_coverage * 36
    education_score = 9 if profile.degree else 3
    project_score = min(profile.project_count, 4) / 4 * 12
    experience_score = min(profile.internship_count, 3) / 3 * 11
    certification_score = min(profile.certification_count, 3) / 3 * 7
    achievement_score = min(len([item for item in profile.achievements if item.strip()]), 3) / 3 * 4
    language_score = min(len([item for item in profile.languages if item.strip()]), 2) / 2 * 2
    study_score = min(profile.weekly_study_hours, 18) / 18 * 5

    score = round(
        skill_score
        + education_score
        + project_score
        + experience_score
        + certification_score
        + achievement_score
        + language_score
        + study_score
    )
    if profile.skills or profile.degree or profile.projects or profile.internships:
        score = max(score, 34)
    if profile.skills and (profile.projects or profile.internships):
        score = max(score, 42)
    years = infer_profile_years(profile)
    genuine_fresher = bool(profile.degree and profile.skills and (profile.projects or profile.certifications))
    early_professional = 2 <= years <= 5 or (profile.internship_count >= 1 and profile.project_count >= 1 and len(profile.skills) >= 4)
    senior_evidence = years >= 10 or (
        profile.project_count >= 6
        and profile.certification_count >= 3
        and any(term in " ".join(profile.achievements).casefold() for term in ["led", "managed", "research", "publication", "patent", "impact"])
    )
    if genuine_fresher:
        score = max(score, 66)
    if early_professional:
        score = max(score, 80 if skill_coverage >= 0.45 else 74)
    if senior_evidence:
        score = max(score, 89)

    positives = []
    improvements = []
    if matched:
        positives.append(f"{len(matched)} target skill(s) already match the role")
    if profile.degree:
        positives.append("education information is present")
    if profile.project_count:
        positives.append(f"{profile.project_count} project signal(s) support the profile")
    else:
        improvements.append("add one practical project or case study for this role")
    if profile.internship_count:
        positives.append("experience, internship, or professional exposure is included")
    else:
        improvements.append("add internship, job, freelance, lab, or volunteer experience")
    if profile.certification_count:
        positives.append("certifications provide proof of learning")
    if profile.weekly_study_hours >= 8:
        positives.append("weekly study consistency is strong")
    elif profile.weekly_study_hours:
        improvements.append("increase weekly practice consistency")
    if missing:
        improvements.append("close priority skill gaps: " + ", ".join(missing[:4]))

    cap = 93 if senior_evidence else 88
    if skill_coverage < 0.5:
        cap = min(cap, 82 if early_professional else 78)
    final_score = max(28, min(score, cap))
    return {
        "score": final_score,
        "label": score_label(final_score),
        "matched_skills": matched,
        "missing_skills": missing,
        "required_skills": required,
        "skill_coverage": round(skill_coverage * 100),
        "recommended_next_skills": missing[:5],
        "positive_factors": positives or ["profile foundation is ready for improvement"],
        "improvement_factors": improvements or ["keep adding measurable proof of work"],
        "why": "Career readiness measures current profile quality: education, skills, projects, experience, certifications, achievements, languages, and study consistency.",
    }


def calculate_success_probability(profile: UserProfile, readiness_score: int, missing_count: int) -> int:
    probability = 30

    if profile.career_goal:
        probability += 5
    if profile.degree:
        probability += 4
    probability += min(len(profile.skills), 10) * 1.0
    probability += min(profile.project_count, 4) * 3
    probability += min(profile.internship_count, 3) * 4
    probability += min(profile.certification_count, 3) * 2
    probability += min(len([item for item in profile.achievements if item.strip()]), 3) * 1.5
    probability += min(readiness_score, 93) * 0.18

    if profile.weekly_study_hours >= 14:
        probability += 8
    elif profile.weekly_study_hours >= 8:
        probability += 5
    elif profile.weekly_study_hours >= 3:
        probability += 3

    if profile.gpa >= 8:
        probability += 2
    elif 6 <= profile.gpa < 8:
        probability += 1

    probability -= min(missing_count, 7) * 1.8
    if profile.skills or profile.projects or profile.internships:
        probability = max(probability, 40)

    cap = 90 if readiness_score >= 88 and profile.project_count >= 3 and profile.internship_count >= 2 else 86
    return max(32, min(round(probability), cap))


def infer_profile_years(profile: UserProfile) -> int:
    import re

    text = " ".join(profile.internships + profile.achievements + profile.projects)
    explicit = re.findall(r"\b(\d{1,2})\+?\s*(?:years|yrs)\b", text, flags=re.IGNORECASE)
    if explicit:
        return max(int(value) for value in explicit)
    years = [int(year) for year in re.findall(r"\b(20\d{2}|19\d{2})\b", text)]
    if len(years) >= 2:
        return max(0, min(40, max(years) - min(years)))
    return min(5, profile.internship_count)


def career_matches(profile: UserProfile, careers: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    matches = []
    for name, career in careers.items():
        readiness = calculate_readiness(profile, career)
        probability = calculate_success_probability(
            profile,
            readiness["score"],
            len(readiness["missing_skills"]),
        )
        matches.append(
            {
                "career": name,
                "score": readiness["score"],
                "probability": probability,
                "missing_skills": readiness["missing_skills"],
                "matched_skills": readiness["matched_skills"],
                "label": readiness["label"],
                "reasoning": readiness.get("positive_factors", [])[:3],
            }
        )
    return sorted(matches, key=lambda item: (item["probability"], item["score"]), reverse=True)


def fallback_roadmap(
    missing_skills: list[str],
    career_goal: str,
    country: str = "",
    weekly_study_hours: int = 0,
) -> list[dict[str, Any]]:
    focus = adaptive_learning_sequence(career_goal, missing_skills, country)
    difficulty = "light" if weekly_study_hours < 6 else "balanced" if weekly_study_hours < 14 else "intensive"

    return [
        {
            "month": f"Month {index + 1}",
            "focus": skill,
            "tasks": [
                monthly_learning_task(skill, difficulty),
                monthly_project_task(skill, career_goal, country),
            ],
            "weeks": [
                {"week": "Week 1", "milestone": f"Understand the fundamentals of {skill} and collect role-specific examples."},
                {"week": "Week 2", "milestone": f"Practice {skill} through two focused exercises or case tasks."},
                {"week": "Week 3", "milestone": f"Apply {skill} in a small {career_goal or 'career'} portfolio artifact."},
                {"week": "Week 4", "milestone": f"Document outcomes, update resume bullets, and prepare interview talking points for {skill}."},
            ],
            "outcome": f"Create a portfolio artifact proving {skill} for {career_goal}.",
        }
        for index, skill in enumerate(focus[:6])
    ]


def fallback_future(profile: UserProfile, readiness_score: int) -> list[dict[str, str]]:
    if readiness_score >= 75:
        one_year = "Strong internship or junior role candidate"
        three_year = profile.career_goal or "Specialist contributor"
        five_year = f"Senior {profile.career_goal}" if profile.career_goal else "Senior specialist"
    elif readiness_score >= 45:
        one_year = "Portfolio-ready learner with early applications"
        three_year = f"Junior {profile.career_goal}" if profile.career_goal else "Junior professional"
        five_year = profile.career_goal or "Mid-level professional"
    else:
        one_year = "Foundation-building learner"
        three_year = "Entry-level candidate with targeted projects"
        five_year = f"Growing {profile.career_goal}" if profile.career_goal else "Growing professional"

    return [
        {"label": "Current", "title": profile.current_year or "Starting point", "detail": "Your present profile and skill base."},
        {"label": "1 Year", "title": one_year, "detail": "Depends heavily on weekly consistency and portfolio completion."},
        {"label": "3 Years", "title": three_year, "detail": "Likely path if missing skills are closed and real projects are shipped."},
        {"label": "5 Years", "title": five_year, "detail": "A realistic upside path with internships, networking, and applied experience."},
    ]


def fallback_action_plan(
    missing_skills: list[str],
    career_goal: str = "",
    weekly_study_hours: int = 0,
    country: str = "",
) -> list[dict[str, str]]:
    focus = adaptive_learning_sequence(career_goal, missing_skills, country)
    weekly_focus = []
    for skill in focus[:3]:
        weekly_focus.append(f"Learn the core concepts of {skill}.")
        weekly_focus.append(f"Build a small {skill} exercise for your portfolio.")
    weekly_focus.extend(
        [
            "Improve resume bullets with measurable project outcomes.",
            f"Prepare interview answers for {career_goal or 'your target role'}.",
        ]
    )

    return [
        {"week": f"Week {index + 1}", "task": focus}
        for index, focus in enumerate(weekly_focus[:8])
    ]


def adaptive_learning_sequence(career_goal: str, missing_skills: list[str], country: str = "") -> list[str]:
    goal = career_goal.casefold()
    if "data analyst" in goal or ("analyst" in goal and "business" not in goal):
        base = ["Advanced Excel", "SQL", "Power BI", "Statistics", "Python", "Portfolio Dashboard"]
    elif "data scientist" in goal:
        base = ["Statistics", "Python", "Machine Learning", "SQL", "Data Visualization", "Portfolio Case Study"]
    elif "ai" in goal or "machine learning" in goal or "ml engineer" in goal:
        base = ["Python Advanced", "Machine Learning", "Deep Learning", "Computer Vision or NLP", "Docker", "Deployment"]
    elif "backend" in goal:
        base = ["Python", "FastAPI", "Databases", "Docker", "Cloud", "System Design"]
    elif "frontend" in goal:
        base = ["JavaScript", "React", "TypeScript", "Testing", "Design Systems", "Deployment"]
    elif "cyber" in goal or "security" in goal:
        base = ["Networking", "Linux", "Security Fundamentals", "SIEM", "Incident Response", "Cloud Security"]
    elif "cloud" in goal or "devops" in goal:
        base = ["Linux", "Docker", "Kubernetes", "CI/CD", "Terraform", "Monitoring"]
    elif "finance" in goal or "account" in goal or "investment" in goal:
        base = ["Excel", "Accounting", "Financial Modeling", "Valuation", "Power BI", "Business Communication"]
    elif "marketing" in goal:
        base = ["SEO", "Content Strategy", "Campaign Analytics", "Copywriting", "Google Ads", "Portfolio Campaign"]
    elif "law" in goal or "legal" in goal or "lawyer" in goal:
        base = ["Legal Research", "Contract Drafting", "Compliance", "Case Analysis", "Legal Writing", "Portfolio Memo"]
    elif "health" in goal or "medical" in goal or "clinical" in goal:
        base = ["Healthcare Operations", "Patient Care", "Public Health", "Compliance", "Data Analysis", "Quality Improvement"]
    elif "teacher" in goal or "education" in goal:
        base = ["Lesson Planning", "Curriculum Design", "Assessment", "Classroom Management", "Teaching Demo", "Student Feedback"]
    elif "designer" in goal or "ux" in goal or "creative" in goal:
        base = ["User Research", "Figma", "Wireframing", "Portfolio Case Study", "Usability Testing", "Presentation"]
    else:
        base = ["Core Role Skills", "Portfolio Project", "Tools Practice", "Deployment", "Interview Prep", "Applications"]

    sequence = []
    for skill in missing_skills + base:
        if skill and skill not in sequence:
            sequence.append(skill)
    if country == "Germany" and "German B1" not in sequence:
        sequence.append("German B1")
    while len(sequence) < 6:
        filler = f"{career_goal or 'Career'} Portfolio"
        if filler not in sequence:
            sequence.append(filler)
        else:
            sequence.append(f"Interview Practice {len(sequence) + 1}")
    return sequence[:6]


def monthly_learning_task(skill: str, difficulty: str) -> str:
    if difficulty == "light":
        return f"Study {skill} for 3 focused sessions each week."
    if difficulty == "intensive":
        return f"Complete an advanced {skill} module and document key notes."
    return f"Complete a structured learning path for {skill}."


def monthly_project_task(skill: str, career_goal: str, country: str) -> str:
    country_context = f" for {country}" if country else ""
    return f"Apply {skill} in a {career_goal or 'career'} project{country_context}."
