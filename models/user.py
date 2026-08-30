from dataclasses import dataclass, field


@dataclass
class UserProfile:
    name: str
    age: int | None
    degree: str
    branch: str
    current_year: str
    gpa: float
    skills: list[str] = field(default_factory=list)
    projects: list[str] = field(default_factory=list)
    certifications: list[str] = field(default_factory=list)
    internships: list[str] = field(default_factory=list)
    languages: list[str] = field(default_factory=list)
    achievements: list[str] = field(default_factory=list)
    weekly_study_hours: int = 0
    career_goal: str = ""
    target_country: str = ""

    @property
    def project_count(self) -> int:
        return len([project for project in self.projects if project.strip()])

    @property
    def certification_count(self) -> int:
        return len([cert for cert in self.certifications if cert.strip()])

    @property
    def internship_count(self) -> int:
        return len([internship for internship in self.internships if internship.strip()])
