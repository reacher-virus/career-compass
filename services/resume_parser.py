from __future__ import annotations

import re
import tempfile
import zipfile
from dataclasses import dataclass, field
from datetime import date
from html import unescape
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

from services.career_knowledge import (
    career_skill_terms,
    categorize_skills_for_domain,
    detect_candidate_domain,
)
from services.scoring import calibrated_score, has_senior_evidence


COMMON_SKILLS = {
    "AWS",
    "Azure",
    "C",
    "C++",
    "C#",
    "CI/CD",
    "Cloud Basics",
    "CSS",
    "Data Cleaning",
    "Data Visualization",
    "Deep Learning",
    "Docker",
    "Excel",
    "FastAPI",
    "Figma",
    "Firebase",
    "Flutter",
    "Git",
    "Google Ads",
    "HTML",
    "Java",
    "JavaScript",
    "Kubernetes",
    "Linux",
    "Machine Learning",
    "MLOps",
    "Networking",
    "NumPy",
    "Pandas",
    "Power BI",
    "Prompt Engineering",
    "Python",
    "React",
    "REST APIs",
    "ROS",
    "Security",
    "SQL",
    "Statistics",
    "System Design",
    "Tableau",
    "Terraform",
    "TypeScript",
    "Unity",
    "Django",
    "Flask",
    "TensorFlow",
    "PyTorch",
    "MongoDB",
    "PostgreSQL",
    "MySQL",
    "Leadership",
    "Communication",
    "Problem Solving",
    "Business Analytics",
    "SEO",
    "Content Strategy",
    "Email Marketing",
    "A/B Testing",
    "Financial Modeling",
    "Accounting",
    "Valuation",
    "Canva",
    "Photoshop",
    "English",
    "Hindi",
    "German",
    "Legal Research",
    "Contract Drafting",
    "Compliance",
    "Litigation",
    "Case Analysis",
    "Legal Writing",
    "Patient Care",
    "Clinical Research",
    "Medical Terminology",
    "Public Health",
    "Pharmacology",
    "Research Methods",
    "Literature Review",
    "Academic Writing",
    "Laboratory Techniques",
    "Lesson Planning",
    "Curriculum Design",
    "Assessment",
    "Classroom Management",
    "Market Research",
    "Campaign Analytics",
    "Copywriting",
    "Brand Strategy",
    "Recruitment",
    "HR Analytics",
    "Employee Relations",
    "CAD",
    "AutoCAD",
    "SolidWorks",
    "MATLAB",
    "Revit",
    "SketchUp",
    "Guest Relations",
    "Hotel Operations",
    "Event Planning",
    "Crop Science",
    "Soil Science",
    "Agri Business",
    "Current Affairs",
    "Policy Analysis",
    "Essay Writing",
    "Customer Discovery",
    "Pitching",
}

SKILL_CATEGORIES = {
    "Programming Languages": {"C", "C++", "C#", "Dart", "Java", "JavaScript", "Python", "R", "SQL", "TypeScript"},
    "Frameworks": {"Django", "FastAPI", "Firebase", "Flask", "Flutter", "React", "ROS", "Streamlit", "TensorFlow", "PyTorch", "Unity"},
    "Databases": {"MongoDB", "MySQL", "PostgreSQL", "SQL"},
    "Cloud": {"AWS", "Azure", "Cloud Basics", "Docker", "Kubernetes", "Terraform"},
    "AI/ML": {"AI Projects", "Data Analysis", "Deep Learning", "Machine Learning", "MLOps", "NumPy", "Pandas", "Statistics"},
    "DevOps": {"CI/CD", "Docker", "Kubernetes", "Linux", "Terraform"},
    "Business": {"Business Analytics", "Business Communication", "Stakeholder Management"},
    "Marketing": {"A/B Testing", "Content Strategy", "Email Marketing", "Google Ads", "SEO"},
    "Finance": {"Accounting", "Excel", "Financial Modeling", "Valuation"},
    "Design": {"Canva", "Figma", "Photoshop", "User Research"},
    "Soft Skills": {"Business Communication", "Communication", "Leadership", "Problem Solving", "Stakeholder Management", "User Research"},
    "Languages": {"English", "German", "Hindi"},
    "Visualization": {"Data Visualization", "Power BI", "Tableau"},
    "Tools": {"Excel", "Figma", "Git", "Google Ads", "Power BI", "Tableau"},
}


SECTION_ALIASES = {
    "skills": ["skills", "technical skills", "technologies", "tools", "core competencies", "professional skills"],
    "projects": [
        "projects",
        "academic projects",
        "personal projects",
        "software projects",
        "clinical projects",
        "audit engagements",
        "recruitment drives",
        "portfolio projects",
        "published articles",
        "hotel operations",
        "legal cases",
        "drug safety programs",
    ],
    "education": ["education", "academics", "qualifications"],
    "certifications": ["certifications", "certificates", "licenses", "licensure", "courses"],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "employment history",
        "internships",
        "articleship",
        "residency",
        "clinical rotation",
        "teaching experience",
        "research experience",
    ],
    "achievements": ["achievements", "awards", "honors", "accomplishments"],
    "languages": ["languages", "spoken languages", "language proficiency"],
}

CONFIDENCE_LOW_MESSAGE = "Not Found in Resume"


@dataclass
class ResumeParseResult:
    text: str
    skills: list[str] = field(default_factory=list)
    projects: list[str] = field(default_factory=list)
    education: list[str] = field(default_factory=list)
    certifications: list[str] = field(default_factory=list)
    experience: list[str] = field(default_factory=list)
    achievements: list[str] = field(default_factory=list)
    languages: list[str] = field(default_factory=list)
    name: str = ""
    email: str = ""
    phone: str = ""
    linkedin: str = ""
    github: str = ""
    portfolio: str = ""
    location: str = ""
    age: int | None = None
    degree: str = ""
    branch: str = ""
    university: str = ""
    start_year: int | None = None
    graduation_year: int | None = None
    current_year: str = "Not Specified"
    gpa: float | None = None
    current_designation: str = ""
    designation_confidence: float = 0.0
    extraction_status: str = "Failed"
    strength_score: int = 0
    completeness_score: int = 0
    industry_readiness_score: int = 0
    ats_readiness_score: int = 0
    overall_career_readiness_score: int = 0
    skill_categories: dict[str, list[str]] = field(default_factory=dict)
    structured_projects: list[dict[str, str]] = field(default_factory=list)
    structured_experience: list[dict[str, str]] = field(default_factory=list)
    structured_certifications: list[dict[str, str]] = field(default_factory=list)
    field_confidence: dict[str, float] = field(default_factory=dict)
    insights: list[str] = field(default_factory=list)
    detected_domain: str = "General"
    domain_confidence: float = 0.0
    domain_scores: dict[str, int] = field(default_factory=dict)

    def autofill(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "age": self.age,
            "degree": self.degree,
            "branch": self.branch,
            "current_year": self.current_year if self.current_year != "Not Specified" else "",
            "gpa": self.gpa,
            "skills": ", ".join(self.skills),
            "projects": "\n".join(format_project(project) for project in self.structured_projects) or "\n".join(self.projects),
            "certifications": "\n".join(format_certification(cert) for cert in self.structured_certifications) or "\n".join(self.certifications),
            "internships": "\n".join(format_experience(exp) for exp in self.structured_experience) or "\n".join(self.experience),
            "languages": ", ".join(self.languages),
            "achievements": "\n".join(self.achievements),
        }


def extract_resume_text(uploaded_file: Any) -> str:
    suffix = Path(uploaded_file.name).suffix.casefold() or ".pdf"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        temp_path = temp_file.name

    try:
        if suffix == ".pdf":
            return extract_pdf_text(temp_path)
        if suffix == ".docx":
            return extract_docx_text(temp_path)
        if suffix in {".jpg", ".jpeg", ".png"}:
            return extract_image_text(temp_path)
        if suffix in {".txt", ".text"}:
            return Path(temp_path).read_text(encoding="utf-8", errors="ignore").strip()
        raise RuntimeError("Unsupported resume format. Upload PDF, DOCX, TXT, JPG, JPEG, or PNG.")
    finally:
        Path(temp_path).unlink(missing_ok=True)


def extract_pdf_text(path: str) -> str:
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError("PyMuPDF is not installed. Install requirements.txt and try again.") from exc

    with fitz.open(path) as document:
        pages = [page.get_text("text") for page in document]
        extracted = "\n".join(pages).strip()
        if extracted:
            return extracted
        return extract_pdf_text_with_ocr(document)


def extract_pdf_text_with_ocr(document: Any) -> str:
    try:
        from PIL import Image
        import pytesseract
    except ImportError as exc:
        raise RuntimeError("No text could be extracted from this resume. OCR fallback requires pytesseract and Pillow.") from exc

    texts = []
    for page in document:
        pixmap = page.get_pixmap(matrix=__import__("fitz").Matrix(2, 2), alpha=False)
        image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
        texts.append(pytesseract.image_to_string(image))
    extracted = "\n".join(texts).strip()
    if not extracted:
        raise RuntimeError("No text could be extracted from this resume.")
    return extracted


def extract_docx_text(path: str) -> str:
    try:
        with zipfile.ZipFile(path) as document:
            xml = document.read("word/document.xml")
    except KeyError as exc:
        raise RuntimeError("Could not read DOCX text from this resume.") from exc

    root = ElementTree.fromstring(xml)
    namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    paragraphs = []
    for paragraph in root.findall(".//w:p", namespace):
        text = "".join(node.text or "" for node in paragraph.findall(".//w:t", namespace))
        if text.strip():
            paragraphs.append(text.strip())
    return "\n".join(paragraphs)


def extract_image_text(path: str) -> str:
    try:
        from PIL import Image
        import pytesseract
    except ImportError as exc:
        raise RuntimeError("Image resume OCR requires pytesseract and Pillow. Install OCR dependencies and try again.") from exc

    try:
        return pytesseract.image_to_string(Image.open(path)).strip()
    except Exception as exc:
        raise RuntimeError("OCR could not extract text from this image resume.") from exc


def parse_resume_text(text: str, careers: dict[str, dict[str, Any]]) -> ResumeParseResult:
    normalized_text = normalize_text(text)
    if not normalized_text:
        return ResumeParseResult(
            text="",
            extraction_status="Failed",
            insights=["No text could be extracted from this resume."],
        )

    sections = extract_sections(normalized_text)
    skill_bank = build_skill_bank(careers)

    result = ResumeParseResult(
        text=normalized_text,
        skills=detect_skills(normalized_text, skill_bank),
        projects=detect_section_items(sections.get("projects", "")) or detect_labeled_items(normalized_text, "projects"),
        education=detect_section_items(sections.get("education", "")) or detect_labeled_items(normalized_text, "education"),
        certifications=detect_section_items(sections.get("certifications", "")) or detect_labeled_items(normalized_text, "certifications"),
        experience=detect_section_items(sections.get("experience", "")) or detect_labeled_items(normalized_text, "experience"),
        achievements=detect_section_items(sections.get("achievements", "")) or detect_labeled_items(normalized_text, "achievements"),
        languages=detect_section_items(sections.get("languages", "")) or detect_labeled_items(normalized_text, "languages"),
        name=detect_name(normalized_text),
        email=detect_email(normalized_text),
        phone=detect_phone(normalized_text),
        linkedin=detect_linkedin(normalized_text),
        github=detect_github(normalized_text),
        portfolio=detect_portfolio(normalized_text),
        location=detect_location(normalized_text),
        age=detect_age(normalized_text),
        gpa=detect_gpa(normalized_text),
    )
    result.skill_categories = categorize_skills(result.skills)
    result.structured_projects = parse_projects(sections.get("projects", "")) or parse_projects("\n".join(result.projects))
    result.structured_experience = parse_experience(sections.get("experience", "")) or parse_experience("\n".join(result.experience))
    result.structured_certifications = parse_certifications(sections.get("certifications", "")) or parse_certifications("\n".join(result.certifications))
    result.degree = detect_degree(result.education, normalized_text)
    result.branch = detect_branch(result.education, normalized_text)
    result.university = detect_university(result.education, normalized_text)
    result.start_year, result.graduation_year = detect_education_years(result.education, normalized_text)
    result.current_year = infer_current_year(result.start_year, result.graduation_year)
    result.current_designation, result.designation_confidence = detect_current_designation(
        normalized_text,
        result.structured_experience,
        careers,
    )
    result.detected_domain, result.domain_confidence, result.domain_scores = detect_candidate_domain(
        normalized_text,
        result.skills,
        result.degree,
        result.branch,
    )
    result.skill_categories = categorize_skills_for_domain(result.skills, result.detected_domain) or categorize_skills(result.skills)
    result.field_confidence = calculate_field_confidence(result)
    result.extraction_status = determine_extraction_status(result)
    scores = calculate_resume_scores(result)
    result.strength_score = scores["resume_strength"]
    result.completeness_score = scores["resume_completeness"]
    result.industry_readiness_score = scores["industry_readiness"]
    result.ats_readiness_score = scores["ats_readiness"]
    result.overall_career_readiness_score = scores["overall_career_readiness"]
    result.insights = build_resume_insights(result)
    return result


def parse_uploaded_resume(uploaded_file: Any, careers: dict[str, dict[str, Any]]) -> ResumeParseResult:
    result = parse_resume_text(extract_resume_text(uploaded_file), careers)
    if result.extraction_status == "Failed" and not result.text:
        raise RuntimeError("No text could be extracted from this resume.")
    return result


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def build_skill_bank(careers: dict[str, dict[str, Any]]) -> list[str]:
    skills = set(COMMON_SKILLS)
    skills.update(career_skill_terms())
    for career in careers.values():
        skills.update(career.get("required_skills", []))
        skills.update(career.get("technical_skills", []))
        skills.update(career.get("soft_skills", []))
    return sorted(skills, key=lambda value: (-len(value), value.casefold()))


def detect_current_designation(
    text: str,
    structured_experience: list[dict[str, str]],
    careers: dict[str, dict[str, Any]],
) -> tuple[str, float]:
    for experience in structured_experience:
        role = (experience.get("role") or "").strip()
        if role:
            return role, 0.86

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    labels = [
        "current role",
        "current designation",
        "designation",
        "job title",
        "position",
        "role",
        "title",
    ]
    role_names = sorted(careers.keys(), key=lambda value: (-len(value), value.casefold()))
    for index, line in enumerate(lines[:60]):
        lower = line.casefold()
        for label in labels:
            if label in lower:
                tail = re.split(r":|-|–|—", line, maxsplit=1)
                candidate_text = tail[-1] if len(tail) > 1 else line
                matched = match_known_role(candidate_text, role_names)
                if matched:
                    return matched, 0.92
                if len(tail) == 1 and index + 1 < len(lines):
                    next_line = lines[index + 1]
                    next_match = match_known_role(next_line, role_names)
                    if next_match:
                        return next_match, 0.9
                    cleaned_next = clean_designation_candidate(next_line)
                    if cleaned_next:
                        return cleaned_next, 0.78
                cleaned = re.sub(r"(?i)\b(current role|current designation|designation|job title|position|role|title)\b", "", candidate_text)
                cleaned = cleaned.strip(" :-–—|")
                cleaned_candidate = clean_designation_candidate(cleaned)
                if cleaned_candidate:
                    return cleaned_candidate, 0.72

    for line in lines[:80]:
        matched = match_known_role(line, role_names)
        if matched:
            return matched, 0.82
    matched = match_known_role(text, role_names)
    if matched:
        return matched, 0.68
    return "", 0.0


def clean_designation_candidate(value: str) -> str:
    cleaned = re.sub(
        r"(?i)\b(headline|summary|profile|current designation|current role|designation|job title|position|role|title)\b",
        "",
        value,
    )
    cleaned = re.sub(r"^[\s:\-|/]+|[\s:\-|/]+$", "", cleaned)
    if not (3 <= len(cleaned) <= 80):
        return ""
    role_markers = r"\b(engineer|manager|officer|analyst|developer|designer|professor|doctor|nurse|pilot|lawyer|executive|associate|scientist|teacher)\b"
    if "/" in value and not re.search(role_markers, cleaned, flags=re.IGNORECASE):
        return ""
    if cleaned.casefold() in {"current", "designation", "headline", "profile", "summary"}:
        return ""
    return cleaned


def match_known_role(text: str, role_names: list[str]) -> str:
    normalized = text.casefold()
    for role in role_names:
        pattern = r"(?<![a-z0-9])" + re.escape(role.casefold()) + r"(?![a-z0-9])"
        if re.search(pattern, normalized):
            return role
    return ""


def detect_skills(text: str, skill_bank: list[str]) -> list[str]:
    found = []
    for skill in skill_bank:
        variants = semantic_skill_variants(skill)
        if any(re.search(r"(?<![a-zA-Z0-9+#.])" + re.escape(variant) + r"(?![a-zA-Z0-9+#.])", text, flags=re.IGNORECASE) for variant in variants):
            found.append(skill)
    return sorted(set(found), key=str.casefold)


def semantic_skill_variants(skill: str) -> set[str]:
    variants = {skill}
    normalized = skill.casefold()
    equivalents = {
        "construction supervision": {"site supervision", "site execution"},
        "financial reporting": {"financial statements", "financial statement analysis"},
        "autocad": {"autocad civil", "auto cad"},
        "python": {"python programming"},
        "communication": {"communication skills", "verbal communication"},
        "patient care": {"patient handling", "clinical care"},
        "recruitment": {"talent acquisition", "sourcing"},
        "rest apis": {"rest api", "api development"},
        "machine learning": {"ml", "predictive modeling"},
        "legal research": {"case law research"},
    }
    for canonical, values in equivalents.items():
        if normalized == canonical:
            variants.update(values)
    return variants


def categorize_skills(skills: list[str]) -> dict[str, list[str]]:
    categorized = {category: [] for category in SKILL_CATEGORIES}
    uncategorized = []
    for skill in skills:
        placed = False
        for category, category_skills in SKILL_CATEGORIES.items():
            if skill in category_skills:
                categorized[category].append(skill)
                placed = True
        if not placed:
            uncategorized.append(skill)
    if uncategorized:
        categorized["Tools"].extend(uncategorized)
    return {category: sorted(set(values), key=str.casefold) for category, values in categorized.items()}


def extract_sections(text: str) -> dict[str, str]:
    lines = text.splitlines()
    heading_to_section = {
        alias: section
        for section, aliases in SECTION_ALIASES.items()
        for alias in aliases
    }
    sections: dict[str, list[str]] = {}
    current_section = ""

    for line in lines:
        key = re.sub(r"[^a-z ]", "", line.casefold()).strip()
        matched_section = heading_to_section.get(key)
        if matched_section:
            current_section = matched_section
            sections.setdefault(current_section, [])
            continue
        if current_section:
            sections[current_section].append(line)

    return {section: "\n".join(content).strip() for section, content in sections.items()}


def detect_section_items(section_text: str, limit: int = 8) -> list[str]:
    if not section_text:
        return []

    items = []
    for line in section_text.splitlines():
        cleaned = re.sub(r"^[\-*•\d.)\s]+", "", line).strip()
        if 4 <= len(cleaned) <= 140 and not is_section_heading(cleaned):
            items.append(cleaned)
    return dedupe_preserve_order(items)[:limit]


def detect_labeled_items(text: str, section: str, limit: int = 8) -> list[str]:
    aliases = SECTION_ALIASES.get(section, [])
    items = []
    for line in text.splitlines():
        for alias in aliases:
            match = re.match(rf"\s*{re.escape(alias)}\s*[:\-]\s*(.+)$", line, flags=re.IGNORECASE)
            if match:
                value = match.group(1).strip()
                if value:
                    items.extend([part.strip() for part in re.split(r"\s*[|;]\s*", value) if part.strip()])
    return dedupe_preserve_order(items)[:limit]


def parse_projects(section_text: str) -> list[dict[str, str]]:
    projects = []
    for item in detect_section_items(section_text, limit=10):
        parts = [part.strip() for part in re.split(r"\s+[|–—-]\s+", item, maxsplit=2) if part.strip()]
        name = parts[0] if parts else item
        description = parts[-1] if len(parts) > 1 else item
        tech_stack = ", ".join(detect_skills(item, sorted(COMMON_SKILLS, key=lambda value: (-len(value), value.casefold()))))
        impact = detect_impact(item)
        projects.append(
            {
                "name": name,
                "tech_stack": tech_stack,
                "description": description,
                "impact": impact,
                "role": detect_project_role(item),
            }
        )
    return projects


def parse_experience(section_text: str) -> list[dict[str, str]]:
    experiences = []
    for item in detect_section_items(section_text, limit=10):
        duration = detect_duration(item)
        role = detect_role(item)
        company = detect_company(item)
        experiences.append(
            {
                "company": company,
                "role": role,
                "duration": duration,
                "responsibilities": item,
                "skills_used": ", ".join(detect_skills(item, sorted(COMMON_SKILLS, key=lambda value: (-len(value), value.casefold())))),
                "achievements": detect_impact(item),
            }
        )
    return experiences


def parse_certifications(section_text: str) -> list[dict[str, str]]:
    certifications = []
    for item in detect_section_items(section_text, limit=10):
        year_match = re.search(r"\b(20\d{2}|19\d{2})\b", item)
        provider = ""
        provider_match = re.search(r"\b(?:by|from|provider:)\s+([A-Za-z0-9 .&+-]+)", item, flags=re.IGNORECASE)
        if provider_match:
            provider = provider_match.group(1).strip()
        certifications.append(
            {
                "name": re.sub(r"\b(20\d{2}|19\d{2})\b", "", item).strip(" -|"),
                "provider": provider,
                "completion_year": year_match.group(1) if year_match else "",
            }
        )
    return certifications


def is_section_heading(value: str) -> bool:
    key = re.sub(r"[^a-z ]", "", value.casefold()).strip()
    return any(key in aliases for aliases in SECTION_ALIASES.values())


def detect_name(text: str) -> str:
    for line in text.splitlines()[:8]:
        if "@" in line or re.search(r"\d", line):
            continue
        words = line.split()
        if 2 <= len(words) <= 4 and all(word[:1].isalpha() for word in words):
            return line.title()
    return ""


def detect_email(text: str) -> str:
    match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    return match.group(0) if match else ""


def detect_phone(text: str) -> str:
    candidates = re.findall(r"(?:\+?\d[\d().\-\s]{7,}\d)", text)
    for candidate in candidates:
        digits = re.sub(r"\D", "", candidate)
        if 10 <= len(digits) <= 15 and not re.fullmatch(r"(?:19|20)\d{2}\s*[-–—]\s*(?:19|20)\d{2}", candidate.strip()):
            return candidate.strip()
    return ""


def detect_linkedin(text: str) -> str:
    match = re.search(r"(?:https?://)?(?:www\.)?linkedin\.com/[^\s]+", text, flags=re.IGNORECASE)
    return clean_url(match.group(0)) if match else ""


def detect_github(text: str) -> str:
    match = re.search(r"(?:https?://)?(?:www\.)?github\.com/[^\s]+", text, flags=re.IGNORECASE)
    return clean_url(match.group(0)) if match else ""


def detect_portfolio(text: str) -> str:
    urls = re.findall(r"(?:https?://)?(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}[^\s]*", text)
    for url in urls:
        if "linkedin.com" not in url.casefold() and "github.com" not in url.casefold():
            return clean_url(url)
    return ""


def detect_location(text: str) -> str:
    match = re.search(r"\b(?:location|address)\s*[:\-]\s*([A-Za-z ,.]+)", text, flags=re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""


def clean_url(url: str) -> str:
    return url.rstrip(".,;)").strip()


def detect_age(text: str) -> int | None:
    age_match = re.search(r"\bage\s*[:\-]?\s*(\d{1,2})\b", text, flags=re.IGNORECASE)
    if age_match:
        age = int(age_match.group(1))
        return age if 14 <= age <= 70 else None

    dob_match = re.search(
        r"\b(?:dob|date of birth)\s*[:\-]?\s*(\d{1,2})[\/\-.](\d{1,2})[\/\-.](\d{4})\b",
        text,
        flags=re.IGNORECASE,
    )
    if not dob_match:
        return None

    day, month, year = map(int, dob_match.groups())
    today = date.today()
    age = today.year - year - ((today.month, today.day) < (month, day))
    return age if 14 <= age <= 70 else None


def detect_gpa(text: str) -> float | None:
    patterns = [
        r"\b(?:gpa|cgpa)\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*/\s*10\b",
        r"\b(?:gpa|cgpa)\s*[:\-]?\s*(\d+(?:\.\d+)?)\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            value = float(match.group(1))
            if 0 <= value <= 10:
                return value
    return None


def detect_degree(education: list[str], text: str) -> str:
    degree_patterns = [
        r"\b(B\.?Tech|Bachelor of Technology|BE|B\.?E\.?|BSc|B\.?Sc|MSc|M\.?Sc|BBA|Bachelor of Business Administration|MBA|BCom|B\.?Com|MCom|M\.?Com|LLB|LLM|MBBS|BDS|BPharm|B\.?Pharm|BEd|B\.?Ed|BA|B\.?A\.?|MA|M\.?A\.?|BArch|B\.?Arch|M\.?Tech|Master of Technology|MS|BCA|MCA)\b",
    ]
    search_space = "\n".join(education + [text])
    for pattern in degree_patterns:
        match = re.search(pattern, search_space, flags=re.IGNORECASE)
        if match:
            return match.group(1).replace(".", "").upper()
    return ""


def detect_branch(education: list[str], text: str) -> str:
    branches = [
        "Computer Science",
        "Artificial Intelligence",
        "Data Science",
        "Information Technology",
        "Electronics",
        "Mechanical",
        "Electrical",
        "Cybersecurity",
        "Business Analytics",
        "Marketing",
        "Finance",
        "Human Resources",
        "Operations",
        "Commerce",
        "Accounting",
        "Banking",
        "Investment",
        "Corporate Law",
        "Criminal Law",
        "Civil Law",
        "Intellectual Property",
        "Cyber Law",
        "Medicine",
        "Nursing",
        "Pharmacy",
        "Physiotherapy",
        "Biotechnology",
        "Public Health",
        "Psychology",
        "Sociology",
        "Political Science",
        "History",
        "Economics",
        "English",
        "Journalism",
        "Photography",
        "Graphic Design",
        "Animation",
        "UI UX",
        "Fashion Design",
        "Physics",
        "Chemistry",
        "Mathematics",
        "Statistics",
        "Biology",
        "Education",
        "Hotel Management",
        "Architecture",
        "Agriculture",
    ]
    search_space = "\n".join(education + [text])
    for branch in branches:
        if re.search(re.escape(branch), search_space, flags=re.IGNORECASE):
            return branch
    return ""


def detect_university(education: list[str], text: str) -> str:
    search_lines = education or text.splitlines()
    for line in search_lines:
        if re.search(r"\b(university|college|institute|school)\b", line, flags=re.IGNORECASE):
            return line.strip()
    return ""


def detect_education_years(education: list[str], text: str) -> tuple[int | None, int | None]:
    search_space = "\n".join(education + [text])
    range_match = re.search(r"\b(20\d{2}|19\d{2})\s*(?:-|–|—|to)\s*(20\d{2}|19\d{2})\b", search_space)
    if range_match:
        return int(range_match.group(1)), int(range_match.group(2))
    years = [int(year) for year in re.findall(r"\b(20\d{2}|19\d{2})\b", search_space)]
    if len(years) >= 2:
        return min(years), max(years)
    if len(years) == 1:
        return None, years[0]
    return None, None


def infer_current_year(start_year: int | None, graduation_year: int | None) -> str:
    if not start_year or not graduation_year or graduation_year <= start_year:
        return "Not Specified"
    duration = graduation_year - start_year
    if duration < 2 or duration > 6:
        return "Not Specified"
    if date.today().year > graduation_year:
        return "Graduate"
    year_number = date.today().year - start_year
    if date.today().year == graduation_year:
        year_number = duration
    if year_number < 1 or year_number > duration:
        return "Not Specified"
    names = {1: "1st Year", 2: "2nd Year", 3: "3rd Year", 4: "4th Year"}
    return names.get(year_number, f"Year {year_number}")


def calculate_field_confidence(result: ResumeParseResult) -> dict[str, float]:
    confidence = {
        "name": 0.9 if result.name else 0.0,
        "email": 0.98 if result.email else 0.0,
        "phone": 0.85 if result.phone else 0.0,
        "linkedin": 0.95 if result.linkedin else 0.0,
        "github": 0.95 if result.github else 0.0,
        "portfolio": 0.75 if result.portfolio else 0.0,
        "location": 0.65 if result.location else 0.0,
        "degree": 0.9 if result.degree else 0.0,
        "branch": 0.85 if result.branch else 0.0,
        "university": 0.8 if result.university else 0.0,
        "start_year": 0.9 if result.start_year else 0.0,
        "graduation_year": 0.9 if result.graduation_year else 0.0,
        "current_year": 0.9 if result.current_year != "Not Specified" else 0.0,
        "cgpa": 0.95 if result.gpa is not None else 0.0,
        "current_designation": result.designation_confidence,
        "skills": min(1.0, len(result.skills) / 6) if result.skills else 0.0,
        "projects": min(1.0, len(result.projects) / 2) if result.projects else 0.0,
        "experience": min(1.0, len(result.experience) / 1) if result.experience else 0.0,
        "certifications": min(1.0, len(result.certifications) / 1) if result.certifications else 0.0,
        "detected_domain": result.domain_confidence,
    }
    return confidence


def calculate_resume_scores(result: ResumeParseResult, github_score: int = 0) -> dict[str, int]:
    years = infer_experience_years_from_resume(result)
    substantial_projects = len(result.structured_projects or result.projects)
    senior_evidence = has_senior_evidence(years, substantial_projects, len(result.certifications), result.achievements)
    education = 10 if result.education or result.degree else 0
    projects = min(substantial_projects, 4) / 4 * 18
    skills = min(len(result.skills), 12) / 12 * 25
    experience = min(len(result.experience), 4) / 4 * 18
    internships = 5 if any("intern" in item.casefold() for item in result.experience) else 0
    certifications = min(len(result.certifications), 4) / 4 * 9
    github = min(github_score, 93) * 0.03
    ats = calculate_ats_score(result) * 0.04
    resume_strength = round(education + projects + skills + experience + internships + certifications + github + ats)
    completeness_ratio = sum([bool(result.name), bool(result.skills), bool(result.education), bool(result.projects), bool(result.experience), bool(result.certifications)]) / 6
    completeness = round(62 + completeness_ratio * 33) if result.text else 0
    industry = round((skills / 25 * 38) + (projects / 18 * 30) + (experience / 18 * 24) + (certifications / 9 * 8))
    ats_readiness = calculate_ats_score(result)
    resume_strength = calibrated_score("resume_strength", resume_strength, exceptional=senior_evidence, floor=35)
    completeness = calibrated_score("resume_completeness", completeness, exceptional=senior_evidence, floor=45)
    industry = calibrated_score("industry_readiness", industry, exceptional=senior_evidence, floor=30)
    ats_readiness = calibrated_score("ats_readiness", ats_readiness, exceptional=senior_evidence, floor=35)
    overall = round(resume_strength * 0.34 + industry * 0.30 + ats_readiness * 0.20 + completeness * 0.16)
    genuine_fresher = bool((result.degree or result.education) and result.skills and (result.projects or result.certifications))
    early_professional = 2 <= years <= 5 or (result.experience and result.projects and len(result.skills) >= 4)
    if genuine_fresher:
        overall = max(overall, 66)
        resume_strength = max(resume_strength, 65)
        industry = max(industry, 58)
    if early_professional:
        overall = max(overall, 78)
        resume_strength = max(resume_strength, 76)
        industry = max(industry, 72)
    if senior_evidence:
        overall = max(overall, 89)
        resume_strength = max(resume_strength, 88)
        industry = max(industry, 86)
    return {
        "resume_strength": resume_strength,
        "resume_completeness": completeness,
        "industry_readiness": industry,
        "ats_readiness": ats_readiness,
        "overall_career_readiness": calibrated_score("overall_career_readiness", overall, exceptional=senior_evidence, floor=30),
    }


def calculate_ats_score(result: ResumeParseResult) -> int:
    score = 0
    score += 20 if result.name else 0
    score += 20 if result.skills else 0
    score += 15 if result.education else 0
    score += 15 if result.projects else 0
    score += 15 if result.experience else 0
    score += 10 if result.certifications else 0
    score += 5 if len(result.text) > 600 else 0
    return calibrated_score("ats_readiness", score, floor=0)


def infer_experience_years_from_resume(result: ResumeParseResult) -> int:
    years = [int(year) for year in re.findall(r"\b(20\d{2}|19\d{2})\b", result.text)]
    explicit = re.findall(r"\b(\d{1,2})\+?\s*(?:years|yrs)\b", result.text, flags=re.IGNORECASE)
    if explicit:
        return max(int(value) for value in explicit)
    if len(years) >= 2:
        return max(0, min(40, max(years) - min(years)))
    return min(5, len(result.experience))


def determine_extraction_status(result: ResumeParseResult) -> str:
    extracted_groups = [
        bool(result.name),
        bool(result.skills),
        bool(result.education),
        bool(result.certifications),
        bool(result.projects),
        bool(result.experience),
    ]
    extracted_count = sum(extracted_groups)
    if not result.text or extracted_count == 0:
        return "Failed"
    if result.name and result.skills and extracted_count >= 3:
        return "Success"
    return "Partial"


def build_resume_insights(result: ResumeParseResult) -> list[str]:
    insights = []
    if result.extraction_status == "Failed":
        return ["No text could be extracted from this resume."]

    if len(result.skills) >= 8:
        insights.append("Strong skill coverage detected across the resume.")
    else:
        insights.append("Add a clearer skills section with tools, languages, and frameworks.")

    if result.projects:
        insights.append(f"{len(result.projects)} project signal(s) found. Keep outcomes measurable where possible.")
    else:
        insights.append("Add 2-3 project entries with problem, tools used, and results.")

    if result.experience:
        insights.append("Experience or internship content was detected.")
    else:
        insights.append("Add internship, freelance, volunteer, or lab experience if available.")

    if result.certifications:
        insights.append("Certifications are visible and can support credibility.")
    else:
        insights.append("Relevant certifications could strengthen the profile for competitive roles.")

    for section_name, values in {
        "Degree": [result.degree],
        "Experience": result.experience,
        "Projects": result.projects,
        "Skills": result.skills,
    }.items():
        if not any(values):
            insights.append(f"We couldn't confidently extract {section_name}. Please review it manually.")

    return insights


def confidence_message(result: ResumeParseResult, field: str, value: object) -> str:
    if result.field_confidence.get(field, 0.0) < 0.6 or not value:
        return CONFIDENCE_LOW_MESSAGE
    return str(value)


def detect_impact(text: str) -> str:
    match = re.search(r"(\d+%|\d+\+?\s*(?:users|students|customers|records|accuracy|reduction|increase))", text, flags=re.IGNORECASE)
    return match.group(1) if match else ""


def detect_project_role(text: str) -> str:
    match = re.search(r"\b(?:role|my role)\s*[:\-]\s*([A-Za-z ]+)", text, flags=re.IGNORECASE)
    return match.group(1).strip() if match else ""


def detect_duration(text: str) -> str:
    match = re.search(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)?[a-z]*\s*20\d{2}\s*(?:-|–|—|to)\s*(?:present|current|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)?[a-z]*\s*20\d{2})\b", text, flags=re.IGNORECASE)
    return match.group(0) if match else ""


def detect_role(text: str) -> str:
    match = re.search(r"\b([A-Za-z ]*(?:Intern|Engineer|Developer|Analyst|Assistant|Manager|Designer))\b", text, flags=re.IGNORECASE)
    return match.group(1).strip() if match else ""


def detect_company(text: str) -> str:
    match = re.search(r"\b(?:at|@)\s+([A-Za-z0-9 .&+-]+)", text, flags=re.IGNORECASE)
    return match.group(1).strip() if match else ""


def format_project(project: dict[str, str]) -> str:
    parts = [project.get("name", ""), project.get("tech_stack", ""), project.get("description", ""), project.get("impact", ""), project.get("role", "")]
    return " | ".join(part for part in parts if part)


def format_experience(experience: dict[str, str]) -> str:
    parts = [
        experience.get("role", ""),
        experience.get("company", ""),
        experience.get("duration", ""),
        experience.get("responsibilities", ""),
        experience.get("skills_used", ""),
        experience.get("achievements", ""),
    ]
    return " | ".join(part for part in parts if part)


def format_certification(certification: dict[str, str]) -> str:
    parts = [certification.get("name", ""), certification.get("provider", ""), certification.get("completion_year", "")]
    return " | ".join(part for part in parts if part)


def dedupe_preserve_order(items: list[str]) -> list[str]:
    seen = set()
    deduped = []
    for item in items:
        key = item.casefold()
        if key not in seen:
            seen.add(key)
            deduped.append(item)
    return deduped
