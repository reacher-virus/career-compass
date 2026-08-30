from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

from models.user import UserProfile
from services.career_engine import calculate_readiness, calculate_success_probability, load_careers
from services.career_knowledge import get_career_knowledge, recommend_careers_for_profile
from services.country_intelligence import SUPPORTED_COUNTRIES, get_country_career_intelligence
from services.resume_matcher import analyze_resume_match
from services.resume_parser import parse_resume_text


@dataclass(frozen=True)
class ValidationResume:
    name: str
    text: str
    expected_terms: tuple[str, ...]
    allowed_domains: tuple[str, ...]


VALIDATION_RESUMES = [
    ValidationResume("Software Engineer", "Current Role: Software Engineer II\nBTech Computer Science\nSkills: Python Java Docker System Design Git\nExperience: Software Engineer at product company 3 years", ("Software", "Backend", "Engineer"), ("Technology",)),
    ValidationResume("Data Scientist", "Designation: Data Scientist\nMSc Statistics\nSkills: Python SQL Machine Learning Statistics Data Visualization\nExperience: Data Scientist 4 years", ("Data Scientist", "Machine Learning", "Analytics"), ("Technology",)),
    ValidationResume("AI Engineer", "Job Title: AI Engineer\nSkills: Python Deep Learning MLOps TensorFlow Docker\nExperience: AI Engineer 3 years", ("AI Engineer", "Machine Learning", "MLOps"), ("Technology",)),
    ValidationResume("Backend Developer", "Role: Backend Developer\nSkills: Python FastAPI SQL Docker REST APIs Git\nExperience: Backend Developer 3 years", ("Backend", "Software", "Developer"), ("Technology",)),
    ValidationResume("Frontend Developer", "Designation: Frontend Developer\nSkills: HTML CSS JavaScript React TypeScript UI Testing\nExperience: Frontend Developer 2 years", ("Frontend", "React", "Developer"), ("Technology", "Creative")),
    ValidationResume("DevOps Engineer", "Current Role: DevOps Engineer\nSkills: Linux Docker Kubernetes CI/CD Terraform Monitoring\nExperience: DevOps Engineer 4 years", ("DevOps", "Cloud", "Site Reliability"), ("Technology",)),
    ValidationResume("Cybersecurity Analyst", "Role: Cybersecurity Analyst\nSkills: SOC SIEM Incident Response Pen Testing Linux Security\nExperience: SOC Analyst 3 years", ("Cybersecurity", "SOC", "Security"), ("Technology",)),
    ValidationResume("Cloud Engineer", "Current Designation: Cloud Engineer\nSkills: AWS Linux Docker Kubernetes Terraform Networking\nExperience: Cloud Engineer 4 years", ("Cloud", "DevOps", "Platform"), ("Technology",)),
    ValidationResume("Finance Analyst", "Role: Finance Analyst\nSkills: Excel Financial Modeling Accounting Power BI Valuation\nExperience: Finance Analyst 3 years", ("Finance", "Financial", "FP&A"), ("Finance",)),
    ValidationResume("CA", "Current Designation: Senior Audit Associate\nChartered Accountant with 4 years at Deloitte\nSkills: Accounting Financial Reporting Audit Taxation Risk Analysis Excel\nCertifications: CA", ("Audit Manager", "Finance Manager", "Finance Controller", "Corporate Finance"), ("Finance",)),
    ValidationResume("Investment Banker", "Designation: Investment Banking Analyst\nSkills: Valuation Financial Modeling M&A Pitch Books Excel\nExperience: Investment Banking Analyst 3 years", ("Investment", "Portfolio", "Finance"), ("Finance",)),
    ValidationResume("Accountant", "Current Role: Accountant\nSkills: Accounting Taxation GST Tally Financial Reporting Excel\nExperience: Accountant 5 years", ("Accountant", "Tax", "Finance"), ("Finance",)),
    ValidationResume("HR", "Position: HR Business Partner\nMBA HR\nSkills: Recruitment Payroll HRIS Employee Relations Talent Acquisition\nExperience: HR Business Partner 5 years", ("HR", "Recruiter", "Talent"), ("Business",)),
    ValidationResume("Recruiter", "Role: Technical Recruiter\nSkills: Sourcing Interview Coordination HRIS Talent Acquisition Negotiation\nExperience: Recruiter 3 years", ("Recruiter", "Talent", "HR"), ("Business",)),
    ValidationResume("Teacher", "Current Designation: Teacher\nBEd English\nSkills: Lesson Planning Curriculum Design Assessment Classroom Management\nExperience: Teacher 5 years", ("Teacher", "Academic", "Curriculum"), ("Education",)),
    ValidationResume("Professor", "Position: Assistant Professor\nPhD Physics\nSkills: Research Methods Academic Writing Teaching Curriculum Design\nExperience: Assistant Professor 6 years", ("Professor", "Research", "Academic"), ("Education", "Science")),
    ValidationResume("Lawyer", "Current Designation: Legal Associate\nLLB Corporate Law\nSkills: Legal Research Contract Drafting Compliance Legal Writing\nExperience: Legal Associate 3 years", ("Legal", "Lawyer", "Counsel"), ("Law",)),
    ValidationResume("Civil Engineer", "Role: Civil Engineer\nBTech Civil Engineering\nSkills: AutoCAD STAAD Pro Construction Management Site Planning\nExperience: Civil Engineer 4 years", ("Civil", "Construction", "Structural"), ("Engineering", "Architecture")),
    ValidationResume("Mechanical Engineer", "Current Role: Mechanical Engineer\nSkills: CAD SolidWorks Manufacturing Quality Control MATLAB\nExperience: Mechanical Engineer 4 years", ("Mechanical", "Manufacturing", "Quality"), ("Engineering",)),
    ValidationResume("Electrical Engineer", "Designation: Electrical Engineer\nSkills: Circuit Design Power Systems MATLAB Safety\nExperience: Electrical Engineer 3 years", ("Electrical", "Power", "Instrumentation"), ("Engineering",)),
    ValidationResume("Architect", "Role: Architect\nBArch\nSkills: AutoCAD Revit Building Codes Sustainable Design\nExperience: Architect 4 years", ("Architect", "BIM", "Design"), ("Architecture", "Creative", "Engineering")),
    ValidationResume("Interior Designer", "Role: Interior Designer\nSkills: Space Planning Furniture Design Lighting Design AutoCAD Client Presentation\nExperience: Interior Designer 4 years", ("Interior", "Designer", "Space"), ("Architecture", "Creative")),
    ValidationResume("Graphic Designer", "Current Role: Graphic Designer\nSkills: Figma Canva Adobe Photoshop Visual Design Portfolio Development\nExperience: Graphic Designer 3 years", ("Designer", "Creative", "Art"), ("Creative",)),
    ValidationResume("UI/UX Designer", "Current Role: UX Designer\nSkills: Figma User Research Wireframing Prototyping Usability Testing\nExperience: UX Designer 3 years", ("UX", "Product Designer", "Designer"), ("Creative", "Technology")),
    ValidationResume("Doctor", "Current Role: Medical Officer\nMBBS\nSkills: Patient Care Diagnosis Clinical Decision Making Medical Records\nExperience: Medical Officer 4 years", ("Medical Officer", "Doctor", "Healthcare"), ("Healthcare",)),
    ValidationResume("Nurse", "Designation: Staff Nurse\nBSc Nursing\nSkills: Patient Care ICU Medication Administration Infection Control Clinical Documentation\nExperience: Staff Nurse 3 years", ("Nurse", "Clinical", "Healthcare"), ("Healthcare",)),
    ValidationResume("Pharmacist", "Current Role: Pharmacist\nBPharm\nSkills: Pharmacology Medication Counseling Drug Safety Patient Care\nExperience: Pharmacist 4 years", ("Pharmacist", "Pharmaceutical", "Drug Safety"), ("Healthcare",)),
    ValidationResume("Dentist", "Current Designation: Dentist\nBDS\nSkills: Patient Care Dental Procedures Diagnosis Clinical Documentation\nExperience: Dentist 4 years", ("Dentist", "Doctor", "Healthcare"), ("Healthcare",)),
    ValidationResume("Physiotherapist", "Role: Physiotherapist\nSkills: Rehabilitation Patient Assessment Exercise Therapy Clinical Documentation\nExperience: Physiotherapist 3 years", ("Physiotherapist", "Healthcare", "Clinical"), ("Healthcare",)),
    ValidationResume("Marketing Manager", "Current Role: Marketing Manager\nSkills: SEO Brand Strategy Campaign Analytics Content Strategy Google Ads\nExperience: Marketing Manager 5 years", ("Marketing", "Brand", "Growth"), ("Marketing",)),
    ValidationResume("Sales Executive", "Designation: Sales Executive\nSkills: CRM Negotiation Customer Relationship Sales Pipeline\nExperience: Sales Executive 2 years", ("Sales", "Account", "Business Development"), ("Business",)),
    ValidationResume("Business Analyst", "Current Role: Business Analyst\nSkills: Requirements Analysis Process Mapping Power BI Stakeholder Management\nExperience: Business Analyst 4 years", ("Business Analyst", "Operations", "Consultant"), ("Business",)),
    ValidationResume("Product Manager", "Designation: Product Manager\nMBA\nSkills: Product Strategy User Research Analytics Roadmapping Stakeholder Management\nExperience: Product Manager 5 years", ("Product Manager", "Program", "Strategy"), ("Business", "Technology")),
    ValidationResume("Supply Chain Manager", "Designation: Supply Chain Manager\nSkills: Logistics Procurement Vendor Management Operations Inventory Planning\nExperience: Supply Chain Manager 6 years", ("Supply Chain", "Logistics", "Procurement"), ("Business",)),
    ValidationResume("Logistics Manager", "Role: Logistics Manager\nSkills: Warehouse Operations Fleet Management Distribution Inventory Control\nExperience: Logistics Manager 5 years", ("Logistics", "Warehouse", "Supply Chain"), ("Business",)),
    ValidationResume("Hotel Manager", "Role: Hotel Manager\nHotel Management degree\nSkills: Guest Relations Hotel Operations Food Safety Event Planning\nExperience: Hotel Manager 5 years", ("Hotel", "Hospitality", "Restaurant"), ("Hospitality",)),
    ValidationResume("Chef", "Current Role: Chef\nSkills: Food Safety Menu Planning Kitchen Operations Guest Service\nExperience: Chef 6 years", ("Chef", "Food", "Restaurant"), ("Hospitality",)),
    ValidationResume("Journalist", "Current Role: Journalist\nSkills: Reporting Editing Interviewing Media Research Storytelling\nExperience: Journalist 4 years", ("Journalist", "Editor", "Media"), ("Creative",)),
    ValidationResume("Police Officer", "Designation: Police Officer\nSkills: Public Safety Investigation Law Enforcement Crisis Response\nExperience: Police Officer 5 years", ("Police", "Government", "Officer"), ("Government",)),
    ValidationResume("Government Officer", "Role: Administrative Officer\nSkills: Public Administration Policy Implementation Documentation Citizen Services\nExperience: Government Officer 5 years", ("Officer", "Public", "Administrative"), ("Government",)),
    ValidationResume("Scientist", "Current Designation: Research Scientist\nPhD Chemistry\nSkills: Research Methods Laboratory Techniques Academic Writing Data Analysis\nExperience: Scientist 5 years", ("Research", "Scientist", "Chemist"), ("Science",)),
    ValidationResume("Researcher", "Role: Research Associate\nSkills: Literature Review Research Methods Statistics Academic Writing\nExperience: Research Associate 3 years", ("Research", "Associate", "Scientist"), ("Science",)),
    ValidationResume("Biotechnologist", "Current Role: Biotechnologist\nSkills: Molecular Biology Cell Culture Bioprocessing Laboratory Techniques\nExperience: Biotechnologist 3 years", ("Biotechnologist", "Biotechnology", "Research"), ("Healthcare", "Science")),
    ValidationResume("Agricultural Officer", "Role: Agricultural Officer\nSkills: Crop Management Soil Science Farmer Advisory Sustainability\nExperience: Agricultural Officer 4 years", ("Agricultural", "Agronomist", "Farm"), ("Agriculture",)),
    ValidationResume("Marine Engineer", "Current Role: Marine Engineer\nSkills: Maritime Safety Ship Systems Maintenance Navigation Regulations\nExperience: Marine Engineer 4 years", ("Marine", "Ship", "Maritime"), ("Engineering",)),
    ValidationResume("Pilot", "Current Designation: Commercial Pilot\nSkills: Flight Operations Aviation Safety Navigation Crew Coordination\nExperience: Pilot 5 years", ("Pilot", "Aviation", "Flight"), ("Engineering",)),
    ValidationResume("Fashion Designer", "Role: Fashion Designer\nSkills: Textile Design Pattern Making Fashion Merchandising Portfolio Development\nExperience: Fashion Designer 4 years", ("Fashion", "Designer", "Merchandiser"), ("Creative",)),
    ValidationResume("Pharmaceutical Scientist", "Role: Pharmaceutical Scientist\nSkills: Formulation Drug Safety Quality Control Clinical Trials\nExperience: Pharmaceutical Scientist 4 years", ("Pharmaceutical", "Drug", "Clinical"), ("Healthcare",)),
    ValidationResume("Renewable Energy Engineer", "Current Role: Renewable Energy Engineer\nSkills: Solar Energy Wind Energy Grid Operations Battery Systems\nExperience: Renewable Energy Engineer 4 years", ("Renewable", "Energy", "Solar"), ("Engineering",)),
    ValidationResume("Entrepreneur", "Role: Startup Founder\nSkills: Customer Discovery Sales Business Model Design Financial Planning Pitching\nExperience: Startup Founder 4 years", ("Founder", "Entrepreneur", "Business"), ("Entrepreneurship", "Business")),
]


LEAKAGE_TERMS = {
    "Technology": ["patient care", "icu", "medication administration", "infection control", "litigation", "taxation", "classroom management"],
    "Healthcare": ["dsa", "leetcode", "coding assessment", "system design", "cloud deployment", "fastapi", "react", "kubernetes", "devops"],
    "Finance": ["patient care", "infection control", "clinical assessment", "litigation", "classroom management", "leetcode", "coding assessment"],
    "Marketing": ["patient care", "infection control", "litigation", "dsa", "system design", "financial reporting"],
    "Law": ["patient care", "infection control", "financial modeling", "coding assessment", "system design", "cloud deployment"],
    "Engineering": ["patient care", "infection control", "litigation", "seo", "coding assessment", "leetcode"],
    "Architecture": ["patient care", "infection control", "coding assessment", "dsa", "taxation", "litigation"],
    "Education": ["coding assessment", "system design", "cloud deployment", "patient care", "taxation", "litigation"],
    "Business": ["patient care", "infection control", "coding assessment", "litigation"],
    "Creative": ["patient care", "infection control", "taxation", "coding assessment", "clinical assessment"],
    "Hospitality": ["coding assessment", "system design", "patient care", "litigation", "taxation"],
    "Agriculture": ["coding assessment", "system design", "patient care", "litigation", "taxation"],
    "Government": ["coding assessment", "system design", "patient care", "cloud deployment"],
    "Science": ["coding assessment", "leetcode", "sales pipeline", "guest relations", "litigation"],
}


def run_validation_suite() -> dict[str, object]:
    careers = load_careers()
    failures = []
    results = []
    samples = expanded_validation_resumes()
    duplicate_count = len(careers) - len({name.casefold() for name in careers})
    if duplicate_count:
        failures.append({"resume": "catalog", "reason": f"{duplicate_count} duplicate career titles found"})

    for index, sample in enumerate(samples):
        target_country = SUPPORTED_COUNTRIES[index % len(SUPPORTED_COUNTRIES)]
        resume = parse_resume_text(sample.text, careers)
        profile = UserProfile(
            name=sample.name,
            age=None,
            degree=resume.degree,
            branch=resume.branch,
            current_year="Professional",
            gpa=0.0,
            skills=resume.skills,
            projects=resume.projects,
            certifications=resume.certifications,
            internships=resume.experience,
            career_goal=resolve_validation_career_goal(sample, careers),
            target_country=target_country,
        )
        career_definition = get_career_knowledge(profile.career_goal, careers.get(profile.career_goal, {}))
        recommendations = recommend_careers_for_profile(profile, resume, careers, limit=5)
        country_intelligence = get_country_career_intelligence(profile.career_goal, profile.target_country, career_definition)
        resume_match = analyze_resume_match(resume, profile, career_definition)
        readiness = calculate_readiness(profile, career_definition)
        probability = calculate_success_probability(profile, readiness["score"], len(readiness["missing_skills"]))

        names = [item.career for item in recommendations]
        joined_names = " ".join(names).casefold()
        reasons = []
        if len(names) != len(set(name.casefold() for name in names)):
            reasons.append(f"Duplicate recommendations found: {names}")
        if any(item.fit_score >= 100 for item in recommendations):
            reasons.append("Unrealistic perfect recommendation score found")
        if len({item.fit_score for item in recommendations[:5]}) == 1 and len(recommendations) >= 5:
            reasons.append("Top recommendations have identical scores")
        if resume.extraction_status == "Failed":
            reasons.append("Resume parser failed to extract useful data")
        if not resume.skills:
            reasons.append("No skills extracted")
        if not resume.current_designation:
            reasons.append("No current designation extracted")
        if not any(term.casefold() in joined_names for term in sample.expected_terms):
            reasons.append(f"Top 5 recommendations were not relevant: {names}")

        wrong_domain_recs = [
            item.career
            for item in recommendations
            if str(careers.get(item.career, {}).get("domain", item.domain)) not in sample.allowed_domains
        ]
        if wrong_domain_recs:
            reasons.append(f"Recommendations crossed domains: {wrong_domain_recs}")

        leakage = leakage_terms_for_sample(sample, recommendations, country_intelligence, career_definition)
        if leakage:
            reasons.append("Cross-domain leakage detected: " + ", ".join(leakage))
        intelligence_missing = missing_career_intelligence(career_definition)
        if intelligence_missing:
            reasons.append("Career intelligence missing: " + ", ".join(intelligence_missing))
        if not country_intelligence.entry_salary or not country_intelligence.interview_process:
            reasons.append("Country intelligence missing salary or interview process")
        if country_intelligence.country != target_country:
            reasons.append(f"Country intelligence did not resolve selected country: {target_country}")
        if not country_intelligence.currency or not country_intelligence.average_salary:
            reasons.append("Country intelligence missing currency or average salary")
        if not country_intelligence.major_hiring_industries or not country_intelligence.visa_overview:
            reasons.append("Country intelligence missing industries or visa overview")
        if not (0 <= resume_match.overall_match <= 100):
            reasons.append("Resume match score outside 0-100")
        if not (20 <= readiness["score"] <= 93):
            reasons.append(f"Career readiness score unrealistic: {readiness['score']}")
        if not (20 <= probability <= 90):
            reasons.append(f"Success probability unrealistic: {probability}")
        if readiness["score"] == probability and profile.project_count and profile.internship_count:
            reasons.append("Independent scoring failed: readiness and success probability were identical for a complete profile")
        if profile.skills and profile.project_count and readiness["score"] < 35:
            reasons.append(f"Complete profile received unfairly low readiness: {readiness['score']}")
        if not readiness.get("positive_factors") or not readiness.get("improvement_factors"):
            reasons.append("Readiness explainability missing")

        passed = not reasons
        if not passed:
            failures.append({"resume": sample.name, "reason": reasons, "recommendations": names})
        results.append(
            {
                "resume": sample.name,
                "designation": resume.current_designation,
                "recommendations": names,
                "country_interview": country_intelligence.interview_process,
                "resume_match": resume_match.overall_match,
                "readiness": readiness["score"],
                "success_probability": probability,
                "passed": passed,
            }
        )

    return {
        "catalog_size": len(careers),
        "duplicates": duplicate_count,
        "total": len(samples),
        "passed": len(samples) - len([failure for failure in failures if failure.get("resume") != "catalog"]),
        "failed": len(failures),
        "failures": failures,
        "results": results,
    }


def expanded_validation_resumes() -> list[ValidationResume]:
    expanded = list(VALIDATION_RESUMES)
    for sample in VALIDATION_RESUMES:
        variants = [
            (
                f"{sample.name}\n"
                f"Professional Experience\n{sample.text}\n"
                "Core Competencies\n"
                "Communication Skills | Leadership | Problem Solving\n"
                "Achievements\nDelivered measurable outcomes in the current profession\n"
                "Languages\nEnglish\n"
            ),
            (
                f"Name: {sample.name} Candidate\n"
                f"Headline / Current Designation\n{sample.text.splitlines()[0]}\n"
                "Profile Summary\n"
                f"{sample.text}\n"
                "Selected Projects\nProfession-specific portfolio project with measurable impact\n"
                "Certifications\nRelevant professional certification\n"
                "Education\nDegree aligned to current profession\n"
            ),
            (
                f"{sample.name} Candidate\n"
                "SUMMARY\n"
                f"Experienced {sample.name.lower()} profile with role-specific achievements.\n"
                "EXPERIENCE\n"
                f"{sample.text}\n"
                "PROJECTS\n"
                "Built a profession-specific improvement initiative with measurable results.\n"
            ),
            (
                "CURRICULUM VITAE\n"
                f"Candidate: {sample.name}\n"
                f"{sample.text}\n"
                "KEY SKILLS\n"
                "Communication, Documentation, Stakeholder Management\n"
                "CERTIFICATIONS\n"
                "Professional development certificate\n"
            ),
            (
                f"{sample.name} Resume\n"
                "Current Position\n"
                f"{sample.text.splitlines()[0]}\n"
                "Education and Training\n"
                f"{sample.text}\n"
                "Impact\n"
                "Improved quality, efficiency, service, or delivery outcomes in the profession.\n"
            ),
            (
                f"{sample.name}\n"
                "Profile\n"
                f"{sample.text}\n"
                "Portfolio / Work Samples\n"
                "Role-specific work sample with documented process and outcome.\n"
                "Professional Strengths\n"
                "Problem Solving | Collaboration | Communication\n"
            ),
            (
                f"{sample.name} - Professional Bio\n"
                f"{sample.text}\n"
                "Responsibilities\n"
                "Handled core responsibilities aligned with the stated designation.\n"
                "Tools and Methods\n"
                "Used profession-appropriate tools, standards, and documentation.\n"
            ),
        ]
        extra_layouts = [
            ("Student Resume", "Academic Projects", "Campus learning project aligned with the profession."),
            ("Fresher Profile", "Internship Readiness", "Entry-level proof through coursework, labs, or practice work."),
            ("Experienced Resume", "Professional Achievements", "Improved measurable outcomes in the current role."),
            ("OCR Extract", "Scanned Resume Text", "Text order may be noisy but core profession signals remain present."),
            ("Manual Profile", "User Entered Details", "Profile was created manually from role, skills, and education."),
            ("GitHub Profile", "Portfolio Evidence", "Public work samples or repositories support the career direction."),
            ("No GitHub Profile", "Offline Portfolio", "Portfolio evidence comes from projects, reports, or case work."),
            ("International Resume", "Country Fit", "Candidate is exploring overseas opportunities in the same profession."),
            ("Career Switch Check", "Transition Intent", "No strong transition intent is stated; keep recommendations profession-specific."),
            ("ATS Resume", "Keyword Evidence", "Resume includes role-specific keywords and domain-specific skills."),
            ("Short Resume", "Compact Experience", "Minimal format with only the strongest professional signals."),
            ("Detailed Resume", "Expanded Experience", "Detailed profile with education, skills, experience, and project evidence."),
        ]
        for title, section, detail in extra_layouts:
            variants.append(
                (
                    f"{title}: {sample.name}\n"
                    f"{sample.text}\n"
                    f"{section}\n"
                    f"{detail}\n"
                    "Validation Note\n"
                    "The recommender should stay within the same profession family unless explicit transition evidence exists.\n"
                )
            )
        for variant in variants:
            expanded.append(
                ValidationResume(
                    name=sample.name,
                    text=variant,
                    expected_terms=sample.expected_terms,
                    allowed_domains=sample.allowed_domains,
                )
            )
    return expanded


def resolve_validation_career_goal(sample: ValidationResume, careers: dict[str, dict[str, Any]]) -> str:
    preferred = {
        "Government Officer": "Administrative Officer",
        "Pilot": "Commercial Pilot",
        "Sales Executive": "Sales Executive",
    }
    if preferred.get(sample.name) in careers:
        return preferred[sample.name]
    if sample.name in careers:
        return sample.name
    for term in sample.expected_terms:
        exact = next((name for name in careers if name.casefold() == term.casefold()), "")
        if exact:
            return exact
    for term in sample.expected_terms:
        contained = next((name for name in careers if term.casefold() in name.casefold()), "")
        if contained:
            return contained
    return sample.expected_terms[0]


def missing_career_intelligence(career_definition: dict[str, Any]) -> list[str]:
    required_fields = [
        "description",
        "degree_requirements",
        "certifications",
        "technical_skills",
        "soft_skills",
        "tools",
        "salary",
        "top_hiring_companies",
        "interview_pattern",
        "career_path",
        "learning_resources",
        "ai_impact",
        "future_growth",
        "remote_opportunities",
        "freelance_opportunities",
        "most_demanded_cities",
        "most_demanded_countries",
        "portfolio_requirements",
        "roadmap",
        "ats_keywords",
        "resume_keywords",
        "transition_paths",
        "industry_insights",
        "daily_responsibilities",
        "kpis",
        "licensing_requirements",
        "work_environment",
        "expected_growth",
    ]
    missing = []
    for field in required_fields:
        value = career_definition.get(field)
        if value in (None, "", [], {}):
            missing.append(field)
    return missing[:6]


def leakage_terms_for_sample(
    sample: ValidationResume,
    recommendations: list[Any],
    country_intelligence: Any,
    career_definition: dict[str, Any],
) -> list[str]:
    allowed = set(sample.allowed_domains)
    forbidden = set()
    for domain in allowed:
        forbidden.update(LEAKAGE_TERMS.get(domain, []))
    if not forbidden:
        return []

    content_parts: list[str] = []
    content_parts.extend(item.explanation for item in recommendations)
    content_parts.extend(country_intelligence.most_required_skills)
    content_parts.extend(country_intelligence.top_hiring_companies)
    content_parts.extend(country_intelligence.most_valuable_certifications)
    content_parts.extend(country_intelligence.interview_process)
    content_parts.extend(country_intelligence.insights)
    content_parts.extend(country_intelligence.most_valuable_programming_languages)
    content_parts.extend(country_intelligence.most_valuable_frameworks)
    content_parts.extend(career_definition.get("career_path", []))
    content_parts.extend(career_definition.get("required_skills", []))
    content_parts.extend(career_definition.get("interview_pattern", []))
    content = " | ".join(str(part) for part in content_parts).casefold()
    leaked = []
    for term in forbidden:
        pattern = r"(?<![a-z0-9])" + re.escape(term.casefold()) + r"(?![a-z0-9])"
        if re.search(pattern, content):
            leaked.append(term)
    return sorted(leaked)


if __name__ == "__main__":
    print(json.dumps(run_validation_suite(), indent=2))
