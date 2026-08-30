from __future__ import annotations

from typing import Any

from services.career_knowledge import (
    build_transition_plan,
    discover_careers,
    interview_preparation,
    learning_recommendations,
)


MENTOR_PROFESSIONS = [
    "Software Engineering",
    "Artificial Intelligence",
    "Machine Learning",
    "Data Science",
    "Cyber Security",
    "Cloud Computing",
    "DevOps",
    "Civil Engineering",
    "Mechanical Engineering",
    "Electrical Engineering",
    "Electronics Engineering",
    "Architecture",
    "Business",
    "Management",
    "Finance",
    "Marketing",
    "Sales",
    "Human Resources",
    "Hospitality",
    "Hotel Management",
    "Tourism",
    "Journalism",
    "Media",
    "Law",
    "Healthcare",
    "Medicine",
    "Nursing",
    "Pharmacy",
    "Pilot",
    "Aviation",
    "Graphic Design",
    "UI/UX",
    "Interior Design",
    "Product Design",
    "Fashion Design",
    "Animation",
    "Game Development",
    "Teaching",
    "Research",
    "Government Jobs",
    "UPSC",
    "Entrepreneurship",
    "Freelancing",
    "Study Abroad",
    "Higher Studies",
]


MENTOR_THEMES = [
    "What should I learn next for {profession}?",
    "How can I improve my resume for {profession}?",
    "Which certifications matter most for {profession}?",
    "What projects or portfolio proof should I build for {profession}?",
    "How should I prepare for {profession} interviews?",
    "How can I get an internship or first role in {profession}?",
]


GENERAL_MENTOR_QUESTIONS = [
    "How can I improve my ATS score?",
    "How can I negotiate salary professionally?",
    "How should I improve my LinkedIn profile?",
    "How can I build a stronger GitHub portfolio?",
    "How do I prepare for remote jobs?",
    "How can I improve communication skills?",
    "How can I build leadership proof as a student?",
    "How do I switch careers without starting from zero?",
    "How should I choose between higher studies and a job?",
    "How can I increase my Resume Match Score?",
    "What should I do in the next 30 days?",
    "How do I prioritize missing skills?",
    "How do I explain career gaps?",
    "How do I write better project bullet points?",
    "How do I prepare for HR interviews?",
    "How do I create a portfolio if my field is non-technical?",
    "How do I target companies in another country?",
    "How do I plan a weekly learning routine?",
    "How do I prove impact in my resume?",
    "How can I become industry ready faster?",
]


def get_mentor_question_library() -> list[str]:
    questions = []
    for profession in MENTOR_PROFESSIONS:
        for template in MENTOR_THEMES:
            questions.append(template.format(profession=profession))
    questions.extend(GENERAL_MENTOR_QUESTIONS)
    return questions[:320]


def build_mentor_context(
    *,
    profile: Any,
    resume: Any,
    github_analysis: Any,
    country_intelligence: Any,
    roadmap: list[dict[str, Any]],
    missing_skills: list[str],
    resume_match: Any,
) -> dict[str, Any]:
    return {
        "name": getattr(profile, "name", "") or "there",
        "career_goal": getattr(profile, "career_goal", "") or "your target career",
        "country": getattr(profile, "target_country", "") or "your target country",
        "weekly_study_hours": getattr(profile, "weekly_study_hours", 0) or 0,
        "resume_strength": getattr(resume, "strength_score", None),
        "resume_skills": getattr(resume, "skills", []) if resume else getattr(profile, "skills", []),
        "projects": getattr(resume, "projects", []) if resume else getattr(profile, "projects", []),
        "experience": getattr(resume, "experience", []) if resume else getattr(profile, "internships", []),
        "certifications": getattr(resume, "certifications", []) if resume else getattr(profile, "certifications", []),
        "github_score": getattr(github_analysis, "github_score", None),
        "github_recommendations": getattr(github_analysis, "recommendations", []) if github_analysis else [],
        "country_demand": getattr(country_intelligence, "demand_level", ""),
        "country_skills": getattr(country_intelligence, "most_required_skills", []) if country_intelligence else [],
        "roadmap": roadmap,
        "missing_skills": missing_skills,
        "resume_match": getattr(resume_match, "overall_match", None),
        "critical_missing": getattr(resume_match, "critical_missing_skills", []) if resume_match else missing_skills[:3],
        "important_skills": getattr(resume_match, "important_skills", []) if resume_match else missing_skills[3:7],
        "match_suggestions": getattr(resume_match, "improvement_suggestions", []) if resume_match else [],
    }


def answer_mentor_question(question: str, context: dict[str, Any], history: list[dict[str, str]] | None = None) -> str:
    normalized = question.casefold()
    history = history or []

    if any(term in normalized for term in ["review my resume", "resume review", "review resume"]):
        return resume_review(context)
    if any(term in normalized for term in ["career suits", "suits me", "career fit", "what career"]):
        return career_fit_advice(question, context)
    if any(term in normalized for term in ["switch", "transition", "change career"]):
        return transition_advice(question, context)
    if any(term in normalized for term in ["higher studies", "masters", "mba", "mtech", "study abroad"]):
        return higher_studies_advice(context)
    if any(term in normalized for term in ["salary", "expect", "pay"]):
        return salary_advice(context)
    if any(term in normalized for term in ["move abroad", "country", "opportunities abroad", "visa"]):
        return country_advice(context)
    if any(term in normalized for term in ["companies", "target companies", "where should i apply"]):
        return company_advice(context)
    if any(term in normalized for term in ["learn next", "next learn", "what should i learn", "learn now"]):
        return learning_advice(context)
    if any(term in normalized for term in ["certification", "certificate", "cert"]):
        return certification_advice(context)
    if any(term in normalized for term in ["interview", "questions", "prepare"]):
        return interview_questions(context)
    if "github" in normalized:
        return github_advice(context)
    if any(term in normalized for term in ["resume match", "match score", "increase my score", "increase score"]):
        return match_score_advice(context)
    if any(term in normalized for term in ["roadmap", "plan", "weeks", "month"]):
        return roadmap_advice(context)

    return general_answer(context, history)


def resume_review(context: dict[str, Any]) -> str:
    score = context.get("resume_strength")
    match = context.get("resume_match")
    projects = context.get("projects", [])
    experience = context.get("experience", [])
    certifications = context.get("certifications", [])
    missing = context.get("critical_missing", [])

    lines = [
        f"For {context['career_goal']} in {context['country']}, your resume is strongest where it shows concrete skills and proof of work.",
    ]
    if score is not None:
        lines.append(f"Resume Strength: {score}%.")
    if match is not None:
        lines.append(f"Resume Match Score: {match}%.")
    if projects:
        lines.append("Your projects help, but make sure each one states the problem, stack, and measurable result.")
    else:
        lines.append("Your biggest resume gap is project proof. Add at least one role-specific project.")
    if not experience:
        lines.append("Experience is not clearly visible, so add internships, freelance, lab, or volunteer work if available.")
    if not certifications:
        lines.append("Certifications are not prominent. A targeted certificate can improve credibility.")
    if missing:
        lines.append("Critical missing skills to address: " + ", ".join(missing[:4]) + ".")
    return "\n\n".join(lines)


def learning_advice(context: dict[str, Any]) -> str:
    roadmap = context.get("roadmap", [])
    critical = context.get("critical_missing", [])
    weekly_hours = context.get("weekly_study_hours", 0)
    first_focus = roadmap[0]["focus"] if roadmap else (critical[0] if critical else "portfolio building")
    second_focus = roadmap[1]["focus"] if len(roadmap) > 1 else None

    answer = [
        f"Learn **{first_focus}** next because it is closest to your current {context['career_goal']} gap.",
        f"With {weekly_hours} study hours per week, keep the plan focused: learn, build, then document proof.",
    ]
    if second_focus:
        answer.append(f"After that, move to **{second_focus}** so your roadmap progresses without repeating topics.")
    if critical:
        answer.append("Do not skip these critical gaps: " + ", ".join(critical[:3]) + ".")
    return "\n\n".join(answer)


def certification_advice(context: dict[str, Any]) -> str:
    career_knowledge = context.get("career_knowledge", {})
    known_certs = career_knowledge.get("preferred_certifications", []) if isinstance(career_knowledge, dict) else []
    if known_certs:
        certs = list(known_certs)
        if context["country"] == "Germany":
            certs.append("German B1 language certification")
        return "Best certification path:\n\n" + "\n".join(f"- {cert}" for cert in certs[:4])

    goal = context["career_goal"].casefold()
    country = context["country"]
    if "ai" in goal or "machine learning" in goal:
        certs = ["Google Professional Machine Learning Engineer", "AWS Machine Learning Specialty", "DeepLearning.AI Machine Learning Specialization"]
    elif "data" in goal:
        certs = ["Google Data Analytics", "Microsoft PL-300 Power BI", "IBM Data Analyst"]
    elif "cloud" in goal or "devops" in goal:
        certs = ["AWS Solutions Architect Associate", "Certified Kubernetes Application Developer", "Terraform Associate"]
    elif "cyber" in goal or "security" in goal:
        certs = ["CompTIA Security+", "Certified Ethical Hacker", "Google Cybersecurity Certificate"]
    else:
        certs = ["AWS Cloud Practitioner", "Google Project Management", "role-specific portfolio certification"]

    if country == "Germany":
        certs.append("German B1 language certification")
    return "Best certification path:\n\n" + "\n".join(f"- {cert}" for cert in certs[:4])


def interview_questions(context: dict[str, Any]) -> str:
    prep = interview_preparation(str(context["career_goal"]))
    questions = []
    questions.extend(prep["hr_questions"][:2])
    questions.extend(prep["technical_questions"][:4])
    questions.extend(prep["case_study_questions"][:2])
    questions.append(f"How would you improve your profile for the {context['country']} market?")
    return "Practice these interview questions:\n\n" + "\n".join(f"- {question}" for question in questions)


def github_advice(context: dict[str, Any]) -> str:
    score = context.get("github_score")
    recommendations = context.get("github_recommendations", [])
    lines = []
    if score is not None:
        lines.append(f"Your GitHub Score is {score}%.")
    if recommendations:
        lines.append("Highest-impact GitHub fixes:\n" + "\n".join(f"- {item}" for item in recommendations[:4]))
    else:
        lines.append("Improve GitHub by pinning 3 strong repositories, adding READMEs, screenshots, setup steps, and deployed demos.")
    lines.append(f"Build one flagship {context['career_goal']} project and make the README recruiter-friendly.")
    return "\n\n".join(lines)


def match_score_advice(context: dict[str, Any]) -> str:
    suggestions = context.get("match_suggestions", [])
    critical = context.get("critical_missing", [])
    lines = []
    if context.get("resume_match") is not None:
        lines.append(f"Your current Resume Match Score is {context['resume_match']}%.")
    if suggestions:
        lines.append("To raise it fastest:")
        lines.extend(f"- {item['suggestion']} Why: {item['why']}" for item in suggestions[:5])
    elif critical:
        lines.append("Add proof for these critical missing skills: " + ", ".join(critical[:4]) + ".")
    else:
        lines.append("Improve match score by adding measurable project outcomes and exact target-role keywords.")
    return "\n".join(lines)


def roadmap_advice(context: dict[str, Any]) -> str:
    roadmap = context.get("roadmap", [])
    if not roadmap:
        return "I need a generated roadmap first. Create your Career Twin, then I can explain the next steps."
    lines = [f"Here is your current roadmap for {context['career_goal']}:"]
    for item in roadmap[:6]:
        lines.append(f"- {item['month']}: {item['focus']}")
    return "\n".join(lines)


def career_fit_advice(question: str, context: dict[str, Any]) -> str:
    profile_like = type(
        "ProfileLike",
        (),
        {
            "degree": "",
            "branch": context.get("detected_domain", ""),
            "skills": context.get("resume_skills", []),
            "projects": context.get("projects", []),
        },
    )()
    recommendations = discover_careers(question + " " + " ".join(context.get("resume_skills", [])), profile_like)
    if not recommendations:
        return f"Your strongest current direction is {context['career_goal']} because it matches the dashboard context and current skill signals."
    lines = ["Career paths that fit your current signals:"]
    for item in recommendations:
        lines.append(f"- {item.career} ({item.fit_score}%): {item.explanation}")
    return "\n".join(lines)


def transition_advice(question: str, context: dict[str, Any]) -> str:
    background = context.get("detected_domain") or "current background"
    plan = build_transition_plan(str(background), str(context["career_goal"]))
    lines = [
        f"Transition: {plan['from_domain']} -> {plan['to_domain']}",
        f"Difficulty: {plan['difficulty']}. Timeline: {plan['timeline']}. Success Probability: {plan['success_probability']}%.",
        f"Why: {plan['why']}",
        "Roadmap:",
    ]
    lines.extend(f"- {step}" for step in plan["roadmap"][:5])
    if plan["required_certifications"]:
        lines.append("Certifications: " + ", ".join(plan["required_certifications"][:3]) + ".")
    return "\n".join(lines)


def higher_studies_advice(context: dict[str, Any]) -> str:
    career = context.get("career_knowledge", {})
    degrees = career.get("degree_requirements", []) if isinstance(career, dict) else []
    return (
        f"For {context['career_goal']}, higher studies are useful if they directly improve access to roles, visas, research, or regulated credentials.\n\n"
        + "Relevant degree directions: "
        + (", ".join(degrees[:4]) if degrees else "a role-specific master's or professional diploma")
        + ".\n\nIf you can build strong projects and internships faster, prioritize proof first; choose higher studies when the target country or role expects credentials."
    )


def salary_advice(context: dict[str, Any]) -> str:
    country = context.get("country")
    demand = context.get("country_demand") or "market dependent"
    career = context.get("career_knowledge", {})
    salary = career.get("salary", "market dependent") if isinstance(career, dict) else "market dependent"
    return f"For {context['career_goal']} in {country}, salary is {salary} and demand is {demand}. Your actual range depends on portfolio proof, internships, interview quality, and local hiring standards."


def country_advice(context: dict[str, Any]) -> str:
    skills = context.get("country_skills", [])
    return (
        f"For {context['career_goal']}, {context['country']} currently shows {context.get('country_demand') or 'market'} demand.\n\n"
        + "Improve country fit by proving: "
        + (", ".join(skills[:5]) if skills else "role skills, communication, and portfolio outcomes")
        + ". Also check visa rules, language expectations, and local salary bands before applying."
    )


def company_advice(context: dict[str, Any]) -> str:
    career = context.get("career_knowledge", {})
    companies = career.get("hiring_companies", []) if isinstance(career, dict) else []
    if not companies:
        companies = ["role-specific startups", "consulting firms", "large employers in your target country"]
    return "Target companies and employer types:\n\n" + "\n".join(f"- {company}" for company in companies[:6])


def general_answer(context: dict[str, Any], history: list[dict[str, str]]) -> str:
    memory_note = ""
    if history:
        memory_note = "I am using our previous messages in this session, plus your current dashboard context.\n\n"
    topics = "career fit, switching careers, higher studies, certifications, salary, country choice, companies, interviews"
    if context.get("detected_domain") == "Technology":
        topics += ", GitHub"
    topics += ", or Resume Match Score"
    return (
        memory_note
        + f"You are targeting **{context['career_goal']}** in **{context['country']}**. "
        + f"Ask me about {topics}."
    )
