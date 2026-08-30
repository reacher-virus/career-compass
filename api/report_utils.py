from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List
import fitz


def wrap_pdf_text(text: str, width: int) -> List[str]:
    words = str(text).split()
    lines: List[str] = []
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


def draw_score_bars(page: Any, x: int, y: int, scores: Dict[str, int]) -> None:
    page.insert_text((x, y), "Score Snapshot", fontsize=13, fontname="helv")
    y += 16
    for label, score in scores.items():
        bounded = max(0, min(int(score), 100))
        page.insert_text((x, y + 9), f"{label}: {bounded}%", fontsize=9, fontname="helv")
        page.draw_rect(fitz.Rect(x + 115, y, x + 315, y + 10), color=(0.78, 0.78, 0.78), fill=(0.92, 0.92, 0.92))
        page.draw_rect(fitz.Rect(x + 115, y, x + 115 + bounded * 2, y + 10), color=(0.12, 0.38, 0.78), fill=(0.12, 0.38, 0.78))
        y += 18


def build_pdf_report_bytes(report: Dict[str, Any]) -> bytes:
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)
    y = 48

    def write_line(text: str, size: int = 10, bold: bool = False) -> None:
        nonlocal y, page
        if y > 790:
            page = doc.new_page(width=595, height=842)
            y = 48
        font = "helv"
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

    profile = report.get("profile", {})
    write_line("Career Twin AI - Professional Career Intelligence Report", 18, True)
    write_line(f"Generated: {report.get('generated_at', datetime.now().isoformat())}", 9)
    write_line("")
    write_line(f"Name: {profile.get('name') or 'Not specified'}", 11)
    write_line(f"Career Goal: {profile.get('career_goal')} in {profile.get('target_country')}", 11)
    
    readiness = report.get("readiness", {})
    write_line(f"Career Readiness: {readiness.get('score', 0)}%", 11)
    write_line(f"Success Probability: {report.get('success_probability', 0)}%", 11)
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
            "Readiness": int(readiness.get("score", 0)),
            "Success": int(report.get("success_probability", 0)),
            "ATS": int((report.get("resume") or {}).get("ats_readiness", readiness.get("score", 0)) or 0),
        },
    )
    y += 86
    
    write_section(
        "Career Readiness",
        "Career Readiness measures current profile quality using education, skills, projects, certifications, experience, achievements, ATS quality, and consistency.",
    )
    write_section(
        "Success Probability",
        "Success Probability estimates future momentum based on current evidence, study consistency, portfolio proof, experience, and roadmap progress.",
    )
    
    write_line("Matched Skills", 13, True)
    for item in readiness.get("matched_skills", [])[:12]:
        write_line(f"- {item}")
    write_line("Missing Skills", 13, True)
    for item in readiness.get("missing_skills", [])[:12]:
        write_line(f"- {item}")
        
    country = report.get("country_intelligence", {})
    if country:
        write_section(
            "Country Intelligence",
            "Country Intelligence explains whether the selected country is suitable for the target career using salary bands, demand, hiring trend, visa complexity, and market growth.",
        )
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
        ]:
            if key in country:
                write_line(f"{key.replace('_', ' ').title()}: {country.get(key, '')}")
                
    if report.get("github"):
        github = report["github"]
        write_line("GitHub Analysis", 13, True)
        write_line(f"Username: {github.get('username')}")
        write_line(f"Score: {github.get('score')}% | Repositories: {github.get('repositories')}")
        
    if report.get("roadmap"):
        write_section(
            "Career Roadmap",
            "The roadmap turns missing skills into a practical learning plan for professional growth.",
        )
        for item in report["roadmap"][:6]:
            write_line(f"{item.get('month', '')}: {item.get('focus', '')}")
            for week in item.get("weeks", [])[:4]:
                write_line(f"  {week.get('week', '')}: {week.get('milestone', '')}", 9)

    write_line("")
    write_line("Career Twin AI - Powered by Advanced Career Intelligence", 9)
    pdf = doc.tobytes()
    doc.close()
    return pdf
