from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class UserProfileSchema(BaseModel):
    name: str = ""
    age: Optional[int] = None
    degree: str = ""
    branch: str = ""
    current_year: str = "Not Specified"
    gpa: float = 0.0
    skills: List[str] = Field(default_factory=list)
    projects: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    internships: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)
    achievements: List[str] = Field(default_factory=list)
    weekly_study_hours: int = 0
    career_goal: str = ""
    target_country: str = ""


class ResumeParsedData(BaseModel):
    text: str = ""
    name: str = ""
    email: str = ""
    phone: str = ""
    linkedin: str = ""
    github: str = ""
    portfolio: str = ""
    location: str = ""
    age: Optional[int] = None
    degree: str = ""
    branch: str = ""
    university: str = ""
    start_year: Optional[int] = None
    graduation_year: Optional[int] = None
    current_year: str = "Not Specified"
    gpa: Optional[float] = None
    current_designation: str = ""
    extraction_status: str = "Failed"
    strength_score: int = 0
    completeness_score: int = 0
    industry_readiness_score: int = 0
    ats_readiness_score: int = 0
    overall_career_readiness_score: int = 0
    skills: List[str] = Field(default_factory=list)
    skill_categories: Dict[str, List[str]] = Field(default_factory=dict)
    structured_projects: List[Dict[str, str]] = Field(default_factory=list)
    structured_experience: List[Dict[str, str]] = Field(default_factory=list)
    structured_certifications: List[Dict[str, str]] = Field(default_factory=list)
    field_confidence: Dict[str, float] = Field(default_factory=dict)
    insights: List[str] = Field(default_factory=list)
    detected_domain: str = "General"
    domain_confidence: float = 0.0
    autofill: Dict[str, Any] = Field(default_factory=dict)


class JobDescriptionMatchRequest(BaseModel):
    resume_text: str = ""
    resume_data: Optional[Dict[str, Any]] = None
    job_description_text: str = ""


class JobDescriptionMatchResponse(BaseModel):
    keyword_match: int = 0
    semantic_match: int = 0
    technical_match: int = 0
    experience_match: int = 0
    education_match: int = 0
    certification_match: int = 0
    hiring_recommendation: str = "Review Needed"
    matched_keywords: List[str] = Field(default_factory=list)
    missing_keywords: List[str] = Field(default_factory=list)
    highlighted_missing_keywords: List[str] = Field(default_factory=list)


class GitHubAnalysisRequest(BaseModel):
    username: str
    force: bool = False


class AnalyzeRequest(BaseModel):
    profile: UserProfileSchema
    resume: Optional[Dict[str, Any]] = None
    github_username: Optional[str] = None
    github_analysis: Optional[Dict[str, Any]] = None


class DigitalTwinStage(BaseModel):
    label: str
    role: str
    salary: str
    skills: List[str]
    career_stage: str
    confidence: int
    probability: int
    salary_value: int


class ScorecardData(BaseModel):
    score: int
    label: str
    positives: List[str] = Field(default_factory=list)
    improvements: List[str] = Field(default_factory=list)
    why: str = ""


class AnalysisResponse(BaseModel):
    profile: UserProfileSchema
    career_goal: str
    target_country: str
    readiness: Dict[str, Any]
    success_probability: int
    coach_scores: Dict[str, ScorecardData]
    career_knowledge: Dict[str, Any]
    country_intelligence: Dict[str, Any]
    digital_twin: List[DigitalTwinStage]
    roadmap: List[Dict[str, Any]]
    action_plan: List[Dict[str, Any]]
    resume_match: Optional[Dict[str, Any]] = None
    github_analysis: Optional[Dict[str, Any]] = None
    github_relevant: bool = False
    ai_explanation: Optional[str] = None
    ai_future: Optional[str] = None
    ai_roadmap: Optional[str] = None
    recommended_careers: List[Dict[str, Any]] = Field(default_factory=list)
    generated_at: str


class MentorChatRequest(BaseModel):
    question: str
    context: Dict[str, Any] = Field(default_factory=dict)
    history: List[Dict[str, str]] = Field(default_factory=list)


class MentorChatResponse(BaseModel):
    answer: str


class SaveProfileRequest(BaseModel):
    profile: UserProfileSchema
    analysis: Dict[str, Any]
    success_probability: int


class FeedbackRequest(BaseModel):
    feedback_type: str = "General Feedback"
    rating: int = 5
    subject: str = ""
    message: str = ""
    email: Optional[str] = None
