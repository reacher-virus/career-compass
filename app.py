from __future__ import annotations

import hashlib
import html
import json
import re
from datetime import datetime

import altair as alt
import pandas as pd
import streamlit as st

from database.db import recent_profiles, save_profile
from models.user import UserProfile
from services.career_engine import (
    calculate_readiness,
    calculate_success_probability,
    fallback_action_plan,
    fallback_future,
    fallback_roadmap,
    load_careers,
    score_label,
    split_multiline_or_csv,
)
from services.gemini_service import (
    generate_explanation,
    generate_future_simulation,
    generate_roadmap,
)
from services.github_analyzer import GitHubAnalysis, analyze_github_profile
from services.country_intelligence import (
    SUPPORTED_COUNTRIES,
    CountryCareerIntelligence,
    get_country_career_intelligence,
    salary_midpoint,
)
from services.resume_parser import CONFIDENCE_LOW_MESSAGE, ResumeParseResult, parse_uploaded_resume
from services.resume_parser import extract_resume_text
from services.resume_matcher import (
    JobDescriptionMatch,
    ResumeMatchAnalysis,
    analyze_resume_match,
    compare_resume_to_job_description,
    is_github_relevant,
)
from services.scoring import calibrated_score, calibrated_ratio_score
from services.ai_mentor import answer_mentor_question, build_mentor_context, get_mentor_question_library
from services.career_knowledge import (
    build_transition_plan,
    career_search_suggestions,
    get_career_knowledge,
    interview_preparation,
    learning_recommendations,
    recommend_careers_for_profile,
)


HTML_TAG_RE = re.compile(r"</?[a-z][\s\S]*?>", re.IGNORECASE)
SCRIPT_STYLE_RE = re.compile(r"<(script|style)[\s\S]*?</\1>", re.IGNORECASE)


st.set_page_config(
    page_title="Career Twin AI",
    page_icon="CT",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
    section.main > div { padding-top: 1.2rem; }
    div[data-testid="stMetric"] { min-height: 76px; }
    div[data-testid="stHorizontalBlock"] { gap: 0.85rem; }
    .block-container { padding-bottom: 3rem; }
    .career-section-anchor { scroll-margin-top: 92px; height: 1px; }
    .dashboard-section-nav {
        position: sticky;
        top: 0.25rem;
        z-index: 999;
        display: flex;
        gap: 0.45rem;
        overflow-x: auto;
        padding: 0.55rem;
        margin: 0.5rem 0 1rem;
        border: 1px solid rgba(128,128,128,.25);
        border-radius: 8px;
        background: color-mix(in srgb, var(--background-color) 92%, transparent);
        backdrop-filter: blur(12px);
    }
    .dashboard-section-nav a {
        white-space: nowrap;
        text-decoration: none;
        border: 1px solid rgba(128,128,128,.25);
        border-radius: 999px;
        padding: 0.35rem 0.7rem;
        color: inherit;
        font-size: 0.86rem;
    }
    .dashboard-section-nav a:hover,
    .dashboard-section-nav a:focus {
        border-color: #3b82f6;
        background: rgba(59, 130, 246, .12);
    }
    html { scroll-behavior: smooth; }
    @media (max-width: 760px) {
        div[data-testid="column"] { width: 100% !important; flex: 1 1 100% !important; }
        div[data-testid="stMetric"] { min-height: auto; }
        .stButton button, .stDownloadButton button, .stLinkButton a { width: 100%; }
        .dashboard-section-nav { top: 0; border-radius: 0; margin-left: -0.25rem; margin-right: -0.25rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def render_metric(label: str, value: str, note: str = "") -> None:
    with st.container(border=True):
        st.metric(label, value)
        if note:
            st.caption(note)


def section_anchor(section_id: str) -> None:
    st.markdown(f'<div id="{section_id}" class="career-section-anchor"></div>', unsafe_allow_html=True)


def render_dashboard_nav(has_resume: bool, has_github: bool) -> None:
    sections = [
        ("overview", "Overview"),
        ("career-twin", "Career Twin"),
        ("country-intelligence", "Country Intelligence"),
        ("career-intelligence", "Career Intelligence"),
        ("skill-gap", "Skill Gap"),
        ("career-match", "Career Match"),
        ("probability", "Final Readiness"),
        ("future-simulation", "Future Simulation"),
        ("roadmap", "Roadmap"),
        ("action-plan", "Action Plan"),
        ("feedback", "Feedback"),
    ]
    if has_resume:
        sections.insert(3, ("resume-analysis", "Resume Analysis"))
        sections.insert(4, ("resume-match", "Resume Match"))
    if has_github:
        sections.insert(6 if has_resume else 3, ("github-analysis", "GitHub Analysis"))
    links = "".join(f'<a href="#{section_id}">{label}</a>' for section_id, label in sections)
    st.markdown(f'<nav class="dashboard-section-nav" aria-label="Dashboard sections">{links}</nav>', unsafe_allow_html=True)


def render_feedback_contact() -> None:
    st.subheader("Feedback & Contact")
    st.caption("Share bugs, ideas, data corrections, or analysis issues directly with the developer.")

    feedback_type = st.selectbox(
        "Feedback Type",
        [
            "Bug Report",
            "Feature Request",
            "General Feedback",
            "Career Data Issue",
            "Resume Parsing Issue",
            "GitHub Analysis Issue",
        ],
        key="feedback_type",
    )
    rating = st.slider("Rating", min_value=1, max_value=5, value=5, key="feedback_rating")
    subject = st.text_input("Subject", key="feedback_subject", placeholder="Short summary")
    message = st.text_area("Message", key="feedback_message", placeholder="Describe what happened or what you would like improved.", height=140)

    upload_cols = st.columns(2)
    with upload_cols[0]:
        st.file_uploader("Screenshot upload", type=["png", "jpg", "jpeg"], key="feedback_screenshot")
    with upload_cols[1]:
        st.file_uploader("Resume upload", type=["pdf", "docx", "txt", "jpg", "jpeg", "png"], key="feedback_resume")

    body_lines = [
        f"Feedback Type: {feedback_type}",
        f"Rating: {rating}/5",
        "",
        "Message:",
        message or "",
    ]
    mail_subject = subject or f"Career Twin AI - {feedback_type}"
    mailto = (
        "mailto:yashpree237915@gmail.com"
        f"?subject={quote_mailto(mail_subject)}"
        f"&body={quote_mailto(chr(10).join(body_lines))}"
    )
    st.link_button("Send Email", mailto, use_container_width=True)
    st.caption("Developer contact: [yashpree237915@gmail.com](mailto:yashpree237915@gmail.com)")


def quote_mailto(value: str) -> str:
    from urllib.parse import quote

    return quote(value, safe="")


def render_footer() -> None:
    st.divider()
    st.markdown(
        """
        <div style="padding: 18px 0 8px; text-align:center; opacity:.9;">
            <div style="font-weight:700;">Developed by Yash Agnihotri </div>
            <div style="font-size:0.95rem;">Aspiring AI Engineer | Career Twin AI Creator</div>
            <div style="margin-top:8px;">
                <a href="https://github.com/REACHER-VIRUS" target="_blank" style="margin-right:14px; text-decoration:none;">GitHub</a></div>
            <div style="font-size:0.85rem; margin-top:8px;">© 2026 Career Twin AI. All Rights Reserved.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def github_username_from_url(value: str) -> str:
    cleaned = (value or "").strip().rstrip("/")
    if not cleaned:
        return ""
    cleaned = re.sub(r"^https?://", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"^www\.", "", cleaned, flags=re.IGNORECASE)
    if cleaned.casefold().startswith("github.com/"):
        cleaned = cleaned.split("/", 1)[1]
    return re.split(r"[/#?]", cleaned, maxsplit=1)[0].strip()


def analyze_github_to_state(username: str, *, force: bool = False, source: str = "manual") -> bool:
    username = github_username_from_url(username)
    if not username:
        st.session_state.github_error = "Enter a GitHub username."
        st.session_state.pop("github_analysis", None)
        return False
    existing = st.session_state.get("github_analysis")
    existing_username = github_username_from_url(getattr(existing, "username", ""))
    if not force and existing and existing_username.casefold() == username.casefold():
        st.session_state.github_username = existing_username or username
        st.session_state.github_error = ""
        st.session_state.github_analysis_skipped = True
        return False
    analysis = analyze_github_profile(username)
    st.session_state.github_username = username
    st.session_state.github_analysis = analysis
    st.session_state.github_analysis_username = username
    st.session_state.github_analysis_source = source
    st.session_state.github_analysis_skipped = False
    st.session_state.github_error = ""
    return True


def build_dashboard_report(
    profile: UserProfile,
    readiness: dict[str, object],
    probability: int,
    country_intelligence: CountryCareerIntelligence,
    career_knowledge: dict[str, object],
    resume: ResumeParseResult | None,
    github_analysis: GitHubAnalysis | None,
    resume_match: ResumeMatchAnalysis | None,
    roadmap_items: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "profile": {
            "name": profile.name,
            "degree": profile.degree,
            "branch": profile.branch,
            "current_year": profile.current_year,
            "career_goal": profile.career_goal,
            "target_country": profile.target_country,
            "weekly_study_hours": profile.weekly_study_hours,
            "skills": profile.skills,
            "projects": profile.projects,
            "certifications": profile.certifications,
            "experience": profile.internships,
            "languages": getattr(profile, "languages", []),
            "achievements": getattr(profile, "achievements", []),
        },
        "readiness": readiness,
        "success_probability": probability,
        "career_intelligence": career_knowledge,
        "country_intelligence": country_intelligence.__dict__,
        "resume": {
            "status": resume.extraction_status,
            "detected_domain": resume.detected_domain,
            "current_designation": resume.current_designation,
            "strength_score": resume.strength_score,
            "ats_readiness": resume.ats_readiness_score,
            "skills": resume.skills,
        } if resume else None,
        "github": {
            "username": github_analysis.username,
            "score": github_analysis.github_score,
            "repositories": github_analysis.repository_count,
            "languages": github_analysis.language_counts,
        } if github_analysis else None,
        "resume_match": {
            "overall_match": resume_match.overall_match,
            "weighted_scores": resume_match.weighted_scores,
            "critical_missing_skills": resume_match.critical_missing_skills,
        } if resume_match else None,
        "roadmap": roadmap_items,
    }


def build_pdf_report(report: dict[str, object]) -> bytes:
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError("PDF export requires PyMuPDF.") from exc

    doc = fitz.open()
    page = doc.new_page(width=595, height=842)
    y = 48

    def write_line(text: str, size: int = 10, bold: bool = False) -> None:
        nonlocal y, page
        if y > 790:
            page = doc.new_page(width=595, height=842)
            y = 48
        font = "helv" if not bold else "helv"
        page.insert_text((48, y), text[:105], fontsize=size, fontname=font)
        y += size + 8

    def write_section(title: str, description: str) -> None:
        nonlocal y
        if y > 755:
            write_line("")
        write_line(title, 14, True)
        for line in wrap_pdf_text(description, 96):
            write_line(line, 9)
        y += 4

    profile = report["profile"]
    write_line("Career Twin AI - Professional Career Intelligence Report", 18, True)
    write_line(f"Generated: {report['generated_at']}", 9)
    write_line("")
    write_line(f"Name: {profile['name'] or 'Not specified'}", 11)
    write_line(f"Career Goal: {profile['career_goal']} in {profile['target_country']}", 11)
    write_line(f"Career Readiness: {report['readiness']['score']}%", 11)
    write_line(f"Success Probability: {report['success_probability']}%", 11)
    write_line("")
    write_section(
        "Executive Summary",
        "This report summarizes the user's current career profile, target role fit, country market context, skill gaps, roadmap, and improvement priorities. Scores are directional coaching indicators based on available profile evidence, not fixed judgments.",
    )
    draw_score_bars(
        page,
        48,
        y,
        {
            "Readiness": int(report["readiness"]["score"]),
            "Success": int(report["success_probability"]),
            "ATS": int((report.get("resume") or {}).get("ats_readiness", report["readiness"].get("score", 0)) or 0),
        },
    )
    y += 86
    write_section(
        "Career Readiness",
        "Career Readiness measures current profile quality using education, skills, projects, certifications, experience, achievements, ATS quality, and consistency. It rewards visible strengths while identifying practical next improvements.",
    )
    write_section(
        "Success Probability",
        "Success Probability estimates future momentum based on current evidence, study consistency, portfolio proof, experience, and roadmap progress. Completing the roadmap should improve this projection over time.",
    )
    write_section(
        "AI Confidence",
        "AI Confidence reflects confidence in the recommendation based on profile completeness, resume extraction quality, career clarity, and available supporting evidence such as GitHub when relevant.",
    )
    write_section(
        "Skill Coverage",
        "Skill Coverage compares matched skills against selected-career requirements. Missing and recommended skills show the fastest areas to improve career fit.",
    )
    write_line("Matched Skills", 13, True)
    for item in report["readiness"].get("matched_skills", [])[:12]:
        write_line(f"- {item}")
    write_line("Missing Skills", 13, True)
    for item in report["readiness"].get("missing_skills", [])[:12]:
        write_line(f"- {item}")
    write_section(
        "Country Intelligence",
        "Country Intelligence explains whether the selected country is suitable for the target career using salary bands, demand, hiring trend, visa complexity, remote availability, industries, and future outlook.",
    )
    country = report["country_intelligence"]
    for key in [
        "currency",
        "average_salary",
        "demand_level",
        "entry_salary",
        "mid_level_salary",
        "senior_salary",
        "visa_difficulty",
        "market_growth",
        "hiring_trend",
        "remote_work_availability",
    ]:
        write_line(f"{key.replace('_', ' ').title()}: {country.get(key, '')}")
    if country.get("visa_overview"):
        for line in wrap_pdf_text("Visa Overview: " + country.get("visa_overview", ""), 96):
            write_line(line, 9)
    if country.get("major_hiring_industries"):
        write_line("Major Hiring Industries: " + ", ".join(country.get("major_hiring_industries", [])[:6]))
    career = report.get("career_intelligence", {})
    if career:
        write_section(
            "Career Match",
            "Career Match explains why the selected career aligns with the user's profile. It considers role skills, education, experience, certifications, portfolio proof, and missing requirements.",
        )
        write_section(
            "Portfolio Strength",
            "Portfolio Strength evaluates profession-specific proof. Technical roles may use GitHub, while non-technical careers rely on case studies, writing samples, clinical evidence, legal research, design work, or operational outcomes.",
        )
        write_section(
            "Market Readiness",
            "Market Readiness estimates competitiveness in the current job market using profile quality, country demand, role requirements, portfolio evidence, communication, and experience.",
        )
        write_line("Career Intelligence Details", 13, True)
        for key in ["daily_responsibilities", "kpis", "ats_keywords", "licensing_requirements"]:
            values = career.get(key, [])
            if isinstance(values, list):
                write_line(f"{key.replace('_', ' ').title()}: {', '.join(values[:4])}")
            elif values:
                write_line(f"{key.replace('_', ' ').title()}: {values}")
    if report.get("github"):
        github = report["github"]
        write_line("GitHub Analysis", 13, True)
        write_line(f"Username: {github['username']}")
        write_line(f"Score: {github['score']}% | Repositories: {github['repositories']}")
    if report.get("resume_match"):
        match = report["resume_match"]
        write_section(
            "Resume Match",
            "Resume Match compares the complete resume against the selected career or job description. It highlights keyword fit, semantic fit, technical fit, missing keywords, and hiring-readiness signals.",
        )
        write_line(f"Overall Match: {match['overall_match']}%")
    write_section(
        "Career Roadmap",
        "The roadmap turns missing skills into a practical learning plan. Completing each milestone should improve future career growth, interview readiness, and portfolio credibility.",
    )
    for item in report["roadmap"][:6]:
        write_line(f"{item['month']}: {item['focus']}")
        for week in item.get("weeks", [])[:4]:
            write_line(f"  {week['week']}: {week['milestone']}", 9)
    write_line("")
    write_line("Developed by Yash Agnihotri | Career Twin AI", 9)
    pdf = doc.tobytes()
    doc.close()
    return pdf


def draw_score_bars(page: object, x: int, y: int, scores: dict[str, int]) -> None:
    import fitz

    page.insert_text((x, y), "Score Snapshot", fontsize=13, fontname="helv")
    y += 16
    for label, score in scores.items():
        bounded = max(0, min(int(score), 100))
        page.insert_text((x, y + 9), f"{label}: {bounded}%", fontsize=9, fontname="helv")
        page.draw_rect(fitz.Rect(x + 115, y, x + 315, y + 10), color=(0.78, 0.78, 0.78), fill=(0.92, 0.92, 0.92))
        page.draw_rect(fitz.Rect(x + 115, y, x + 115 + bounded * 2, y + 10), color=(0.12, 0.38, 0.78), fill=(0.12, 0.38, 0.78))
        y += 18


def wrap_pdf_text(text: str, width: int) -> list[str]:
    words = str(text).split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) > width and current:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def render_ai_mentor_chat(context: dict[str, object]) -> None:
    st.session_state.setdefault("mentor_messages", [])

    with st.popover("AI Mentor Chat", use_container_width=True):
        st.caption("Personalized mentor using your resume, career goal, GitHub, country, roadmap, missing skills, and match scores.")
        quick_prompts = [
            "Review my resume.",
            "What should I learn next?",
            "Which certification should I do?",
            "Prepare interview questions.",
            "How can I increase my Resume Match Score?",
        ]
        if context.get("detected_domain") == "Technology":
            quick_prompts.insert(4, "Improve my GitHub.")
        mentor_library = get_mentor_question_library()
        selected_prompt = st.selectbox("Quick question", [""] + quick_prompts + mentor_library, key="mentor_quick_prompt")
        st.caption(f"{len(mentor_library)} profession-aware mentor questions available.")
        custom_prompt = st.text_area("Ask your mentor", value="", height=90, key="mentor_custom_prompt")

        if st.button("Ask Mentor", use_container_width=True):
            question = custom_prompt.strip() or selected_prompt.strip()
            if question:
                st.session_state.mentor_messages.append({"role": "user", "content": question})
                with st.spinner("Mentor is preparing a personalized answer..."):
                    answer = answer_mentor_question(question, context, st.session_state.mentor_messages)
                st.session_state.mentor_messages.append({"role": "assistant", "content": answer})
                st.success("Mentor response ready.")

        if st.button("Clear Mentor Memory", use_container_width=True):
            st.session_state.mentor_messages = []

        for message in st.session_state.mentor_messages[-10:]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


def render_circular_score(label: str, score: int, note: str = "") -> None:
    score = max(0, min(int(score), 100))
    badge = score_label(score)
    st.markdown(
        f"""
        <div style="border:1px solid rgba(128,128,128,.25); border-radius:14px; padding:16px; text-align:center;">
            <div style="width:112px; height:112px; border-radius:50%; margin:0 auto 10px;
                background: conic-gradient(#4f8cff {score * 3.6}deg, rgba(128,128,128,.18) 0deg);
                display:flex; align-items:center; justify-content:center;">
                <div style="width:78px; height:78px; border-radius:50%; background:rgba(14,17,23,.96);
                    display:flex; align-items:center; justify-content:center; font-size:22px; font-weight:700;">
                    {score}%
                </div>
            </div>
            <div style="font-weight:700;">{label}</div>
            <div style="font-size:12px; opacity:.84; margin-top:2px;">{badge}</div>
            <div style="font-size:12px; opacity:.72;">{html.escape(note)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_progress_steps(current_step: int) -> None:
    steps = [
        ("01", "Create Profile"),
        ("02", "Analyze Skills"),
        ("03", "Generate Career Twin"),
        ("04", "View Dashboard"),
    ]
    st.progress(current_step / len(steps))
    columns = st.columns(len(steps))
    for index, (column, (icon, step)) in enumerate(zip(columns, steps), start=1):
        with column:
            label = f"{icon} {step}"
            if index < current_step:
                st.success(label)
            elif index == current_step:
                st.info(label)
            else:
                st.caption(label)


def render_onboarding_intro(method: str) -> None:
    st.header("Career Twin AI")
    st.caption("An AI career intelligence workspace for resumes, GitHub portfolios, skill gaps, country insights, roadmaps, and PDF reports.")
    feature_chips = [
        "Resume Analysis",
        "GitHub Intelligence",
        "Career Match",
        "AI Mentor",
        "Country Intelligence",
        "Skill Gap Analysis",
        "PDF Reports",
    ]
    st.markdown(" ".join(f"`{chip}`" for chip in feature_chips))
    stat_cols = st.columns(4)
    stats = [
        ("3,500+", "Careers supported"),
        (str(len(SUPPORTED_COUNTRIES)), "Countries"),
        ("150", "Validation profiles"),
        ("20+", "Career domains"),
    ]
    for column, (value, label) in zip(stat_cols, stats):
        with column:
            render_metric(label, value)

    st.subheader("How would you like to create your Career Twin?")
    option_cols = st.columns(2)
    with option_cols[0]:
        with st.container(border=True):
            st.markdown("**Upload Resume**")
            st.caption("Recommended. Extract your profile from a PDF resume, then review and edit it before generating the dashboard.")
            if method == "Upload Resume":
                st.success("Recommended path selected")
    with option_cols[1]:
        with st.container(border=True):
            st.markdown("**Fill Manually**")
            st.caption("Enter your education, skills, projects, certifications, and experience yourself.")
            if method == "Fill Manually":
                st.success("Manual path selected")

    st.subheader("Feature Showcase")
    showcase = [
        ("Resume Analysis", "Extract profile fields, skills, projects, education, experience, and certifications."),
        ("GitHub Intelligence", "Analyze public repositories, languages, quality, portfolio strength, and career signals."),
        ("Career Match Engine", "Compare your profile with thousands of domain-aware career paths."),
        ("Skill Gap Analysis", "See matched, missing, and recommended next skills with clear reasons."),
        ("AI Mentor", "Ask personalized questions using your resume, roadmap, country, and GitHub context."),
        ("Country Intelligence", "Review demand, salary, visa difficulty, hiring companies, and market growth."),
        ("Salary Insights", "Understand entry, mid-level, senior, and future earning projections."),
        ("Career Roadmaps", "Follow monthly plans with weekly milestones."),
        ("Resume Match", "Compare your resume to a career or job description with explainable scoring."),
        ("Digital Career Twin", "Visualize current, 1-year, 3-year, 5-year, and 10-year outcomes."),
        ("PDF Reports", "Export a professional career dashboard report."),
        ("Feedback System", "Send bugs, requests, parsing issues, or career data corrections."),
    ]
    for start in range(0, len(showcase), 4):
        columns = st.columns(4)
        for column, (title, detail) in zip(columns, showcase[start : start + 4]):
            with column:
                with st.container(border=True):
                    st.markdown(f"**{title}**")
                    st.caption(detail)


def render_pills(items: list[str]) -> None:
    if not items:
        st.success("No gaps found")
        return

    columns = st.columns(2)
    for index, item in enumerate(items):
        with columns[index % 2]:
            st.write(f"- {item}")


def render_skill_grid(skills: list[str]) -> None:
    if not skills:
        st.info("No skills detected yet.")
        return

    columns = st.columns(4)
    for index, skill in enumerate(skills):
        with columns[index % 4]:
            with st.container(border=True):
                st.caption(skill)


def display_value(value: object) -> str:
    if value in {None, "", "Unknown", "None", "Null", 0}:
        return "Not Specified"
    return str(value)


def confident_value(resume: ResumeParseResult, field: str, value: object) -> str:
    if resume.field_confidence.get(field, 0.0) < 0.6 or value in {None, "", "Unknown", "None", "Null"}:
        return CONFIDENCE_LOW_MESSAGE
    return str(value)


def confidence_pct(resume: ResumeParseResult, field: str) -> str:
    return f"{round(resume.field_confidence.get(field, 0.0) * 100)}%"


def render_resume_debug_panels(resume: ResumeParseResult) -> None:
    with st.expander("Extracted Resume Text"):
        if resume.text:
            st.text_area(
                "Raw text extracted by PyMuPDF",
                value=resume.text,
                height=320,
                disabled=True,
            )
        else:
            st.error("No text could be extracted from this resume.")

    with st.expander("Detected Skills"):
        if resume.skills:
            render_skill_grid(resume.skills)
        else:
            st.warning("No skills were detected.")


def render_extracted_fields(resume: ResumeParseResult) -> None:
    st.markdown("**Exact fields extracted from resume**")
    personal_cols = st.columns(2)
    with personal_cols[0]:
        st.write(f"Name: {confident_value(resume, 'name', resume.name)} ({confidence_pct(resume, 'name')})")
        st.write(f"Email: {confident_value(resume, 'email', resume.email)} ({confidence_pct(resume, 'email')})")
        st.write(f"Phone: {confident_value(resume, 'phone', resume.phone)} ({confidence_pct(resume, 'phone')})")
        st.write(f"Location: {confident_value(resume, 'location', resume.location)} ({confidence_pct(resume, 'location')})")
        st.write(f"Age: {display_value(resume.age)}")
    with personal_cols[1]:
        st.write(f"LinkedIn: {confident_value(resume, 'linkedin', resume.linkedin)} ({confidence_pct(resume, 'linkedin')})")
        st.write(f"GitHub: {confident_value(resume, 'github', resume.github)} ({confidence_pct(resume, 'github')})")
        st.write(f"Portfolio: {confident_value(resume, 'portfolio', resume.portfolio)} ({confidence_pct(resume, 'portfolio')})")
        st.write(f"Degree: {confident_value(resume, 'degree', resume.degree)} ({confidence_pct(resume, 'degree')})")
        st.write(f"Branch: {confident_value(resume, 'branch', resume.branch)} ({confidence_pct(resume, 'branch')})")
        st.write(f"Detected Domain: {resume.detected_domain} ({round(resume.domain_confidence * 100)}%)")
        st.write(f"Current Designation: {confident_value(resume, 'current_designation', resume.current_designation)} ({confidence_pct(resume, 'current_designation')})")
    st.write(f"University: {confident_value(resume, 'university', resume.university)} ({confidence_pct(resume, 'university')})")
    st.write(f"Education Years: {display_value(resume.start_year)} - {display_value(resume.graduation_year)}")
    st.write(f"Current Year: {confident_value(resume, 'current_year', resume.current_year)} ({confidence_pct(resume, 'current_year')})")
    st.write(f"CGPA: {confident_value(resume, 'cgpa', resume.gpa)} ({confidence_pct(resume, 'cgpa')})")


def render_resume_insights(resume: ResumeParseResult, missing_skills: list[str]) -> None:
    st.subheader("Resume Insights")
    metric_cols = st.columns(5)
    with metric_cols[0]:
        render_metric("Resume Strength", f"{resume.strength_score}%", "Based on skills, projects, education, certifications, and experience.")
        st.progress(resume.strength_score / 100)
    with metric_cols[1]:
        render_metric("Resume Completeness", f"{resume.completeness_score}%", "How many major resume sections were detected.")
    with metric_cols[2]:
        render_metric("Industry Readiness", f"{resume.industry_readiness_score}%", "Role proof from skills, projects, and experience.")
    with metric_cols[3]:
        render_metric("ATS Readiness", f"{resume.ats_readiness_score}%", "Keyword and section readiness.")
    with metric_cols[4]:
        render_metric("Overall Career Readiness", f"{resume.overall_career_readiness_score}%", "Combined resume readiness.")

    insight_cols = st.columns([1.2, 1])
    with insight_cols[0]:
        st.markdown("**Extracted Skills By Category**")
        for category, skills in resume.skill_categories.items():
            with st.expander(category, expanded=bool(skills)):
                render_skill_grid(skills)
    with insight_cols[1]:
        st.markdown("**Missing Skills For Selected Career**")
        render_pills(missing_skills)

    detail_cols = st.columns(3)
    with detail_cols[0]:
        with st.expander("Education", expanded=True):
            if resume.education:
                for item in resume.education:
                    st.write(f"- {item}")
                st.caption(f"Degree: {display_value(resume.degree)}")
                st.caption(f"Branch: {display_value(resume.branch)}")
                st.caption(f"University: {display_value(resume.university)}")
                st.caption(f"Current Year: {display_value(resume.current_year)}")
            else:
                st.warning("We couldn't confidently extract this section. Please review it manually.")
    with detail_cols[1]:
        with st.expander("Certifications", expanded=True):
            if resume.structured_certifications:
                for cert in resume.structured_certifications:
                    with st.container(border=True):
                        st.markdown(f"**{display_value(cert.get('name'))}**")
                        if cert.get("provider") or cert.get("completion_year"):
                            st.caption(f"{display_value(cert.get('provider'))} | {display_value(cert.get('completion_year'))}")
            else:
                st.warning("We couldn't confidently extract this section. Please review it manually.")
    with detail_cols[2]:
        with st.expander("Projects and Experience", expanded=True):
            if resume.structured_projects:
                st.markdown("**Projects**")
                for project in resume.structured_projects:
                    with st.container(border=True):
                        st.markdown(f"**{display_value(project.get('name'))}**")
                        st.caption(f"Stack: {display_value(project.get('tech_stack'))}")
                        st.write(display_value(project.get("description")))
                        if project.get("role"):
                            st.caption(f"Role: {project['role']}")
                        if project.get("impact"):
                            st.success(f"Impact: {project['impact']}")
            else:
                st.warning("We couldn't confidently extract Projects. Please review it manually.")
            if resume.structured_experience:
                st.markdown("**Experience**")
                for experience in resume.structured_experience:
                    with st.container(border=True):
                        st.markdown(f"**{display_value(experience.get('role'))}**")
                        st.caption(f"{display_value(experience.get('company'))} | {display_value(experience.get('duration'))}")
                        st.write(display_value(experience.get("responsibilities")))
                        if experience.get("skills_used"):
                            st.caption(f"Skills Used: {experience['skills_used']}")
                        if experience.get("achievements"):
                            st.success(f"Achievement: {experience['achievements']}")
            else:
                st.warning("We couldn't confidently extract Experience. Please review it manually.")

    with st.expander("Resume improvement notes"):
        for insight in resume.insights:
            st.write(f"- {insight}")

    render_extracted_fields(resume)
    render_resume_debug_panels(resume)


def render_github_analysis(analysis: GitHubAnalysis) -> None:
    st.subheader("GitHub Profile Analysis")
    st.caption(f"Public portfolio analysis for `{analysis.username}`.")
    render_github_nav()

    section_anchor("github-overview")
    metric_cols = st.columns(4)
    with metric_cols[0]:
        render_metric("GitHub Score", f"{analysis.github_score}%", "Repository depth, stars, skills, activity, and project quality.")
        st.progress(analysis.github_score / 100)
    with metric_cols[1]:
        render_metric("Repository Count", str(analysis.repository_count), "Public repositories analyzed.")
    with metric_cols[2]:
        render_metric("Project Quality", f"{analysis.project_quality_score}%", "Average quality of the strongest repositories.")
        st.progress(analysis.project_quality_score / 100)
    with metric_cols[3]:
        render_metric("Portfolio Strength", analysis.portfolio_strength, f"Activity level: {analysis.activity_level}")

    breakdown = getattr(analysis, "score_breakdown", {}) or {}
    if breakdown:
        st.markdown("**Recruiter-Grade Score Breakdown**")
        breakdown_items = list(breakdown.values())
        for start in range(0, len(breakdown_items), 4):
            columns = st.columns(min(4, len(breakdown_items[start : start + 4])))
            for column, item in zip(columns, breakdown_items[start : start + 4]):
                with column:
                    score = int(item.get("score", 0))
                    render_metric(
                        str(item.get("label", "Score")),
                        f"{score}%",
                        f"Weight {item.get('weight', 0)}%",
                    )
                    st.progress(score / 100)
                    st.caption(str(item.get("reason", "")))

    section_anchor("github-stats")
    stats_cols = st.columns(4)
    with stats_cols[0]:
        render_metric("Followers", str(analysis.followers), f"Following {analysis.following}")
    with stats_cols[1]:
        render_metric("Total Stars", f"{analysis.total_stars:,}", f"Forks {analysis.total_forks:,}")
    with stats_cols[2]:
        render_metric("Years Active", str(analysis.years_active), f"Public gists {analysis.public_gists}")
    with stats_cols[3]:
        render_metric("Open Source Impact", analysis.open_source_contribution_level, f"Top repo: {analysis.most_starred_repository}")

    section_anchor("github-languages")
    chart_cols = st.columns([1, 1])
    with chart_cols[0]:
        st.markdown("**Languages Used**")
        if analysis.language_counts:
            language_data = pd.DataFrame(
                [{"Language": language, "Repositories": count} for language, count in analysis.language_counts.items()]
            )
            chart = (
                alt.Chart(language_data)
                .mark_arc(innerRadius=55)
                .encode(
                    theta=alt.Theta("Repositories:Q"),
                    color=alt.Color("Language:N"),
                    tooltip=["Language", "Repositories"],
                )
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("No repository languages detected.")
    with chart_cols[1]:
        st.markdown("**Project Categories**")
        render_count_chart(analysis.category_counts, "Category", "Repositories")

    extra_chart_cols = st.columns([1, 1])
    with extra_chart_cols[0]:
        st.markdown("**Repository Quality Distribution**")
        render_count_chart(analysis.quality_distribution, "Quality", "Repositories")
    with extra_chart_cols[1]:
        st.markdown("**Technology Stack Distribution**")
        render_count_chart(analysis.technology_stack_counts, "Technology", "Repositories")

    section_anchor("github-skills")
    skill_cols = st.columns([1, 1])
    with skill_cols[0]:
        st.markdown("**Top Skills**")
        render_skill_grid(analysis.top_skills)
    with skill_cols[1]:
        st.markdown("**Portfolio Insights**")
        render_pills([
            f"Most used language: {analysis.most_used_language}",
            f"Average repository quality: {analysis.project_quality_score}%",
            f"Most starred repository: {analysis.most_starred_repository}",
            f"Activity level: {analysis.activity_level}",
        ])

    project_cols = st.columns(2)
    with project_cols[0]:
        render_metric("AI/ML Projects", str(len(analysis.ai_ml_projects)), "Detected from repository names, topics, and descriptions.")
    with project_cols[1]:
        render_metric("Web Projects", str(len(analysis.web_projects)), "Detected from repository names, topics, and descriptions.")

    section_anchor("github-repos")
    st.markdown("**Project Summary Cards**")
    render_project_summary_cards(analysis.repos)

    section_anchor("github-careers")
    st.markdown("**Career Recommendations From GitHub**")
    career_cols = st.columns(min(4, max(1, len(analysis.suitable_careers))))
    for column, career in zip(career_cols, analysis.suitable_careers):
        with column:
            with st.container(border=True):
                st.markdown(f"**{career['career']}**")
                st.caption(career["why"])

    section_anchor("github-strengths")
    sw_cols = st.columns(2)
    with sw_cols[0]:
        st.markdown("**Strengths**")
        for strength in analysis.strengths:
            st.write(f"- {strength}")
    with sw_cols[1]:
        st.markdown("**Weaknesses**")
        for weakness in analysis.weaknesses:
            st.write(f"- {weakness}")

    section_anchor("github-suggestions")
    with st.expander("Improvement Suggestions", expanded=True):
        for recommendation in analysis.recommendations:
            st.write(f"- {recommendation}")


def render_github_nav() -> None:
    sections = [
        ("github-overview", "Overview"),
        ("github-stats", "GitHub Statistics"),
        ("github-languages", "Languages"),
        ("github-skills", "Skills"),
        ("github-skills", "Portfolio Insights"),
        ("github-repos", "Repository Analysis"),
        ("github-languages", "Project Categories"),
        ("github-careers", "Career Recommendations"),
        ("github-strengths", "Strengths & Weaknesses"),
        ("github-suggestions", "Improvement Suggestions"),
    ]
    links = "".join(f'<a href="#{section_id}">{label}</a>' for section_id, label in sections)
    st.markdown(f'<nav class="dashboard-section-nav" aria-label="GitHub analysis sections">{links}</nav>', unsafe_allow_html=True)


def render_count_chart(counts: dict[str, int], label: str, value: str) -> None:
    if not counts:
        st.info("No data available yet.")
        return
    data = pd.DataFrame([{label: key, value: val} for key, val in counts.items()])
    st.altair_chart(
        alt.Chart(data)
        .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
        .encode(
            x=alt.X(f"{label}:N", sort="-y", axis=alt.Axis(labelAngle=-30)),
            y=alt.Y(f"{value}:Q"),
            tooltip=[label, value],
            color=alt.Color(f"{label}:N", legend=None),
        )
        .properties(height=260),
        use_container_width=True,
    )


def render_github_cta() -> None:
    st.subheader("GitHub Profile Analysis")
    with st.container(border=True):
        st.markdown("**Connect GitHub to unlock portfolio intelligence**")
        st.caption("Analyze real public repositories, language distribution, project categories, repository quality, career signals, and portfolio recommendations.")
        cols = st.columns(3)
        with cols[0]:
            st.metric("Unlocked", "Repo quality")
        with cols[1]:
            st.metric("Unlocked", "Tech stack")
        with cols[2]:
            st.metric("Unlocked", "Portfolio score")
        st.info("Enter a GitHub username in the sidebar and click Analyze GitHub. This also works without uploading a resume.")
        if st.session_state.get("github_error"):
            st.warning(st.session_state.github_error)


def selected_profession_specializations(career_name: str, career_knowledge: dict[str, object]) -> list[str]:
    name = career_name.casefold()
    domain = str(career_knowledge.get("domain", "")).casefold()
    if "civil" in name:
        return ["Structural Engineer", "Construction Engineer", "Site Engineer", "Highway Engineer", "Water Resources Engineer"]
    if "ai" in name or "machine learning" in name:
        return ["Machine Learning Engineer", "Computer Vision Engineer", "NLP Engineer", "MLOps Engineer", "Applied AI Engineer"]
    if "data" in name:
        return ["Data Analyst", "Data Scientist", "BI Analyst", "Analytics Engineer", "Machine Learning Analyst"]
    if "software" in name or "developer" in name or domain == "technology":
        return ["Backend Developer", "Frontend Developer", "Full-Stack Developer", "Platform Engineer", "Mobile Developer"]
    if "finance" in name or "audit" in name or "account" in name:
        return ["Audit Manager", "Finance Controller", "Tax Consultant", "Financial Analyst", "Risk Analyst"]
    if "marketing" in name:
        return ["SEO Specialist", "Performance Marketer", "Brand Strategist", "Content Marketer", "Growth Marketer"]
    if "law" in name or "legal" in name:
        return ["Corporate Lawyer", "Compliance Counsel", "Contract Specialist", "Legal Researcher", "Litigation Associate"]
    if "doctor" in name or "medical" in name or "nurse" in name or "pharmac" in name or domain == "healthcare":
        return ["Clinical Specialist", "Hospital Operations Specialist", "Public Health Specialist", "Clinical Research Associate", "Quality & Compliance Specialist"]
    if "pilot" in name or "aviation" in name:
        return ["Commercial Pilot", "Flight Instructor", "Airline First Officer", "Aviation Safety Officer", "Flight Operations Specialist"]
    if "hotel" in name or "hospitality" in name:
        return ["Hotel Operations Manager", "Guest Relations Manager", "Revenue Manager", "Event Operations Manager", "Food & Beverage Manager"]
    if "journal" in name or "media" in name:
        return ["Reporter", "Editor", "Digital Journalist", "Investigative Journalist", "Content Producer"]
    if "design" in name or domain in {"creative", "architecture"}:
        return ["Visual Designer", "UX Designer", "Product Designer", "Interior Designer", "Creative Lead"]
    if "teacher" in name or "professor" in name or domain == "education":
        return ["Subject Teacher", "Curriculum Designer", "Academic Coordinator", "Instructional Designer", "Education Consultant"]
    return list(career_knowledge.get("career_path", []))[:5] or [career_name]


def render_selected_career_overview(
    profile: UserProfile,
    readiness: dict[str, object],
    probability: int,
    country_intelligence: CountryCareerIntelligence,
    career_knowledge: dict[str, object],
    resume_match: ResumeMatchAnalysis | None,
    coach_scores: dict[str, dict[str, object]],
    roadmap_items: list[dict[str, object]],
) -> None:
    st.subheader("Selected Career Overview")
    st.caption("Focused coaching for the career you selected, with nearby specializations only.")
    match_score = int(getattr(resume_match, "overall_match", readiness["score"]) or readiness["score"])
    roadmap_progress = calibrated_ratio_score(
        "roadmap_progress",
        len(readiness.get("matched_skills", [])),
        max(1, len(readiness.get("required_skills", []))),
    )
    overview_cols = st.columns(4)
    with overview_cols[0]:
        render_metric("Career Match Score", f"{match_score}%", "Fit for the selected career.")
    with overview_cols[1]:
        render_metric("Career Readiness", f"{readiness['score']}%", str(readiness.get("label", "")))
    with overview_cols[2]:
        render_metric("Market Readiness", f"{coach_scores['market_readiness']['score']}%", str(coach_scores["market_readiness"].get("label", "")))
    with overview_cols[3]:
        render_metric("Skill Coverage", f"{readiness.get('skill_coverage', 0)}%", "Matched role requirements.")

    detail_cols = st.columns(3)
    with detail_cols[0]:
        st.markdown("**Required Skills**")
        render_pills([str(item) for item in readiness.get("required_skills", [])[:8]])
    with detail_cols[1]:
        st.markdown("**Missing Skills**")
        render_pills([str(item) for item in readiness.get("missing_skills", [])[:8]])
    with detail_cols[2]:
        st.markdown("**Selected-Profession Specializations**")
        render_pills(selected_profession_specializations(profile.career_goal, career_knowledge))

    market_cols = st.columns(4)
    with market_cols[0]:
        render_metric("Salary Information", country_intelligence.average_salary, f"Entry: {country_intelligence.entry_salary}")
    with market_cols[1]:
        render_metric("Job Demand", country_intelligence.demand_level, country_intelligence.hiring_trend)
    with market_cols[2]:
        render_metric("Growth Outlook", country_intelligence.market_growth, country_intelligence.future_outlook[:120])
    with market_cols[3]:
        render_metric("Roadmap Progress", f"{roadmap_progress}%", f"Next: {roadmap_items[0]['focus'] if roadmap_items else 'Build proof'}")

    with st.container(border=True):
        st.markdown("**AI Mentor Advice**")
        advice = [
            f"Stay focused on {profile.career_goal}; the dashboard is now evaluating this selected path rather than guessing unrelated careers.",
            "Prioritize missing mandatory and domain skills before adding broad soft skills.",
            f"Use the next roadmap milestone to create proof around {roadmap_items[0]['focus'] if roadmap_items else 'your highest-priority skill'}.",
        ]
        for item in advice:
            st.write(f"- {item}")


def render_project_summary_cards(repos: list[object]) -> None:
    if not repos:
        st.caption("No matching public repositories found.")
        return

    for repo in repos:
        with st.container(border=True):
            header_cols = st.columns([2, 1])
            with header_cols[0]:
                st.markdown(f"**{repo.name}**")
                st.caption(repo.description)
            with header_cols[1]:
                st.metric("Quality", f"{repo.quality_score}%")
            detail_cols = st.columns(4)
            with detail_cols[0]:
                st.metric("Stars", repo.stars)
            with detail_cols[1]:
                st.metric("Forks", getattr(repo, "forks", 0))
            with detail_cols[2]:
                st.metric("Language", repo.language)
            with detail_cols[3]:
                st.metric("Difficulty", getattr(repo, "difficulty_level", "Beginner"))
            meta_cols = st.columns(3)
            with meta_cols[0]:
                st.caption(f"Category: {repo.project_type}")
            with meta_cols[1]:
                st.caption(f"Updated: {format_github_date(repo.updated_at)}")
            with meta_cols[2]:
                st.caption(f"Size: {getattr(repo, 'size_kb', 0):,} KB")
            if getattr(repo, "topics", []):
                render_pills(repo.topics[:8])
            breakdown = getattr(repo, "quality_breakdown", {}) or {}
            if breakdown:
                with st.expander("Quality score breakdown"):
                    for item in breakdown.values():
                        st.write(
                            f"- {item.get('label', 'Signal')}: "
                            f"{item.get('score', 0)}/{item.get('max', 0)}"
                        )
                        st.caption(str(item.get("reason", "")))
            if repo.url:
                st.link_button("Open repository", repo.url)


def format_github_date(value: str) -> str:
    if not value:
        return "Unknown"
    return value[:10]


def career_match_reason(match: dict[str, object]) -> str:
    matched = match.get("matched_skills", [])
    missing = match.get("missing_skills", [])
    reasons = []
    if matched:
        reasons.append(f"matches {len(matched)} required skill(s): {', '.join(matched[:3])}")
    if missing:
        reasons.append(f"still needs {', '.join(missing[:3])}")
    if not reasons:
        reasons.append("uses project, experience, certification, and study-hour signals")
    return "; ".join(reasons) + "."


def probability_factors(profile: UserProfile, readiness: dict[str, object]) -> tuple[list[str], list[str]]:
    positives = []
    gaps = []
    if readiness["matched_skills"]:
        positives.append(f"{len(readiness['matched_skills'])} matched skill(s)")
    if profile.project_count:
        positives.append(f"{profile.project_count} project signal(s)")
    else:
        gaps.append("add at least one role-specific project")
    if profile.internship_count:
        positives.append("experience or internship signal")
    else:
        gaps.append("add internship, freelance, lab, or volunteer experience")
    if profile.certification_count:
        positives.append("certification proof")
    if profile.weekly_study_hours >= 8:
        positives.append(f"{profile.weekly_study_hours} weekly study hours")
    elif profile.weekly_study_hours < 5:
        gaps.append("increase weekly study consistency")
    if readiness["missing_skills"]:
        gaps.append("close missing skills: " + ", ".join(readiness["missing_skills"][:4]))
    return positives or ["profile created successfully"], gaps or ["no major scoring blockers detected"]


def future_success_milestones(probability: int) -> list[tuple[str, int, str]]:
    return [
        ("Current", probability, "Based on current evidence and consistency."),
        ("3 months", min(probability + 4, 90), "Complete the first roadmap project and close two priority gaps."),
        ("6 months", min(probability + 8, 91), "Add portfolio proof, targeted applications, and interview practice."),
        ("1 year", min(probability + 13, 92), "Combine experience, certifications, and a stronger body of work."),
    ]


def calculate_ai_confidence(
    profile: UserProfile,
    resume: ResumeParseResult | None,
    github_relevant: bool,
    github_analysis: GitHubAnalysis | None,
) -> dict[str, object]:
    score = 42
    positives = []
    improvements = []
    if profile.career_goal:
        score += 7
        positives.append("career goal is clearly selected")
    if profile.skills:
        score += min(len(profile.skills), 10) * 1.4
        positives.append("skill evidence is available")
    if resume:
        if resume.extraction_status == "Success":
            score += 11
            positives.append("resume extraction completed successfully")
        elif resume.extraction_status == "Partial":
            score += 5
            improvements.append("some resume fields need manual review")
        else:
            improvements.append("resume extraction failed")
        if resume.current_designation:
            score += 4
            positives.append("current designation was detected")
        if resume.detected_domain:
            score += 3
            positives.append(f"domain signal detected: {resume.detected_domain}")
    else:
        improvements.append("uploading a resume would improve AI confidence")
    if github_relevant:
        if github_analysis:
            score += 4
            positives.append("GitHub evidence is included for this technical path")
        else:
            improvements.append("GitHub is relevant for this path but not connected")
    if resume and resume.extraction_status == "Success" and profile.skills and profile.project_count >= 2 and profile.internship_count:
        cap = 93
    elif resume or profile.skills:
        cap = 86
    else:
        cap = 72
    final_score = max(45, min(round(score), cap))
    return {
        "score": final_score,
        "label": score_label(final_score),
        "positives": positives or ["enough profile context exists to begin"],
        "improvements": improvements or ["no major confidence gaps detected"],
        "why": "AI confidence measures data quality, profile completeness, career clarity, extraction quality, and relevant portfolio availability.",
    }


def calculate_portfolio_strength(
    profile: UserProfile,
    resume: ResumeParseResult | None,
    github_analysis: GitHubAnalysis | None,
    career_knowledge: dict[str, object],
) -> dict[str, object]:
    domain = str(career_knowledge.get("domain", "")).casefold()
    score = 30
    positives = []
    improvements = []
    requirements = career_knowledge.get("portfolio_requirements", []) or []
    if profile.project_count:
        score += min(profile.project_count, 4) * 9
        positives.append(f"{profile.project_count} project/case-study item(s) are present")
    else:
        improvements.append("add profession-specific portfolio proof")
    if profile.achievements:
        score += min(len(profile.achievements), 3) * 5
        positives.append("achievement evidence strengthens credibility")
    if profile.internship_count:
        score += min(profile.internship_count, 3) * 5
        positives.append("experience supports portfolio strength")
    tech_domain = any(term in domain for term in ["software", "engineering", "data", "cybersecurity", "cloud", "technology", "ai"])
    if tech_domain:
        if github_analysis:
            score += calibrated_score("github", int(github_analysis.github_score)) * 0.18
            positives.append("GitHub repositories are evaluated for this technical path")
        else:
            improvements.append("add GitHub or production project links for stronger technical proof")
    elif resume and (resume.portfolio or resume.linkedin):
        score += 8
        positives.append("professional profile or portfolio link is available")
    if requirements:
        improvements.append("best portfolio evidence: " + ", ".join(str(item) for item in requirements[:3]))
    cap = 92 if profile.project_count >= 4 and profile.internship_count >= 2 else 86
    final_score = max(30, min(round(score), cap))
    return {
        "score": final_score,
        "label": score_label(final_score),
        "positives": positives or ["portfolio can be built from current profile evidence"],
        "improvements": improvements or ["keep adding measurable examples of work"],
        "why": "Portfolio strength is profession-aware. Technical roles consider GitHub when relevant; non-technical roles focus on case studies, writing, clinical, legal, design, business, or operational proof.",
    }


def calculate_market_readiness(
    profile: UserProfile,
    readiness: dict[str, object],
    country_intelligence: CountryCareerIntelligence,
    portfolio_strength: dict[str, object],
) -> dict[str, object]:
    demand = str(country_intelligence.demand_level).casefold()
    score = 30
    positives = []
    improvements = []
    if "very high" in demand:
        score += 12
        positives.append("market demand is very high")
    elif "high" in demand:
        score += 9
        positives.append("market demand is high")
    elif "medium" in demand:
        score += 5
        positives.append("market demand is moderate")
    score += calibrated_score("technical_skills", int(readiness.get("skill_coverage", 0))) * 0.20
    score += calibrated_score("portfolio_strength", int(portfolio_strength["score"])) * 0.15
    if profile.internship_count:
        score += 6
        positives.append("experience improves job-market signal")
    else:
        improvements.append("add internship, field work, freelance, or practical experience")
    if profile.certification_count:
        score += 3
        positives.append("certifications support market credibility")
    if readiness.get("missing_skills"):
        improvements.append("close market-critical skills: " + ", ".join(str(item) for item in readiness["missing_skills"][:3]))
    final_score = max(32, min(round(score), 90))
    return {
        "score": final_score,
        "label": score_label(final_score),
        "positives": positives or ["selected market has an identifiable path"],
        "improvements": improvements or ["continue building proof and interview readiness"],
        "why": "Market readiness estimates competitiveness using demand, skill coverage, portfolio evidence, experience, certifications, and country-specific expectations.",
    }


def render_professional_scorecard(title: str, data: dict[str, object]) -> None:
    score = int(data["score"])
    with st.container(border=True):
        st.metric(title, f"{score}%")
        st.caption(f"{data.get('label', score_label(score))}")
        st.progress(score / 100)
        st.markdown("**Why this score exists**")
        st.caption(str(data.get("why", "")))
        cols = st.columns(2)
        with cols[0]:
            st.markdown("**Improved by**")
            render_pills([str(item) for item in data.get("positives", [])][:4])
        with cols[1]:
            st.markdown("**Improve next**")
            render_pills([str(item) for item in data.get("improvements", [])][:4])


def render_career_coach_scores(
    profile: UserProfile,
    readiness: dict[str, object],
    probability: int,
    resume: ResumeParseResult | None,
    github_relevant: bool,
    github_analysis: GitHubAnalysis | None,
    country_intelligence: CountryCareerIntelligence,
    career_knowledge: dict[str, object],
) -> dict[str, dict[str, object]]:
    ai_confidence = calculate_ai_confidence(profile, resume, github_relevant, github_analysis)
    portfolio_strength = calculate_portfolio_strength(profile, resume, github_analysis if github_relevant else None, career_knowledge)
    market_readiness = calculate_market_readiness(profile, readiness, country_intelligence, portfolio_strength)
    success_data = {
        "score": probability,
        "label": score_label(probability),
        "positives": probability_factors(profile, readiness)[0],
        "improvements": probability_factors(profile, readiness)[1],
        "why": "Success probability estimates future momentum from profile evidence, study consistency, experience, portfolio proof, and realistic roadmap progress. It is not copied from readiness.",
    }
    readiness_data = {
        "score": readiness["score"],
        "label": readiness.get("label", score_label(int(readiness["score"]))),
        "positives": readiness.get("positive_factors", []),
        "improvements": readiness.get("improvement_factors", []),
        "why": readiness.get("why", ""),
    }
    skill_data = {
        "score": readiness.get("skill_coverage", 0),
        "label": score_label(int(readiness.get("skill_coverage", 0))),
        "positives": [f"Matched: {', '.join(readiness['matched_skills'][:5])}"] if readiness["matched_skills"] else ["skills are ready to be built"],
        "improvements": [f"Next skills: {', '.join(readiness['missing_skills'][:5])}"] if readiness["missing_skills"] else ["maintain and deepen current skills"],
        "why": "Skill coverage compares current skills with the selected career's required skills and recommends the next highest-impact skills.",
    }
    st.subheader("Professional Career Coach Scores")
    score_cards = [
        ("Career Readiness", readiness_data),
        ("Success Probability", success_data),
        ("AI Confidence", ai_confidence),
        ("Skill Coverage", skill_data),
        ("Portfolio Strength", portfolio_strength),
        ("Market Readiness", market_readiness),
    ]
    for start in range(0, len(score_cards), 3):
        columns = st.columns(3)
        for column, (title, data) in zip(columns, score_cards[start : start + 3]):
            with column:
                render_professional_scorecard(title, data)
    st.markdown("**Success Milestones**")
    milestone_cols = st.columns(4)
    for column, (label, value, detail) in zip(milestone_cols, future_success_milestones(probability)):
        with column:
            with st.container(border=True):
                st.metric(label, f"{value}%")
                st.caption(score_label(value))
                st.caption(detail)
    return {
        "ai_confidence": ai_confidence,
        "portfolio_strength": portfolio_strength,
        "market_readiness": market_readiness,
        "skill_coverage": skill_data,
    }


def render_resume_match_score(
    analysis: ResumeMatchAnalysis,
    resume: ResumeParseResult,
    careers: dict[str, dict],
) -> None:
    st.subheader("Resume Match Score")
    st.caption("Complete resume-to-career match intelligence for the selected target role.")

    render_circular_score("Overall Resume Match", analysis.overall_match, "Weighted fit across resume, ATS, GitHub, and role evidence.")

    score_items = list(analysis.weighted_scores.items())
    for start in range(0, len(score_items), 5):
        columns = st.columns(5)
        for column, (label, score) in zip(columns, score_items[start : start + 5]):
            with column:
                if isinstance(score, int):
                    render_circular_score(label, score)
                else:
                    render_metric(label, str(score), "Not applicable for this career/profile.")

    summary_cols = st.columns(2)
    with summary_cols[0]:
        with st.expander("Strengths", expanded=True):
            for item in analysis.strengths:
                st.success(item)
        with st.expander("Critical Missing Skills", expanded=True):
            render_pills(analysis.critical_missing_skills)
        with st.expander("Important Skills"):
            render_pills(analysis.important_skills)
    with summary_cols[1]:
        with st.expander("Weaknesses", expanded=True):
            if analysis.weaknesses:
                for item in analysis.weaknesses:
                    st.warning(item)
            else:
                st.success("No major weaknesses detected for the selected career.")
        with st.expander("Nice-to-have Skills"):
            render_pills(analysis.nice_to_have_skills)
        with st.expander("Resume Improvement Suggestions", expanded=True):
            for suggestion in analysis.improvement_suggestions:
                with st.container(border=True):
                    st.markdown(f"**{suggestion['suggestion']}**")
                    st.caption(f"Why: {suggestion['why']}")

    st.markdown("**Resume vs Job Description**")
    jd_cols = st.columns([1, 1])
    with jd_cols[0]:
        jd_file = st.file_uploader("Upload PDF or DOCX Job Description", type=["pdf", "docx"], key="job_description_file")
    with jd_cols[1]:
        jd_text = st.text_area("Or paste Text Job Description", height=160, key="job_description_text")

    jd_source_text = ""
    if jd_file:
        try:
            jd_source_text = extract_resume_text(jd_file)
        except RuntimeError as exc:
            st.error(str(exc))
    elif jd_text.strip():
        jd_source_text = jd_text.strip()

    if jd_source_text:
        jd_match = compare_resume_to_job_description(resume, jd_source_text, careers)
        render_job_description_match(jd_match)


def render_job_description_match(match: JobDescriptionMatch) -> None:
    metric_cols = st.columns(4)
    with metric_cols[0]:
        render_circular_score("Keyword Match", match.keyword_match)
    with metric_cols[1]:
        render_circular_score("Semantic Match", match.semantic_match)
    with metric_cols[2]:
        render_circular_score("Technical Match", match.technical_match)
    with metric_cols[3]:
        render_metric("Hiring Recommendation", match.hiring_recommendation)

    detail_cols = st.columns(3)
    with detail_cols[0]:
        render_metric("Experience Match", f"{match.experience_match}%")
    with detail_cols[1]:
        render_metric("Education Match", f"{match.education_match}%")
    with detail_cols[2]:
        render_metric("Certification Match", f"{match.certification_match}%")

    keyword_cols = st.columns(2)
    with keyword_cols[0]:
        st.markdown("**Matched Keywords**")
        render_pills(match.matched_keywords)
    with keyword_cols[1]:
        st.markdown("**Missing Keywords**")
        render_pills(match.missing_keywords)

    if match.highlighted_missing_keywords:
        st.warning("Missing keywords to add or prove: " + ", ".join(match.highlighted_missing_keywords))


def render_country_intelligence(intelligence: CountryCareerIntelligence) -> None:
    st.subheader("Country Career Intelligence")
    st.caption(f"{intelligence.flag} {intelligence.career} in {intelligence.country}")

    top_cols = st.columns(5)
    with top_cols[0]:
        render_metric("Currency", intelligence.currency, "Local salary currency.")
    with top_cols[1]:
        render_metric("Average Salary", intelligence.average_salary, "Directional mid-market estimate.")
    with top_cols[2]:
        render_metric("Demand", intelligence.demand_level, "Hiring appetite for this role.")
    with top_cols[3]:
        render_metric("Hiring Trend", intelligence.hiring_trend, "Current market direction.")
    with top_cols[4]:
        render_metric("Industry Growth", intelligence.market_growth, "Expected sector momentum.")

    context_cols = st.columns(4)
    with context_cols[0]:
        render_metric("Remote Work", intelligence.remote_work_availability, "Remote and hybrid opportunity level.")
    with context_cols[1]:
        render_metric("Visa / Permit", intelligence.visa_difficulty, intelligence.visa_overview)
    with context_cols[2]:
        render_metric("Cost of Living", intelligence.cost_of_living, "Planning context for relocation.")
    with context_cols[3]:
        render_metric("Interview Style", intelligence.interview_style, "Typical first-stage evaluation pattern.")

    salary_cols = st.columns(3)
    with salary_cols[0]:
        render_metric("Entry Salary", intelligence.entry_salary)
    with salary_cols[1]:
        render_metric("Mid-Level Salary", intelligence.mid_level_salary)
    with salary_cols[2]:
        render_metric("Senior Salary", intelligence.senior_salary)

    outlook_cols = st.columns(2)
    with outlook_cols[0]:
        with st.container(border=True):
            st.markdown("**Career Outlook**")
            st.caption(intelligence.future_outlook)
    with outlook_cols[1]:
        with st.container(border=True):
            st.markdown("**Top Hiring Industries**")
            render_pills(intelligence.major_hiring_industries)

    detail_cols = st.columns([1, 1, 1])
    with detail_cols[0]:
        st.markdown("**Most Required Skills**")
        render_skill_grid(intelligence.most_required_skills)
    with detail_cols[1]:
        st.markdown("**Top Hiring Companies**")
        render_pills(intelligence.top_hiring_companies)
    with detail_cols[2]:
        st.markdown("**Interview Process**")
        for step in intelligence.interview_process:
            st.write(f"- {step}")

    value_cols = st.columns(3)
    with value_cols[0]:
        st.markdown("**Most Valuable Certifications**")
        render_pills(intelligence.most_valuable_certifications)
    with value_cols[1]:
        if intelligence.most_valuable_programming_languages:
            st.markdown("**Most Valuable Programming Languages**")
            render_pills(intelligence.most_valuable_programming_languages)
        else:
            st.markdown("**Role-Specific Market Skills**")
            render_pills(intelligence.most_required_skills[:5])
    with value_cols[2]:
        if intelligence.most_valuable_frameworks:
            st.markdown("**Most Valuable Frameworks**")
            render_pills(intelligence.most_valuable_frameworks)
        else:
            st.markdown("**Professional Focus Areas**")
            render_pills(intelligence.interview_process[:4])

    with st.expander("Language Requirements"):
        render_pills(intelligence.language_requirements)

    with st.expander("Degree Requirements"):
        render_pills(intelligence.degree_requirements)

    with st.expander("Career Progression"):
        render_pills(intelligence.career_progression)

    with st.expander("Market Insights", expanded=True):
        st.markdown("**Market Insights**")
        for insight in intelligence.insights:
            st.write(f"- {insight}")
        st.caption("Salary and visa indicators are directional planning estimates, not legal or compensation advice.")

    st.markdown("**Quick Country Comparison**")
    comparison_countries = [
        country for country in ["India", "Germany", "USA", "Canada", "Australia", "United Kingdom", "Singapore", "UAE"]
        if country in SUPPORTED_COUNTRIES and country != intelligence.country
    ][:5]
    comparison_rows = []
    for country in comparison_countries:
        comparison = get_country_career_intelligence(intelligence.career, country, {"domain": "", "required_skills": intelligence.most_required_skills})
        comparison_rows.append(
            {
                "Country": f"{comparison.flag} {comparison.country}",
                "Demand": comparison.demand_level,
                "Average Salary": comparison.average_salary,
                "Remote": comparison.remote_work_availability,
                "Visa": comparison.visa_difficulty,
            }
        )
    if comparison_rows:
        st.dataframe(pd.DataFrame(comparison_rows), use_container_width=True, hide_index=True)


def render_universal_career_intelligence(
    profile: UserProfile,
    resume: ResumeParseResult | None,
    career_knowledge: dict[str, object],
    missing_skills: list[str],
) -> None:
    st.subheader("Universal Career Intelligence")
    detected_domain = getattr(resume, "detected_domain", "") if resume else ""
    domain_confidence = getattr(resume, "domain_confidence", 0.0) if resume else 0.0
    domain = detected_domain or str(career_knowledge.get("domain", "General"))

    intro_cols = st.columns(4)
    with intro_cols[0]:
        render_metric("Profession Domain", domain, f"{round(domain_confidence * 100)}% confidence" if resume else "Based on selected career.")
    with intro_cols[1]:
        render_metric("AI Impact", str(career_knowledge.get("future_growth", "Medium")), str(career_knowledge.get("ai_impact", ""))[:110])
    with intro_cols[2]:
        render_metric("Remote", str(career_knowledge.get("remote_opportunities", "Medium")), "Remote opportunity level.")
    with intro_cols[3]:
        render_metric("Freelance / Startup", f"{career_knowledge.get('freelance_opportunities', 'Medium')} / {career_knowledge.get('startup_opportunities', 'Medium')}")

    info_cols = st.columns(3)
    with info_cols[0]:
        st.markdown("**Degree Requirements**")
        render_pills(list(career_knowledge.get("degree_requirements", [])))
    with info_cols[1]:
        st.markdown("**Portfolio Requirements**")
        render_pills(list(career_knowledge.get("portfolio_requirements", [])))
    with info_cols[2]:
        st.markdown("**Most Demanded Cities**")
        render_pills(list(career_knowledge.get("most_demanded_cities", [])))

    profile_cols = st.columns(4)
    with profile_cols[0]:
        st.markdown("**Profession Skills**")
        render_pills(list(career_knowledge.get("required_skills", []))[:6])
    with profile_cols[1]:
        st.markdown("**Tools / Software**")
        tools = list(career_knowledge.get("tools", [])) + list(career_knowledge.get("software", []))
        render_pills(tools[:6])
    with profile_cols[2]:
        st.markdown("**Top Employers**")
        render_pills(list(career_knowledge.get("top_hiring_companies", career_knowledge.get("hiring_companies", [])))[:6])
    with profile_cols[3]:
        st.markdown("**Career Path**")
        render_pills(list(career_knowledge.get("career_path", []))[:5])

    cert_cols = st.columns(2)
    with cert_cols[0]:
        st.markdown("**Certifications**")
        render_pills(list(career_knowledge.get("certifications", career_knowledge.get("preferred_certifications", [])))[:6])
    with cert_cols[1]:
        st.markdown("**Interview Pattern**")
        render_pills(list(career_knowledge.get("interview_pattern", []))[:6])

    with st.expander("Role Intelligence", expanded=False):
        role_cols = st.columns(3)
        role_sections = [
            ("Daily Responsibilities", list(career_knowledge.get("daily_responsibilities", []))),
            ("KPIs", list(career_knowledge.get("kpis", []))),
            ("ATS Keywords", list(career_knowledge.get("ats_keywords", []))),
            ("Resume Keywords", list(career_knowledge.get("resume_keywords", []))),
            ("Licensing Requirements", list(career_knowledge.get("licensing_requirements", []))),
            ("Transition Paths", list(career_knowledge.get("transition_paths", []))),
        ]
        for index, (label, values) in enumerate(role_sections):
            with role_cols[index % 3]:
                st.markdown(f"**{label}**")
                render_pills(values[:6])
        if career_knowledge.get("work_environment"):
            st.markdown("**Work Environment**")
            st.caption(str(career_knowledge.get("work_environment")))
        if career_knowledge.get("industry_insights"):
            st.markdown("**Industry Insights**")
            for insight in list(career_knowledge.get("industry_insights", []))[:3]:
                st.write(f"- {insight}")

    with st.expander("Selected Career Focus", expanded=True):
        st.caption("Career Twin AI now stays focused on your selected career path and its direct specializations.")
        focus_cols = st.columns(2)
        with focus_cols[0]:
            st.markdown("**Selected Profession Specializations**")
            render_pills(selected_profession_specializations(profile.career_goal, career_knowledge))
        with focus_cols[1]:
            st.markdown("**Why This Path Is Being Evaluated**")
            focus_reasons = [
                f"Selected target: {profile.career_goal}",
                f"Detected domain: {domain}",
                "Recommendations are limited to specializations within this profession.",
            ]
            render_pills(focus_reasons)

    transition_background = st.text_input(
        "Career transition background",
        value=st.session_state.get("transition_background", profile.branch or profile.degree or domain),
        placeholder="Example: BCom, Mechanical Engineer, BA Psychology",
    )
    st.session_state.transition_background = transition_background
    transition = build_transition_plan(transition_background, profile.career_goal, profile)
    with st.expander("Career Transition Engine", expanded=True):
        transition_cols = st.columns(4)
        with transition_cols[0]:
            render_metric("Difficulty", transition["difficulty"], transition["why"])
        with transition_cols[1]:
            render_metric("Timeline", transition["timeline"])
        with transition_cols[2]:
            render_metric("Success Probability", f"{transition['success_probability']}%")
        with transition_cols[3]:
            render_metric("Expected Salary", str(transition["expected_salary"]))
        st.markdown("**Transition Roadmap**")
        for step in transition["roadmap"]:
            st.write(f"- {step}")
        st.markdown("**Required Certifications**")
        render_pills(transition["required_certifications"])

    learning = learning_recommendations(profile.career_goal, profile, missing_skills)
    with st.expander("Learning Recommendations", expanded=True):
        learning_cols = st.columns(3)
        for index, (label, values) in enumerate(learning.items()):
            with learning_cols[index % 3]:
                st.markdown(f"**{label.replace('_', ' ').title()}**")
                render_pills(values)

    interview = interview_preparation(profile.career_goal, profile)
    with st.expander("Interview Preparation", expanded=True):
        st.metric("Difficulty Level", interview["difficulty_level"])
        interview_cols = st.columns(3)
        sections = [
            ("HR Questions", interview["hr_questions"]),
            ("Technical / Role Questions", interview["technical_questions"]),
            ("Case Study Questions", interview["case_study_questions"]),
            ("Behavioral Questions", interview["behavioral_questions"]),
            ("Portfolio Review", interview["portfolio_review"]),
            ("Checklist", interview["checklist"]),
        ]
        for index, (label, values) in enumerate(sections):
            with interview_cols[index % 3]:
                st.markdown(f"**{label}**")
                render_pills(values)


def clean_gemini_response(text: str | None) -> str:
    if not text:
        return ""

    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:html|markdown|md)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    cleaned = SCRIPT_STYLE_RE.sub("", cleaned)
    cleaned = cleaned.replace("\r\n", "\n")
    cleaned = html.unescape(cleaned)
    return cleaned.strip()


def html_to_markdown(text: str) -> str:
    converted = clean_gemini_response(text)
    replacements = [
        (r"<\s*br\s*/?\s*>", "\n"),
        (r"</\s*p\s*>", "\n\n"),
        (r"<\s*p[^>]*>", ""),
        (r"</\s*div\s*>", "\n"),
        (r"<\s*div[^>]*>", ""),
        (r"<\s*li[^>]*>", "- "),
        (r"</\s*li\s*>", "\n"),
        (r"</?\s*(ul|ol)[^>]*>", "\n"),
        (r"<\s*h[1-6][^>]*>", "### "),
        (r"</\s*h[1-6]\s*>", "\n\n"),
        (r"<\s*(strong|b)[^>]*>", "**"),
        (r"</\s*(strong|b)\s*>", "**"),
        (r"<\s*(em|i)[^>]*>", "*"),
        (r"</\s*(em|i)\s*>", "*"),
    ]
    for pattern, replacement in replacements:
        converted = re.sub(pattern, replacement, converted, flags=re.IGNORECASE)

    converted = HTML_TAG_RE.sub("", converted)
    converted = re.sub(r"\n{3,}", "\n\n", converted)
    return converted.strip()


def render_clean_response(text: str | None) -> None:
    cleaned = clean_gemini_response(text)
    if not cleaned:
        return

    if HTML_TAG_RE.search(cleaned):
        st.markdown(html_to_markdown(cleaned))
    else:
        st.markdown(cleaned)


def render_timeline(items: list[dict[str, str]]) -> None:
    columns = st.columns(len(items))
    for index, (column, item) in enumerate(zip(columns, items)):
        with column:
            with st.container(border=True):
                st.caption(item["label"])
                st.subheader(item["title"])
                st.write(item["detail"])
                if index < len(items) - 1:
                    st.caption("Next step ->")


def salary_range_for_stage(career_goal: str, stage_index: int) -> str:
    salary_bands = {
        "AI": ["Not applicable", "INR 6-8 LPA", "INR 12-18 LPA", "INR 25-40 LPA", "INR 45-75 LPA"],
        "Data": ["Not applicable", "INR 5-7 LPA", "INR 10-16 LPA", "INR 22-35 LPA", "INR 38-60 LPA"],
        "Cybersecurity": ["Not applicable", "INR 5-8 LPA", "INR 12-20 LPA", "INR 24-38 LPA", "INR 42-65 LPA"],
        "Cloud": ["Not applicable", "INR 6-9 LPA", "INR 14-22 LPA", "INR 28-45 LPA", "INR 50-80 LPA"],
        "DevOps": ["Not applicable", "INR 6-9 LPA", "INR 14-24 LPA", "INR 30-48 LPA", "INR 55-85 LPA"],
        "Developer": ["Not applicable", "INR 4-7 LPA", "INR 10-18 LPA", "INR 22-38 LPA", "INR 40-70 LPA"],
        "Product": ["Not applicable", "INR 7-10 LPA", "INR 16-28 LPA", "INR 35-60 LPA", "INR 65-100 LPA"],
        "UX": ["Not applicable", "INR 4-7 LPA", "INR 10-16 LPA", "INR 20-32 LPA", "INR 35-55 LPA"],
    }
    for keyword, bands in salary_bands.items():
        if keyword.casefold() in career_goal.casefold():
            return bands[stage_index]
    return ["Not applicable", "INR 4-7 LPA", "INR 10-18 LPA", "INR 22-35 LPA", "INR 40-65 LPA"][stage_index]


def digital_twin_stages(
    profile: UserProfile,
    readiness: dict[str, object],
    probability: int,
    country_intelligence: CountryCareerIntelligence | None = None,
) -> list[dict[str, object]]:
    missing_skills = list(readiness.get("missing_skills", []))
    matched_skills = list(readiness.get("matched_skills", []))
    career_goal = profile.career_goal or "Target Career"
    current_role = profile.current_year if profile.current_year not in {"Not specified", "Not Specified"} else "Current You"

    staged_skills = [
        matched_skills[:4] or profile.skills[:4],
        missing_skills[:3] or matched_skills[:3] or ["Portfolio Building"],
        (missing_skills[:5] + ["Real Projects"])[:5] if missing_skills else matched_skills[:5],
        (missing_skills + ["Leadership", "System Design", "Mentoring"])[:6],
        (missing_skills + ["Architecture", "Strategy", "Leadership", "Mentoring", "Market Expertise"])[:7],
    ]
    confidence_scores = [
        max(10, calibrated_score("ai_confidence", readiness["score"])),
        max(20, calibrated_score("ai_confidence", readiness["score"] + 8)),
        max(35, calibrated_score("ai_confidence", probability)),
        max(45, calibrated_score("ai_confidence", probability + 6)),
        max(55, calibrated_score("ai_confidence", probability + 10)),
    ]
    probability_scores = [
        max(5, calibrated_score("success_probability", probability - 20)),
        max(10, calibrated_score("success_probability", probability - 5)),
        max(20, calibrated_score("success_probability", probability)),
        max(25, calibrated_score("success_probability", probability + 5)),
        max(30, calibrated_score("success_probability", probability + 9)),
    ]
    salary_ranges = projected_salary_ranges(career_goal, country_intelligence)

    return [
        {
            "label": "Current You",
            "role": current_role or "Student",
            "salary": salary_ranges[0],
            "skills": staged_skills[0],
            "career_stage": "Foundation",
            "confidence": confidence_scores[0],
            "probability": probability_scores[0],
            "salary_value": 0,
        },
        {
            "label": "1 Year Future",
            "role": f"{career_goal.split()[0]} Intern" if career_goal else "Career Intern",
            "salary": salary_ranges[1],
            "skills": staged_skills[1],
            "career_stage": "Internship Ready",
            "confidence": confidence_scores[1],
            "probability": probability_scores[1],
            "salary_value": salary_midpoint(salary_ranges[1]),
        },
        {
            "label": "3 Year Future",
            "role": career_goal,
            "salary": salary_ranges[2],
            "skills": staged_skills[2],
            "career_stage": "Early Professional",
            "confidence": confidence_scores[2],
            "probability": probability_scores[2],
            "salary_value": salary_midpoint(salary_ranges[2]),
        },
        {
            "label": "5 Year Future",
            "role": f"Senior {career_goal}",
            "salary": salary_ranges[3],
            "skills": staged_skills[3],
            "career_stage": "Advanced Contributor",
            "confidence": confidence_scores[3],
            "probability": probability_scores[3],
            "salary_value": salary_midpoint(salary_ranges[3]),
        },
        {
            "label": "10 Year Future",
            "role": f"Lead / Principal {career_goal}",
            "salary": salary_ranges[4],
            "skills": staged_skills[4],
            "career_stage": "Leadership Track",
            "confidence": confidence_scores[4],
            "probability": probability_scores[4],
            "salary_value": salary_midpoint(salary_ranges[4]),
        },
    ]


def projected_salary_ranges(career_goal: str, country_intelligence: CountryCareerIntelligence | None) -> list[str]:
    if not country_intelligence:
        return [salary_range_for_stage(career_goal, index) for index in range(5)]
    senior_mid = salary_midpoint(country_intelligence.senior_salary)
    ten_year_salary = f"{country_intelligence.senior_salary}+" if senior_mid else salary_range_for_stage(career_goal, 4)
    return [
        "Not applicable",
        country_intelligence.entry_salary,
        country_intelligence.mid_level_salary,
        country_intelligence.senior_salary,
        ten_year_salary,
    ]


def render_digital_twin(
    profile: UserProfile,
    readiness: dict[str, object],
    probability: int,
    country_intelligence: CountryCareerIntelligence | None = None,
) -> None:
    st.header("🚀 Your Digital Twin")
    st.caption("A projected career timeline based on your current profile, selected goal, skills, and readiness score.")

    stages = digital_twin_stages(profile, readiness, probability, country_intelligence)
    selected_stage_label = st.radio(
        "Explore timeline stage",
        [str(stage["label"]) for stage in stages],
        horizontal=True,
        label_visibility="collapsed",
    )
    for index, stage in enumerate(stages):
        with st.container(border=True):
            top_cols = st.columns([1.2, 2, 1])
            with top_cols[0]:
                st.caption(str(stage["label"]))
                st.subheader(str(stage["role"]))
            with top_cols[1]:
                st.markdown(f"**Salary Estimate:** {stage['salary']}")
                st.markdown(f"**Career Stage:** {stage['career_stage']}")
                skills = stage["skills"] or ["No skills detected yet"]
                st.markdown("**Skills Acquired:** " + ", ".join(str(skill) for skill in skills))
            with top_cols[2]:
                st.metric("Confidence Score", f"{stage['confidence']}%")
                st.progress(int(stage["confidence"]) / 100)
                st.metric("Probability", f"{stage['probability']}%")
                st.progress(int(stage["probability"]) / 100)
            if stage["label"] == selected_stage_label:
                st.info(f"Selected stage: {stage['label']} - focus on {', '.join(str(skill) for skill in (stage['skills'] or [])[:3])}.")

        if index < len(stages) - 1:
            arrow_cols = st.columns([1, 1, 1])
            with arrow_cols[1]:
                next_stage = stages[index + 1]["label"]
                st.markdown(f"**Progresses to {next_stage}**")
                st.progress((index + 1) / (len(stages) - 1))
                st.markdown("### ↓")

    salary_data = pd.DataFrame(
        [
            {"Stage": stage["label"], "Projected Salary Midpoint": stage["salary_value"]}
            for stage in stages
            if int(stage["salary_value"]) > 0
        ]
    )
    if not salary_data.empty:
        st.markdown("**Salary Graph**")
        chart = (
            alt.Chart(salary_data)
            .mark_line(point=True)
            .encode(
                x=alt.X("Stage:N", sort=None),
                y=alt.Y("Projected Salary Midpoint:Q"),
                tooltip=["Stage", "Projected Salary Midpoint"],
            )
        )
        st.altair_chart(chart, use_container_width=True)


def render_roadmap(items: list[dict[str, object]]) -> None:
    for item in items:
        with st.expander(f"{item['month']}: {item['focus']}", expanded=item["month"] in {"Month 1", "Month 2"}):
            for task in item["tasks"]:
                st.write(f"- {task}")
            if item.get("weeks"):
                st.markdown("**Weekly Milestones**")
                for week in item["weeks"]:
                    st.write(f"- **{week['week']}**: {week['milestone']}")
            st.success(str(item["outcome"]))


def render_profile_form(careers: dict[str, dict], autofill: dict[str, object], submit_label: str) -> bool:
    career_options = sorted(careers.keys())
    default_career_index = career_options.index("AI Engineer") if "AI Engineer" in career_options else 0
    gpa_value = str(autofill.get("gpa") or "")
    current_year_options = ["Not Specified", "1st Year", "2nd Year", "3rd Year", "4th Year", "Graduate", "Professional"]
    autofill_current_year = str(autofill.get("current_year") or "Not Specified")
    current_year_index = current_year_options.index(autofill_current_year) if autofill_current_year in current_year_options else 0

    with st.sidebar.expander("Education", expanded=True):
        name = st.text_input("Name", value=str(autofill.get("name") or ""))
        age_text = st.text_input("Age", value=str(autofill.get("age") or ""), placeholder="Not Specified")
        degree = st.text_input("Degree", value=str(autofill.get("degree") or ""))
        branch = st.text_input("Branch", value=str(autofill.get("branch") or ""))
        current_year = st.selectbox("Current Year", current_year_options, index=current_year_index)
        gpa_text = st.text_input("GPA / CGPA", value=gpa_value, placeholder="Not Specified")
    with st.sidebar.expander("Skills", expanded=True):
        skills = st.text_area("Skills", value=str(autofill.get("skills") or ""), help="Use commas or new lines.")
    with st.sidebar.expander("Projects"):
        projects = st.text_area("Projects", value=str(autofill.get("projects") or ""))
    with st.sidebar.expander("Experience"):
        internships = st.text_area("Experience / Internships", value=str(autofill.get("internships") or ""))
    with st.sidebar.expander("Certifications"):
        certifications = st.text_area("Certifications", value=str(autofill.get("certifications") or ""))
    with st.sidebar.expander("Languages"):
        languages = st.text_area("Languages", value=str(autofill.get("languages") or ""))
    with st.sidebar.expander("Achievements"):
        achievements = st.text_area("Achievements", value=str(autofill.get("achievements") or ""))
    with st.sidebar.expander("Career Preferences", expanded=True):
        weekly_study_hours = st.slider("Weekly Study Hours", min_value=0, max_value=40, value=0)
        career_query = st.text_input("Search Career Goal", value="", placeholder="Try fina, soft, audit, teach")
        suggested_careers = career_search_suggestions(career_query, careers, limit=80) if career_query.strip() else career_options
        if "AI Engineer" in suggested_careers:
            suggested_index = suggested_careers.index("AI Engineer")
        elif suggested_careers:
            suggested_index = 0
        else:
            suggested_careers = career_options
            suggested_index = default_career_index
        career_goal = st.selectbox("Career Goal", suggested_careers, index=suggested_index)
        target_country = st.selectbox("Target Country", SUPPORTED_COUNTRIES, index=0)
    submitted = st.sidebar.button(submit_label, use_container_width=True)

    age = int(age_text) if age_text.strip().isdigit() else None
    try:
        gpa = float(gpa_text) if gpa_text.strip() else 0.0
    except ValueError:
        gpa = 0.0
    should_update_profile = submitted or st.session_state.get("profile_created", False)
    if should_update_profile:
        st.session_state.profile = UserProfile(
            name=name.strip(),
            age=age,
            degree=degree.strip(),
            branch=branch.strip(),
            current_year=current_year,
            gpa=float(gpa),
            skills=split_multiline_or_csv(skills),
            projects=split_multiline_or_csv(projects),
            certifications=split_multiline_or_csv(certifications),
            internships=split_multiline_or_csv(internships),
            languages=split_multiline_or_csv(languages),
            achievements=split_multiline_or_csv(achievements),
            weekly_study_hours=int(weekly_study_hours),
            career_goal=career_goal,
            target_country=target_country.strip(),
        )
        if submitted:
            st.session_state.profile_created = True

    return submitted


def clear_resume_state(clear_profile: bool = True, clear_github: bool = True) -> None:
    keys = [
        "profile",
        "profile_created",
        "resume_parse",
        "resume_autofill",
        "resume_error",
        "resume_file_key",
        "github_username",
        "github_analysis",
        "github_error",
        "github_analysis_username",
        "github_analysis_source",
        "github_analysis_skipped",
    ]
    if not clear_profile:
        keys.remove("profile")
    if not clear_github:
        for key in [
            "github_username",
            "github_analysis",
            "github_error",
            "github_analysis_username",
            "github_analysis_source",
            "github_analysis_skipped",
        ]:
            keys.remove(key)
    for key in keys:
        st.session_state.pop(key, None)


def uploaded_file_key(uploaded_file: object) -> str:
    file_bytes = uploaded_file.getvalue()
    return hashlib.sha256(file_bytes).hexdigest()


def profile_form(careers: dict[str, dict]) -> UserProfile | None:
    st.sidebar.title("Career Twin AI")
    st.sidebar.caption("Build your profile, then generate the same dashboard from either path.")
    st.sidebar.subheader("How would you like to create your Career Twin?")

    method = st.sidebar.radio(
        "Creation method",
        ["Upload Resume", "Fill Manually"],
        index=0,
        captions=["Recommended. Fastest way to start.", "Enter every detail yourself."],
    )
    st.session_state.onboarding_method = method
    st.sidebar.divider()

    if method == "Upload Resume":
        st.sidebar.info("Upload Resume is recommended for faster profile creation.")
        uploaded_resume = st.sidebar.file_uploader("Upload resume", type=["pdf", "docx", "txt", "jpg", "jpeg", "png"])
        if uploaded_resume:
            current_file_key = uploaded_file_key(uploaded_resume)
            if st.session_state.get("resume_file_key") != current_file_key:
                clear_resume_state(clear_github=False)
                st.session_state.resume_file_key = current_file_key
            with st.sidebar.container(border=True):
                st.markdown("**Resume Ready**")
                st.caption(f"Filename: {uploaded_resume.name}")
                st.caption(f"File type: {uploaded_resume.type or uploaded_resume.name.split('.')[-1].upper()}")
                st.caption(f"Size: {len(uploaded_resume.getvalue()) / 1024:.1f} KB")
                st.success("Ready for analysis")

        if uploaded_resume and st.sidebar.button("Analyze Resume", use_container_width=True):
            try:
                current_file_key = uploaded_file_key(uploaded_resume)
                clear_resume_state(clear_github=False)
                st.session_state.resume_file_key = current_file_key
                with st.spinner("Parsing resume and extracting profile..."):
                    resume = parse_uploaded_resume(uploaded_resume, careers)
                st.session_state.resume_parse = resume
                if resume.extraction_status == "Failed":
                    st.session_state.resume_error = "Resume extraction failed. No usable fields were detected."
                    st.sidebar.error(st.session_state.resume_error)
                else:
                    st.session_state.resume_autofill = resume.autofill()
                    st.sidebar.success("Resume Analysis Complete")
                    extracted_username = github_username_from_url(resume.github)
                    if extracted_username:
                        try:
                            with st.spinner(f"Analyzing GitHub profile `{extracted_username}`..."):
                                did_analyze = analyze_github_to_state(extracted_username, force=False, source="resume")
                            if did_analyze:
                                st.sidebar.success("GitHub analysis complete.")
                            else:
                                st.sidebar.info("GitHub analysis already exists for this username.")
                        except RuntimeError as exc:
                            st.session_state.github_username = extracted_username
                            st.session_state.github_error = str(exc)
                            st.sidebar.warning(f"GitHub analysis needs attention: {exc}")
                st.rerun()
            except RuntimeError as exc:
                clear_resume_state(clear_github=False)
                st.session_state.resume_error = str(exc)
                st.sidebar.error(str(exc))
            except Exception:
                clear_resume_state(clear_github=False)
                st.session_state.resume_error = "Could not read this PDF resume. Try another PDF file."
                st.sidebar.error(st.session_state.resume_error)

        if st.session_state.get("resume_error"):
            st.sidebar.error(st.session_state.resume_error)
        resume = st.session_state.get("resume_parse")
        if resume:
            if resume.extraction_status == "Success":
                st.sidebar.success("Extraction Status: Success")
            elif resume.extraction_status == "Partial":
                st.sidebar.warning("Extraction Status: Partial")
            else:
                st.sidebar.error("Extraction Status: Failed")
            st.sidebar.metric("Resume Strength", f"{resume.strength_score}%")
            st.sidebar.caption(f"{len(resume.skills)} skills detected")
            with st.sidebar.expander("Exact extracted fields", expanded=True):
                st.write(f"Name: {display_value(resume.name)}")
                st.write(f"Email: {display_value(resume.email)}")
                st.write(f"Phone: {display_value(resume.phone)}")
                st.write(f"LinkedIn: {display_value(resume.linkedin)}")
                st.write(f"GitHub: {display_value(resume.github)}")
                st.write(f"Portfolio: {display_value(resume.portfolio)}")
                st.write(f"Location: {display_value(resume.location)}")
                st.write(f"Age: {display_value(resume.age)}")
                st.write(f"Degree: {display_value(resume.degree)}")
                st.write(f"Branch: {display_value(resume.branch)}")
                st.write(f"University: {display_value(resume.university)}")
                st.write(f"Current Year: {display_value(resume.current_year)}")
                st.write(f"CGPA: {display_value(resume.gpa)}")
                st.write(f"Detected Domain: {display_value(resume.detected_domain)} ({round(resume.domain_confidence * 100)}%)")
                st.write(f"Skills: {', '.join(resume.skills) if resume.skills else 'Not Specified'}")
                st.write(f"Education: {'; '.join(resume.education) if resume.education else 'Not Specified'}")
                st.write(f"Certifications: {'; '.join(resume.certifications) if resume.certifications else 'Not Specified'}")
                st.write(f"Projects: {'; '.join(resume.projects) if resume.projects else 'Not Specified'}")
                st.write(f"Experience: {'; '.join(resume.experience) if resume.experience else 'Not Specified'}")
            if resume.extraction_status != "Failed":
                with st.sidebar.expander("Edit extracted contact fields"):
                    resume.name = st.text_input("Extracted Name", value=resume.name)
                    resume.email = st.text_input("Extracted Email", value=resume.email)
                    resume.phone = st.text_input("Extracted Phone", value=resume.phone)
                    resume.linkedin = st.text_input("Extracted LinkedIn", value=resume.linkedin)
                    resume.github = st.text_input("Extracted GitHub", value=resume.github)
                    resume.portfolio = st.text_input("Extracted Portfolio", value=resume.portfolio)
                    resume.location = st.text_input("Extracted Location", value=resume.location)
                    st.session_state.resume_autofill["name"] = resume.name
                st.sidebar.subheader("Review and edit extracted data")
                render_profile_form(careers, st.session_state.get("resume_autofill", {}), "Generate Career Twin")
        else:
            st.sidebar.caption("The manual form will appear after resume analysis so you can review and edit extracted data.")

    else:
        clear_resume_state(clear_profile=False, clear_github=False)
        st.sidebar.subheader("Manual Entry")
        render_profile_form(careers, {}, "Generate Career Twin")

    st.sidebar.divider()
    st.sidebar.subheader("GitHub Profile Analysis")
    github_username = st.sidebar.text_input("GitHub Username", value=st.session_state.get("github_username", ""))
    if st.sidebar.button("Analyze GitHub", use_container_width=True):
        try:
            with st.spinner("Analyzing GitHub repositories..."):
                analyze_github_to_state(github_username, force=True, source="manual")
            st.sidebar.success("GitHub analysis complete.")
        except RuntimeError as exc:
            st.session_state.github_error = str(exc)
            st.session_state.pop("github_analysis", None)
            st.sidebar.error(str(exc))
        except Exception:
            st.session_state.github_error = "Could not analyze this GitHub profile."
            st.session_state.pop("github_analysis", None)
            st.sidebar.error(st.session_state.github_error)

    if st.session_state.get("github_error"):
        st.sidebar.error(st.session_state.github_error)

    return st.session_state.get("profile")


def main() -> None:
    careers = load_careers()
    profile = profile_form(careers)

    st.title("Career Twin AI")
    st.caption(
        "See the future version of your career before you live it. Build a digital career twin..."
    )
    render_progress_steps(4 if profile else 1)

    if profile is None:
        render_onboarding_intro(st.session_state.get("onboarding_method", "Upload Resume"))
        st.info("Choose Upload Resume or Fill Manually in the sidebar to create your profile.")
        if st.session_state.get("github_analysis"):
            st.divider()
            render_github_analysis(st.session_state.github_analysis)
        else:
            st.divider()
            render_github_cta()
        render_feedback_contact()
        render_footer()
        return

    selected_career = careers[profile.career_goal]
    career_knowledge = get_career_knowledge(profile.career_goal, selected_career)
    github_relevant = is_github_relevant(career_knowledge)
    readiness = calculate_readiness(profile, selected_career)
    country_intelligence = get_country_career_intelligence(profile.career_goal, profile.target_country, selected_career)
    probability = calculate_success_probability(profile, readiness["score"], len(readiness["missing_skills"]))
    resume = st.session_state.get("resume_parse")
    github_analysis = st.session_state.get("github_analysis")
    roadmap_items = fallback_roadmap(
        readiness["missing_skills"],
        profile.career_goal,
        profile.target_country,
        profile.weekly_study_hours,
    )
    resume_match = analyze_resume_match(resume, profile, career_knowledge, github_analysis if github_relevant else None) if resume else None
    mentor_context = build_mentor_context(
        profile=profile,
        resume=resume,
        github_analysis=github_analysis if github_relevant else None,
        country_intelligence=country_intelligence,
        roadmap=roadmap_items,
        missing_skills=readiness["missing_skills"],
        resume_match=resume_match,
    )
    mentor_context["career_knowledge"] = career_knowledge
    mentor_context["detected_domain"] = getattr(resume, "detected_domain", career_knowledge.get("domain", "General")) if resume else career_knowledge.get("domain", "General")

    if st.sidebar.button("Save Snapshot", use_container_width=True):
        save_profile(profile, readiness, probability)
        st.sidebar.success("Snapshot saved.")

    section_anchor("overview")
    st.subheader(f"{profile.career_goal} in {profile.target_country}")
    render_dashboard_nav(bool(resume), bool(github_analysis and github_relevant))
    metric_cols = st.columns(4)
    with metric_cols[0]:
        render_metric("Readiness Score", f"{readiness['score']}%", f"{readiness.get('label', score_label(int(readiness['score'])))} current profile quality.")
        st.progress(readiness["score"] / 100)
    with metric_cols[1]:
        render_metric("Success Probability", f"{probability}%", f"{score_label(probability)} future momentum estimate.")
        st.progress(probability / 100)
    with metric_cols[2]:
        render_metric("Matched Skills", str(len(readiness["matched_skills"])), f"Out of {len(readiness['required_skills'])} required skills.")
    with metric_cols[3]:
        render_metric("Weekly Effort", f"{profile.weekly_study_hours}h", "Consistency is your route multiplier.")
    coach_scores = render_career_coach_scores(
        profile,
        readiness,
        probability,
        resume,
        github_relevant,
        github_analysis if github_relevant else None,
        country_intelligence,
        career_knowledge,
    )
    render_ai_mentor_chat(mentor_context)

    st.divider()
    section_anchor("career-match")
    render_selected_career_overview(
        profile,
        readiness,
        probability,
        country_intelligence,
        career_knowledge,
        resume_match,
        coach_scores,
        roadmap_items,
    )

    report = build_dashboard_report(
        profile,
        readiness,
        probability,
        country_intelligence,
        career_knowledge,
        resume,
        github_analysis if github_relevant else None,
        resume_match,
        roadmap_items,
    )
    with st.expander("Download Report"):
        export_cols = st.columns(2)
        with export_cols[0]:
            try:
                st.download_button(
                    "Download PDF Report",
                    data=build_pdf_report(report),
                    file_name="career_twin_report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            except RuntimeError as exc:
                st.warning(str(exc))
        with export_cols[1]:
            st.download_button(
                "Download JSON Export",
                data=json.dumps(report, indent=2, default=str),
                file_name="career_twin_export.json",
                mime="application/json",
                use_container_width=True,
            )

    st.divider()
    section_anchor("career-twin")
    render_digital_twin(profile, readiness, probability, country_intelligence)
    st.divider()
    section_anchor("country-intelligence")
    render_country_intelligence(country_intelligence)
    st.divider()

    section_anchor("career-intelligence")
    render_universal_career_intelligence(profile, resume, career_knowledge, readiness["missing_skills"])
    st.divider()

    if resume:
        section_anchor("resume-analysis")
        render_resume_insights(resume, readiness["missing_skills"])
        st.divider()

    if resume and resume_match:
        section_anchor("resume-match")
        render_resume_match_score(resume_match, resume, careers)
        st.divider()

    if github_analysis and github_relevant:
        section_anchor("github-analysis")
        render_github_analysis(github_analysis)
        st.divider()
    elif not github_analysis and github_relevant:
        render_github_cta()
        st.divider()

    section_anchor("skill-gap")
    gap_cols = st.columns([1, 1])
    with gap_cols[0]:
        st.subheader("Skill Gap Analysis")
        st.caption("Current skills that match your target role.")
        render_pills(readiness["matched_skills"])
    with gap_cols[1]:
        st.subheader("Missing Skills")
        st.caption("Prioritize these to increase readiness fastest.")
        render_pills(readiness["missing_skills"])

    st.divider()

    section_anchor("probability")
    with st.spinner("Generating career probability reasoning..."):
        explanation = generate_explanation(profile, readiness)
    with st.container():
        st.subheader("Career Probability Reasoning")
        positive_factors, improvement_factors = probability_factors(profile, readiness)
        factor_cols = st.columns(2)
        with factor_cols[0]:
            st.markdown("**Positive Factors**")
            render_pills(positive_factors)
        with factor_cols[1]:
            st.markdown("**Score Constraints**")
            render_pills(improvement_factors)
        if explanation:
            render_clean_response(explanation)
        else:
            reasons = [
                f"You already match {len(readiness['matched_skills'])} required skills.",
                f"You need to close {len(readiness['missing_skills'])} skill gaps.",
                f"Your weekly study pace is {profile.weekly_study_hours} hours.",
            ]
            if profile.internship_count:
                reasons.append("Internship experience improves your credibility for this path.")
            else:
                reasons.append("Adding one internship or applied project would improve your signal.")
            st.markdown("\n".join(f"- {reason}" for reason in reasons))

    st.divider()

    section_anchor("future-simulation")
    st.subheader("Future Simulation Notes")
    with st.spinner("Generating future simulation notes..."):
        gemini_future = generate_future_simulation(profile, readiness)
    with st.expander("Classic timeline summary"):
        render_timeline(fallback_future(profile, readiness["score"]))
    if gemini_future:
        with st.expander("AI future notes"):
            render_clean_response(gemini_future)

    st.divider()

    section_anchor("roadmap")
    st.subheader("AI Career Roadmap")
    with st.spinner("Generating AI roadmap notes..."):
        gemini_roadmap = generate_roadmap(profile, readiness)
    render_roadmap(roadmap_items)
    if gemini_roadmap:
        with st.expander("AI roadmap notes"):
            render_clean_response(gemini_roadmap)

    st.divider()

    section_anchor("action-plan")
    action_cols = st.columns([2, 1])
    with action_cols[0]:
        st.subheader("Weekly Action Plan")
        for action in fallback_action_plan(
            readiness["missing_skills"],
            profile.career_goal,
            profile.weekly_study_hours,
            profile.target_country,
        ):
            st.markdown(f"**{action['week']}**: {action['task']}")
    with action_cols[1]:
        st.subheader("Recent Snapshots")
        profiles = recent_profiles()
        if profiles:
            for item in profiles:
                st.caption(
                    f"{item['name']} | {item['career_goal']} | Readiness {item['readiness_score']}% | Probability {item['success_probability']}%"
                )
        else:
            st.caption("No saved snapshots yet.")

    section_anchor("feedback")
    render_feedback_contact()
    render_footer()


if __name__ == "__main__":
    main()
