from __future__ import annotations

from typing import Any, Dict, List, Optional
import io
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from services.career_engine import load_careers
from services.resume_parser import (
    ResumeParseResult,
    parse_resume_text,
    extract_pdf_text,
    extract_docx_text,
    extract_image_text,
)
from services.resume_matcher import (
    compare_resume_to_job_description,
    JobDescriptionMatch,
)
from api.schemas import (
    JobDescriptionMatchRequest,
    JobDescriptionMatchResponse,
    ResumeParsedData,
)
import tempfile
from pathlib import Path

router = APIRouter(prefix="/api/resume", tags=["Resume"])


class FileAdapter:
    def __init__(self, name: str, data: bytes):
        self.name = name
        self._data = data

    def getbuffer(self) -> bytes:
        return self._data

    def getvalue(self) -> bytes:
        return self._data


def extract_text_from_bytes(filename: str, file_bytes: bytes) -> str:
    suffix = Path(filename).suffix.casefold() or ".pdf"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(file_bytes)
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
        raise RuntimeError(f"Unsupported resume format '{suffix}'. Upload PDF, DOCX, TXT, JPG, JPEG, or PNG.")
    finally:
        Path(temp_path).unlink(missing_ok=True)


def parse_result_to_dict(result: ResumeParseResult) -> Dict[str, Any]:
    return {
        "text": result.text,
        "name": result.name,
        "email": result.email,
        "phone": result.phone,
        "linkedin": result.linkedin,
        "github": result.github,
        "portfolio": result.portfolio,
        "location": result.location,
        "age": result.age,
        "degree": result.degree,
        "branch": result.branch,
        "university": result.university,
        "start_year": result.start_year,
        "graduation_year": result.graduation_year,
        "current_year": result.current_year,
        "gpa": result.gpa,
        "current_designation": result.current_designation,
        "extraction_status": result.extraction_status,
        "strength_score": result.strength_score,
        "completeness_score": result.completeness_score,
        "industry_readiness_score": result.industry_readiness_score,
        "ats_readiness_score": result.ats_readiness_score,
        "overall_career_readiness_score": result.overall_career_readiness_score,
        "skills": result.skills,
        "skill_categories": result.skill_categories,
        "structured_projects": result.structured_projects,
        "structured_experience": result.structured_experience,
        "structured_certifications": result.structured_certifications,
        "field_confidence": result.field_confidence,
        "insights": result.insights,
        "detected_domain": result.detected_domain,
        "domain_confidence": result.domain_confidence,
        "autofill": result.autofill(),
    }


@router.post("/parse")
async def parse_resume(file: UploadFile = File(...)) -> Dict[str, Any]:
    careers = load_careers()
    try:
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")
        
        extracted_text = extract_text_from_bytes(file.filename or "resume.pdf", content)
        if not extracted_text:
            raise HTTPException(status_code=400, detail="No readable text could be extracted from this resume.")
        
        result = parse_resume_text(extracted_text, careers)
        return parse_result_to_dict(result)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Failed to parse resume: {str(exc)}")


@router.post("/match-jd", response_model=JobDescriptionMatchResponse)
def match_job_description(request: JobDescriptionMatchRequest) -> JobDescriptionMatchResponse:
    careers = load_careers()
    resume_text = request.resume_text
    
    # If resume_data was supplied, construct minimal resume object or re-parse
    if not resume_text and request.resume_data:
        resume_text = request.resume_data.get("text", "")
    
    if not resume_text:
        raise HTTPException(status_code=400, detail="Resume text is required for Job Description comparison.")
    
    if not request.job_description_text.strip():
        raise HTTPException(status_code=400, detail="Job description text is required.")
        
    resume_obj = parse_resume_text(resume_text, careers)
    
    match: JobDescriptionMatch = compare_resume_to_job_description(
        resume_obj, request.job_description_text.strip(), careers
    )
    
    return JobDescriptionMatchResponse(
        keyword_match=match.keyword_match,
        semantic_match=match.semantic_match,
        technical_match=match.technical_match,
        experience_match=match.experience_match,
        education_match=match.education_match,
        certification_match=match.certification_match,
        hiring_recommendation=match.hiring_recommendation,
        matched_keywords=match.matched_keywords,
        missing_keywords=match.missing_keywords,
        highlighted_missing_keywords=match.highlighted_missing_keywords,
    )
