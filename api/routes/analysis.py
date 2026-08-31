from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException

from models.user import UserProfile
from services.career_engine import (
    calculate_readiness,
    calculate_success_probability,
    fallback_action_plan,
    fallback_future,
    fallback_roadmap,
    load_careers,
    score_label,
)
from services.career_knowledge import (
    get_career_knowledge,
    recommend_careers_for_profile,
)
from services.country_intelligence import (
    get_country_career_intelligence,
    salary_midpoint,
)
from services.resume_matcher import (
    analyze_resume_match,
    is_github_relevant,
)
from services.resume_parser import (
    ResumeParseResult,
    parse_resume_text,
)
from services.scoring import calibrated_score, calibrated_ratio_score
from services.gemini_service import (
    generate_explanation,
    generate_future_simulation,
    generate_roadmap,
)
from services.github_analyzer import GitHubAnalysis, GitHubRepoSummary

from api.schemas import (
    AnalyzeRequest,
    AnalysisResponse,
    DigitalTwinStage,
    ScorecardData,
    UserProfileSchema,
)

router = APIRouter(prefix="/api/analysis", tags=["Analysis"])


def dict_to_resume_obj(data: Dict[str, Any]) -> ResumeParseResult:
    return ResumeParseResult(
        text=data.get("text", ""),
        skills=data.get("skills", []),
        projects=data.get("projects", []),
        education=data.get("education", []),
        certifications=data.get("certifications", []),
        experience=data.get("experience", []),
        achievements=data.get("achievements", []),
        languages=data.get("languages", []),
        name=data.get("name", ""),
        email=data.get("email", ""),
        phone=data.get("phone", ""),
        linkedin=data.get("linkedin", ""),
        github=data.get("github", ""),
        portfolio=data.get("portfolio", ""),
        location=data.get("location", ""),
        age=data.get("age"),
        degree=data.get("degree", ""),
        branch=data.get("branch", ""),
        university=data.get("university", ""),
        start_year=data.get("start_year"),
        graduation_year=data.get("graduation_year"),
        current_year=data.get("current_year", "Not Specified"),
        gpa=data.get("gpa"),
        current_designation=data.get("current_designation", ""),
        extraction_status=data.get("extraction_status", "Success"),
        strength_score=data.get("strength_score", 0),
        completeness_score=data.get("completeness_score", 0),
        industry_readiness_score=data.get("industry_readiness_score", 0),
        ats_readiness_score=data.get("ats_readiness_score", 0),
        overall_career_readiness_score=data.get("overall_career_readiness_score", 0),
        skill_categories=data.get("skill_categories", {}),
        structured_projects=data.get("structured_projects", []),
        structured_experience=data.get("structured_experience", []),
        structured_certifications=data.get("structured_certifications", []),
        field_confidence=data.get("field_confidence", {}),
        insights=data.get("insights", []),
        detected_domain=data.get("detected_domain", "General"),
        domain_confidence=data.get("domain_confidence", 0.0),
    )


def dict_to_github_obj(data: Dict[str, Any]) -> GitHubAnalysis:
    repos = [
        GitHubRepoSummary(
            name=r.get("name", ""),
            description=r.get("description", ""),
            language=r.get("language", ""),
            stars=r.get("stars", 0),
            forks=r.get("forks", 0),
            watchers=r.get("watchers", 0),
            open_issues=r.get("open_issues", 0),
            size_kb=r.get("size_kb", 0),
            topics=r.get("topics", []),
            updated_at=r.get("updated_at", ""),
            url=r.get("url", ""),
            project_type=r.get("project_type", "General"),
            difficulty_level=r.get("difficulty_level", "Beginner"),
            has_license=r.get("has_license", False),
            has_readme_signal=r.get("has_readme_signal", False),
            has_releases_signal=r.get("has_releases_signal", False),
            quality_score=r.get("quality_score", 0),
        )
        for r in data.get("repos", [])
    ]
    return GitHubAnalysis(
        username=data.get("username", ""),
        repository_count=data.get("repository_count", 0),
        total_stars=data.get("total_stars", 0),
        total_forks=data.get("total_forks", 0),
        followers=data.get("followers", 0),
        following=data.get("following", 0),
        public_gists=data.get("public_gists", 0),
        years_active=data.get("years_active", 0),
        language_counts=data.get("language_counts", {}),
        category_counts=data.get("category_counts", {}),
        quality_distribution=data.get("quality_distribution", {}),
        technology_stack_counts=data.get("technology_stack_counts", {}),
        top_skills=data.get("top_skills", []),
        ai_ml_projects=[],
        web_projects=[],
        activity_level=data.get("activity_level", "Active"),
        github_score=data.get("github_score", 0),
        project_quality_score=data.get("project_quality_score", 0),
        portfolio_strength=data.get("portfolio_strength", "Developing"),
        most_starred_repository=data.get("most_starred_repository", ""),
        most_used_language=data.get("most_used_language", ""),
        open_source_contribution_level=data.get("open_source_contribution_level", "Active"),
        suitable_careers=data.get("suitable_careers", []),
        strengths=data.get("strengths", []),
        weaknesses=data.get("weaknesses", []),
        recommendations=data.get("recommendations", []),
        repos=repos,
    )


def compute_ai_confidence(
    profile: UserProfile,
    resume: Optional[ResumeParseResult],
    github_relevant: bool,
    github_analysis: Optional[GitHubAnalysis],
) -> ScorecardData:
    score = 42
    positives = []
    improvements = []
    if profile.career_goal:
        score += 7
        positives.append("Career goal is clearly defined")
    if profile.skills:
        score += min(len(profile.skills), 10) * 1.4
        positives.append(f"{len(profile.skills)} verifiable skills cataloged")
    if resume:
        if resume.extraction_status == "Success":
            score += 11
            positives.append("Structured resume parsing complete")
        elif resume.extraction_status == "Partial":
            score += 5
            improvements.append("Some resume fields need review")
        if resume.current_designation:
            score += 4
            positives.append(f"Current role detected: {resume.current_designation}")
    else:
        improvements.append("Uploading a resume increases profile confidence")
        
    if github_relevant:
        if github_analysis:
            score += 4
            positives.append("Live GitHub portfolio connected")
        else:
            improvements.append("Connect GitHub to verify technical projects")
            
    cap = 93 if resume and resume.extraction_status == "Success" and profile.skills and profile.project_count >= 2 else 86
    final_score = max(45, min(round(score), cap))
    return ScorecardData(
        score=final_score,
        label=score_label(final_score),
        positives=positives or ["Core profile foundation is active"],
        improvements=improvements or ["Profile is fully verified"],
        why="AI confidence measures data completeness, role alignment, resume clarity, and available code repository proof.",
    )


def compute_portfolio_strength(
    profile: UserProfile,
    resume: Optional[ResumeParseResult],
    github_analysis: Optional[GitHubAnalysis],
    career_knowledge: Dict[str, Any],
) -> ScorecardData:
    domain = str(career_knowledge.get("domain", "")).casefold()
    score = 30
    positives = []
    improvements = []
    if profile.project_count:
        score += min(profile.project_count, 4) * 9
        positives.append(f"{profile.project_count} project signal(s) present")
    else:
        improvements.append("Add at least 1-2 practical projects or case studies")
        
    if profile.internship_count:
        score += min(profile.internship_count, 3) * 5
        positives.append(f"{profile.internship_count} work/internship experience(s)")
        
    if profile.achievements:
        score += min(len(profile.achievements), 3) * 5
        positives.append("Documented honors & achievements")
        
    tech_domain = any(term in domain for term in ["software", "engineering", "data", "cybersecurity", "cloud", "technology", "ai"])
    if tech_domain:
        if github_analysis:
            score += calibrated_score("github", int(github_analysis.github_score)) * 0.18
            positives.append("Evaluated GitHub repository signals")
        else:
            improvements.append("Add public repository or demo links")
            
    cap = 92 if profile.project_count >= 4 and profile.internship_count >= 2 else 86
    final_score = max(30, min(round(score), cap))
    return ScorecardData(
        score=final_score,
        label=score_label(final_score),
        positives=positives or ["Portfolio proof is developing"],
        improvements=improvements or ["Maintain production projects & measurable impact"],
        why="Portfolio strength measures role-specific proof, projects, internships, GitHub activity, and achievements.",
    )


def compute_market_readiness(
    profile: UserProfile,
    readiness: Dict[str, Any],
    country_intelligence: Any,
    portfolio_strength: ScorecardData,
) -> ScorecardData:
    demand = str(getattr(country_intelligence, "demand_level", "")).casefold()
    score = 30
    positives = []
    improvements = []
    if "very high" in demand:
        score += 12
        positives.append("Target country has very high market demand")
    elif "high" in demand:
        score += 9
        positives.append("Target country has strong market demand")
    elif "medium" in demand:
        score += 5
        positives.append("Target country has steady hiring")
        
    score += calibrated_score("technical_skills", int(readiness.get("skill_coverage", 0))) * 0.20
    score += calibrated_score("portfolio_strength", int(portfolio_strength.score)) * 0.15
    
    if profile.internship_count:
        score += 6
        positives.append("Practical experience boosts candidate ranking")
    else:
        improvements.append("Acquire internships or freelance client projects")
        
    if readiness.get("missing_skills"):
        improvements.append("Bridge high-priority skills: " + ", ".join(readiness["missing_skills"][:3]))
        
    final_score = max(32, min(round(score), 90))
    return ScorecardData(
        score=final_score,
        label=score_label(final_score),
        positives=positives or ["Market position identified"],
        improvements=improvements or ["Keep advancing interview readiness and proof"],
        why="Market readiness benchmarks your profile against local market demand, required skills, and recruiter hiring criteria.",
    )


def build_digital_twin_stages(
    profile: UserProfile,
    readiness: Dict[str, Any],
    probability: int,
    country_intelligence: Any,
) -> List[DigitalTwinStage]:
    missing_skills = list(readiness.get("missing_skills", []))
    matched_skills = list(readiness.get("matched_skills", []))
    career_goal = profile.career_goal or "Target Career"
    current_role = profile.current_year if profile.current_year not in {"Not specified", "Not Specified", ""} else "Current Foundation"

    staged_skills = [
        matched_skills[:4] or profile.skills[:4] or ["Core Fundamentals"],
        (missing_skills[:3] or matched_skills[:3] or ["Portfolio Projects"])[:4],
        (missing_skills[:5] + ["Production Systems"])[:5] if missing_skills else matched_skills[:5],
        (missing_skills + ["System Design", "Leadership", "Mentoring"])[:6],
        (missing_skills + ["Strategy", "Architecture", "Industry Expertise"])[:7],
    ]

    confidences = [
        max(10, calibrated_score("ai_confidence", readiness["score"])),
        max(20, calibrated_score("ai_confidence", readiness["score"] + 8)),
        max(35, calibrated_score("ai_confidence", probability)),
        max(45, calibrated_score("ai_confidence", probability + 6)),
        max(55, calibrated_score("ai_confidence", probability + 10)),
    ]

    probabilities = [
        max(5, calibrated_score("success_probability", probability - 20)),
        max(10, calibrated_score("success_probability", probability - 5)),
        max(20, calibrated_score("success_probability", probability)),
        max(25, calibrated_score("success_probability", probability + 5)),
        max(30, calibrated_score("success_probability", probability + 9)),
    ]

    entry_salary = getattr(country_intelligence, "entry_salary", "Market Rate")
    mid_salary = getattr(country_intelligence, "mid_level_salary", "Market Rate")
    senior_salary = getattr(country_intelligence, "senior_salary", "Market Rate")
    lead_salary = f"{senior_salary}+"

    labels = ["Current You", "1 Year Future", "3 Year Future", "5 Year Future", "10 Year Future"]
    roles = [
        current_role,
        f"{career_goal.split()[0]} Associate / Intern" if career_goal else "Career Intern",
        career_goal,
        f"Senior {career_goal}",
        f"Principal / Lead {career_goal}",
    ]
    salaries = ["Current Profile", entry_salary, mid_salary, senior_salary, lead_salary]
    stages_names = ["Foundation", "Internship Ready", "Professional", "Advanced Contributor", "Leadership Track"]

    stages: List[DigitalTwinStage] = []
    for i in range(5):
        sal_val = salary_midpoint(salaries[i]) if i > 0 else 0
        stages.append(
            DigitalTwinStage(
                label=labels[i],
                role=roles[i],
                salary=salaries[i],
                skills=staged_skills[i],
                career_stage=stages_names[i],
                confidence=confidences[i],
                probability=probabilities[i],
                salary_value=sal_val,
            )
        )
    return stages


from api.routes.countries import normalize_country

@router.post("", response_model=AnalysisResponse)
def analyze_career_profile(request: AnalyzeRequest) -> AnalysisResponse:
    careers = load_careers()
    p_data = request.profile
    career_goal = p_data.career_goal or "Software Engineer"
    raw_country = p_data.target_country or "USA"
    target_country = normalize_country(raw_country)

    profile = UserProfile(
        name=p_data.name,
        age=p_data.age,
        degree=p_data.degree,
        branch=p_data.branch,
        current_year=p_data.current_year,
        gpa=p_data.gpa,
        skills=p_data.skills,
        projects=p_data.projects,
        certifications=p_data.certifications,
        internships=p_data.internships,
        languages=p_data.languages,
        achievements=p_data.achievements,
        weekly_study_hours=p_data.weekly_study_hours,
        career_goal=career_goal,
        target_country=target_country,
    )

    selected_career = careers.get(career_goal, {})
    career_knowledge = get_career_knowledge(career_goal, selected_career)
    github_relevant = is_github_relevant(career_knowledge)
    readiness = calculate_readiness(profile, selected_career)
    country_intelligence = get_country_career_intelligence(career_goal, target_country, selected_career)
    probability = calculate_success_probability(profile, readiness["score"], len(readiness["missing_skills"]))

    resume_obj = dict_to_resume_obj(request.resume) if request.resume else None
    github_obj = dict_to_github_obj(request.github_analysis) if request.github_analysis else None

    # Coach scorecards
    ai_conf = compute_ai_confidence(profile, resume_obj, github_relevant, github_obj)
    port_str = compute_portfolio_strength(profile, resume_obj, github_obj, career_knowledge)
    mkt_read = compute_market_readiness(profile, readiness, country_intelligence, port_str)

    skill_cov = ScorecardData(
        score=readiness.get("skill_coverage", 0),
        label=score_label(int(readiness.get("skill_coverage", 0))),
        positives=[f"Matched: {', '.join(readiness['matched_skills'][:4])}"] if readiness.get("matched_skills") else ["Skills ready to be built"],
        improvements=[f"Next: {', '.join(readiness['missing_skills'][:4])}"] if readiness.get("missing_skills") else ["Skills fully aligned"],
        why="Skill coverage compares verified profile skills against required skills for this career.",
    )

    readiness_card = ScorecardData(
        score=readiness["score"],
        label=readiness.get("label", score_label(int(readiness["score"]))),
        positives=readiness.get("positive_factors", []),
        improvements=readiness.get("improvement_factors", []),
        why=readiness.get("why", "Career readiness measures current overall profile strength."),
    )

    prob_card = ScorecardData(
        score=probability,
        label=score_label(probability),
        positives=[f"{len(readiness['matched_skills'])} matched skills", f"{profile.weekly_study_hours}h weekly effort"] if readiness['matched_skills'] else ["Profile initialised"],
        improvements=[f"Close {len(readiness['missing_skills'])} skill gaps"] if readiness['missing_skills'] else ["Maintain learning momentum"],
        why="Success probability models future career progression based on skill velocity and study hours.",
    )

    coach_scores = {
        "readiness": readiness_card,
        "success_probability": prob_card,
        "ai_confidence": ai_conf,
        "skill_coverage": skill_cov,
        "portfolio_strength": port_str,
        "market_readiness": mkt_read,
    }

    # Digital twin
    digital_twin = build_digital_twin_stages(profile, readiness, probability, country_intelligence)

    # Roadmap & Action Plan
    roadmap_items = fallback_roadmap(
        readiness["missing_skills"],
        career_goal,
        target_country,
        profile.weekly_study_hours,
    )
    action_plan_items = fallback_action_plan(
        readiness["missing_skills"],
        career_goal,
        profile.weekly_study_hours,
        target_country,
    )

    # Resume Match
    resume_match_dict = None
    if resume_obj:
        rm = analyze_resume_match(resume_obj, profile, career_knowledge, github_obj if github_relevant else None)
        resume_match_dict = {
            "overall_match": rm.overall_match,
            "weighted_scores": rm.weighted_scores,
            "strengths": rm.strengths,
            "weaknesses": rm.weaknesses,
            "critical_missing_skills": rm.critical_missing_skills,
            "important_skills": rm.important_skills,
            "nice_to_have_skills": rm.nice_to_have_skills,
            "improvement_suggestions": rm.improvement_suggestions,
        }

    # Recommended alternative careers
    rec_objects = recommend_careers_for_profile(profile, resume_obj, careers, limit=6)
    recommended = [
        {
            "career": r.career,
            "domain": r.domain,
            "fit_score": r.fit_score,
            "explanation": r.explanation,
            "matched_signals": r.matched_signals,
        }
        for r in rec_objects
    ]

    # Optional AI explanations
    ai_exp = generate_explanation(profile, readiness)
    ai_fut = generate_future_simulation(profile, readiness)
    ai_road = generate_roadmap(profile, readiness)

    return AnalysisResponse(
        profile=p_data,
        career_goal=career_goal,
        target_country=target_country,
        readiness=readiness,
        success_probability=probability,
        coach_scores=coach_scores,
        career_knowledge=career_knowledge,
        country_intelligence=country_intelligence.__dict__,
        digital_twin=digital_twin,
        roadmap=roadmap_items,
        action_plan=action_plan_items,
        resume_match=resume_match_dict,
        github_analysis=request.github_analysis,
        github_relevant=github_relevant,
        ai_explanation=ai_exp,
        ai_future=ai_fut,
        ai_roadmap=ai_road,
        recommended_careers=recommended,
        generated_at=datetime.now().isoformat(),
    )
