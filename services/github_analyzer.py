from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import math
import os
from dotenv import load_dotenv
from typing import Any

import requests

from services.scoring import calibrated_score

load_dotenv()
print("GITHUB_TOKEN =", os.getenv("GITHUB_TOKEN"))
print("GitHub Token Exists:", bool(os.getenv("GITHUB_TOKEN")))

print(
    "GitHub Token Prefix:",
    os.getenv("GITHUB_TOKEN")[:20] if os.getenv("GITHUB_TOKEN") else "NOT FOUND",
)

AI_KEYWORDS = {
    "ai",
    "artificial-intelligence",
    "chatbot",
    "computer-vision",
    "deep-learning",
    "gemini",
    "langchain",
    "llm",
    "machine-learning",
    "ml",
    "nlp",
    "neural",
    "tensorflow",
    "pytorch",
}

WEB_KEYWORDS = {
    "api",
    "backend",
    "css",
    "dashboard",
    "django",
    "fastapi",
    "frontend",
    "fullstack",
    "html",
    "javascript",
    "next",
    "react",
    "streamlit",
    "typescript",
    "web",
}

PROJECT_CATEGORY_KEYWORDS = {
    "AI / ML": AI_KEYWORDS | {"model", "inference", "rag", "transformer", "huggingface", "diffusion"},
    "Web Development": WEB_KEYWORDS | {"website", "webapp", "tailwind", "vue", "svelte", "node"},
    "Mobile": {"android", "ios", "kotlin", "swift", "flutter", "react-native", "mobile"},
    "DevOps": {"devops", "ci", "cd", "pipeline", "terraform", "ansible", "helm", "jenkins"},
    "Cloud": {"aws", "azure", "gcp", "cloud", "serverless", "lambda", "firebase"},
    "Data Science": {"data", "analytics", "pandas", "notebook", "visualization", "etl", "warehouse"},
    "Systems Programming": {"kernel", "linux", "os", "operating-system", "runtime", "compiler", "memory", "filesystem"},
    "Embedded Systems": {"embedded", "firmware", "arduino", "iot", "esp32", "microcontroller"},
    "Cybersecurity": {"security", "crypto", "cryptography", "reverse", "malware", "ctf", "pentest", "forensics"},
    "Blockchain": {"blockchain", "ethereum", "solidity", "web3", "smart-contract"},
    "Game Development": {"game", "unity", "unreal", "pygame", "gamedev"},
    "Desktop Applications": {"desktop", "electron", "qt", "gtk", "gui"},
    "CLI Tools": {"cli", "terminal", "command-line", "shell"},
    "Libraries": {"library", "package", "sdk", "toolkit", "client"},
    "Frameworks": {"framework", "fastapi", "django", "react", "vue", "svelte", "express"},
}

LANGUAGE_COMPLEXITY = {
    "C": 18,
    "C++": 18,
    "Rust": 18,
    "Go": 15,
    "Java": 14,
    "Kotlin": 13,
    "Swift": 13,
    "TypeScript": 12,
    "Python": 11,
    "JavaScript": 10,
    "C#": 13,
    "Scala": 15,
    "Elixir": 13,
    "Haskell": 16,
    "Jupyter Notebook": 9,
}

LANGUAGE_TO_SKILLS = {
    "C": ["Low-Level Programming", "Systems Programming", "Memory Management"],
    "C++": ["Systems Programming", "Performance Engineering", "Memory Management"],
    "CSS": ["Frontend Development", "Responsive UI"],
    "Dart": ["Flutter", "Mobile Development"],
    "Go": ["Backend Development", "Distributed Systems", "Cloud Services"],
    "HTML": ["Frontend Development", "Semantic UI"],
    "Java": ["Backend Development", "Object-Oriented Design"],
    "JavaScript": ["Web Development", "Frontend Engineering"],
    "Jupyter Notebook": ["Machine Learning", "Data Analysis", "Experimentation"],
    "Kotlin": ["Android Development", "Mobile Architecture"],
    "Python": ["Backend Development", "Automation", "Data Engineering"],
    "R": ["Statistics", "Data Analysis"],
    "Rust": ["Systems Programming", "Memory Safety", "Performance Engineering"],
    "SQL": ["Database Design", "Data Analysis"],
    "Swift": ["iOS Development", "Mobile Development"],
    "TypeScript": ["Frontend Architecture", "Typed JavaScript", "React"],
}


@dataclass
class GitHubRepoSummary:
    name: str
    description: str
    language: str
    stars: int
    forks: int = 0
    watchers: int = 0
    open_issues: int = 0
    size_kb: int = 0
    topics: list[str] = field(default_factory=list)
    updated_at: str = ""
    url: str = ""
    project_type: str = "General"
    difficulty_level: str = "Beginner"
    has_license: bool = False
    has_readme_signal: bool = False
    has_releases_signal: bool = False
    quality_score: int = 0


@dataclass
class GitHubAnalysis:
    username: str
    repository_count: int
    total_stars: int
    total_forks: int
    followers: int
    following: int
    public_gists: int
    years_active: int
    language_counts: dict[str, int]
    category_counts: dict[str, int]
    quality_distribution: dict[str, int]
    technology_stack_counts: dict[str, int]
    top_skills: list[str]
    ai_ml_projects: list[GitHubRepoSummary]
    web_projects: list[GitHubRepoSummary]
    activity_level: str
    github_score: int
    project_quality_score: int
    portfolio_strength: str
    most_starred_repository: str
    most_used_language: str
    open_source_contribution_level: str
    suitable_careers: list[dict[str, str]]
    strengths: list[str]
    weaknesses: list[str]
    recommendations: list[str]
    repos: list[GitHubRepoSummary]


def analyze_github_profile(username: str) -> GitHubAnalysis:
    username = username.strip()
    if not username:
        raise RuntimeError("Enter a GitHub username.")

    user = fetch_github_user(username)
    repos = fetch_public_repos(username)
    summaries = [summarize_repo(repo) for repo in repos]
    language_counts = count_languages(summaries)
    category_counts = count_categories(summaries)
    quality_distribution = count_quality_distribution(summaries)
    technology_stack_counts = count_technology_stack(summaries)
    ai_projects = [repo for repo in summaries if repo.project_type == "AI / ML"]
    web_projects = [repo for repo in summaries if repo.project_type == "Web Development"]
    total_stars = sum(repo.stars for repo in summaries)
    total_forks = sum(repo.forks for repo in summaries)
    activity_level = calculate_activity_level(summaries)
    project_quality_score = calculate_project_quality_score(summaries)
    followers = int(user.get("followers") or 0)
    following = int(user.get("following") or 0)
    public_gists = int(user.get("public_gists") or 0)
    years_active = calculate_years_active(user.get("created_at") or "")
    most_starred = max(summaries, key=lambda repo: repo.stars, default=None)
    most_used_language = next(iter(language_counts), "Unknown")
    github_score = calculate_github_score(
        repo_count=len(summaries),
        stars=total_stars,
        forks=total_forks,
        followers=followers,
        language_count=len(language_counts),
        category_count=len(category_counts),
        ai_project_count=len(ai_projects),
        web_project_count=len(web_projects),
        activity_level=activity_level,
        project_quality_score=project_quality_score,
        documentation_score=average_documentation_score(summaries),
        recent_ratio=recent_activity_ratio(summaries),
    )
    top_skills = extract_skills(summaries, language_counts)
    suitable_careers = infer_careers(category_counts, top_skills, summaries)
    strengths, weaknesses = portfolio_strengths_weaknesses(summaries, top_skills, category_counts, activity_level)

    return GitHubAnalysis(
        username=username,
        repository_count=len(summaries),
        total_stars=total_stars,
        total_forks=total_forks,
        followers=followers,
        following=following,
        public_gists=public_gists,
        years_active=years_active,
        language_counts=language_counts,
        category_counts=category_counts,
        quality_distribution=quality_distribution,
        technology_stack_counts=technology_stack_counts,
        top_skills=top_skills,
        ai_ml_projects=ai_projects,
        web_projects=web_projects,
        activity_level=activity_level,
        github_score=github_score,
        project_quality_score=project_quality_score,
        portfolio_strength=portfolio_strength(github_score),
        most_starred_repository=most_starred.name if most_starred else "None",
        most_used_language=most_used_language,
        open_source_contribution_level=open_source_level(total_stars, total_forks, followers, project_quality_score),
        suitable_careers=suitable_careers,
        strengths=strengths,
        weaknesses=weaknesses,
        recommendations=build_recommendations(
            summaries=summaries,
            ai_project_count=len(ai_projects),
            web_project_count=len(web_projects),
            activity_level=activity_level,
            top_skills=top_skills,
        ),
        repos=sorted(summaries, key=lambda repo: (repo.quality_score, repo.stars), reverse=True)[:10],
    )


def fetch_github_user(username: str) -> dict[str, Any]:
    url = f"https://api.github.com/users/{username}"
    headers = {
           "Accept": "application/vnd.github+json",
           "User-Agent": "Career-Twin-AI",
       }

    github_token = os.getenv("GITHUB_TOKEN")
    if github_token:
           headers["Authorization"] = f"Bearer {github_token}"

    response = requests.get(
         url,
         headers=headers,
        timeout=15,
    )
    if response.status_code == 404:
        raise RuntimeError("GitHub user not found.")
    if response.status_code == 403:
        raise RuntimeError("GitHub API rate limit reached. Try again later.")
    if response.status_code >= 400:
        raise RuntimeError("Could not fetch this GitHub profile.")
    return response.json()


def fetch_public_repos(username: str) -> list[dict[str, Any]]:
    url = f"https://api.github.com/users/{username}/repos"

    headers = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "Career-Twin-AI",
    }

    github_token = os.getenv("GITHUB_TOKEN")
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"

    response = requests.get(
         url,
        params={
        "per_page": 100,
        "sort": "updated",
        "type": "owner",
        },
         headers=headers,
        timeout=15,
)
    if response.status_code == 404:
        raise RuntimeError("GitHub user not found.")
    if response.status_code == 403:
        raise RuntimeError("GitHub API rate limit reached. Try again later.")
    if response.status_code >= 400:
        raise RuntimeError("Could not fetch this GitHub profile.")
    return response.json()


def summarize_repo(repo: dict[str, Any]) -> GitHubRepoSummary:
    topics = repo.get("topics") or []
    language = repo.get("language") or "Unknown"
    text = " ".join(
        [
            repo.get("name") or "",
            repo.get("description") or "",
            language,
            " ".join(topics),
        ]
    ).casefold()
    project_type = classify_project(text)
    summary = GitHubRepoSummary(
        name=repo.get("name") or "Untitled repository",
        description=repo.get("description") or "No description provided.",
        language=language,
        stars=int(repo.get("stargazers_count") or 0),
        forks=int(repo.get("forks_count") or 0),
        watchers=int(repo.get("watchers_count") or 0),
        open_issues=int(repo.get("open_issues_count") or 0),
        size_kb=int(repo.get("size") or 0),
        topics=topics,
        updated_at=repo.get("updated_at") or "",
        url=repo.get("html_url") or "",
        project_type=project_type,
        difficulty_level=repo_difficulty(language, project_type, int(repo.get("size") or 0), int(repo.get("stargazers_count") or 0)),
        has_license=bool(repo.get("license")),
        has_readme_signal=has_readme_signal(repo, topics),
        has_releases_signal=bool(repo.get("has_releases")),
    )
    summary.quality_score = repo_quality_score(summary)
    return summary


def classify_project(text: str) -> str:
    scores = []
    for category, keywords in PROJECT_CATEGORY_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in text)
        if score:
            scores.append((score, category))
    if scores:
        return sorted(scores, key=lambda item: (-item[0], item[1]))[0][1]
    return "General"


def count_languages(repos: list[GitHubRepoSummary]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for repo in repos:
        if repo.language and repo.language != "Unknown":
            counts[repo.language] = counts.get(repo.language, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))


def count_categories(repos: list[GitHubRepoSummary]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for repo in repos:
        counts[repo.project_type] = counts.get(repo.project_type, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))


def count_quality_distribution(repos: list[GitHubRepoSummary]) -> dict[str, int]:
    buckets = {"Excellent": 0, "Strong": 0, "Developing": 0, "Needs Work": 0}
    for repo in repos:
        if repo.quality_score >= 90:
            buckets["Excellent"] += 1
        elif repo.quality_score >= 75:
            buckets["Strong"] += 1
        elif repo.quality_score >= 55:
            buckets["Developing"] += 1
        else:
            buckets["Needs Work"] += 1
    return {key: value for key, value in buckets.items() if value}


def count_technology_stack(repos: list[GitHubRepoSummary]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for repo in repos:
        for skill in infer_repo_skills(repo):
            counts[skill] = counts.get(skill, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: item[1], reverse=True)[:12])


def extract_skills(repos: list[GitHubRepoSummary], language_counts: dict[str, int]) -> list[str]:
    skills = []
    for language in language_counts:
        skills.extend(LANGUAGE_TO_SKILLS.get(language, [language]))
    for repo in repos:
        skills.extend(infer_repo_skills(repo))
    return dedupe(skills)[:18]


def infer_repo_skills(repo: GitHubRepoSummary) -> list[str]:
    text = f"{repo.name} {repo.description} {repo.language} {' '.join(repo.topics)}".casefold()
    skills = []
    category_skills = {
        "AI / ML": ["Machine Learning", "Deep Learning", "Model Deployment", "NLP", "Computer Vision"],
        "Web Development": ["REST APIs", "Frontend Development", "Backend Development", "Software Architecture"],
        "Mobile": ["Mobile Development", "App Architecture"],
        "DevOps": ["CI/CD", "Infrastructure Automation", "Release Engineering"],
        "Cloud": ["Cloud Architecture", "Cloud Deployment", "Infrastructure as Code"],
        "Data Science": ["Data Analysis", "Statistics", "Data Visualization"],
        "Systems Programming": ["Operating Systems", "Kernel Development", "Memory Management", "Low-Level Programming"],
        "Embedded Systems": ["Firmware", "IoT", "Hardware Integration"],
        "Cybersecurity": ["Network Security", "Reverse Engineering", "Cryptography", "Incident Response"],
        "Blockchain": ["Smart Contracts", "Blockchain Development"],
        "Game Development": ["Game Development", "Interactive Systems"],
        "Desktop Applications": ["Desktop Application Development", "GUI Development"],
        "CLI Tools": ["Developer Tooling", "Command-Line Interfaces"],
        "Libraries": ["API Design", "Library Maintenance"],
        "Frameworks": ["Framework Design", "Developer Experience"],
    }
    skills.extend(category_skills.get(repo.project_type, []))
    keyword_skills = {
        "fastapi": "FastAPI",
        "django": "Django",
        "react": "React",
        "kubernetes": "Kubernetes",
        "docker": "Docker",
        "aws": "AWS",
        "azure": "Azure",
        "microservice": "Microservices",
        "distributed": "Distributed Systems",
        "compiler": "Compiler Toolchains",
        "kernel": "Kernel Development",
        "cryptography": "Cryptography",
        "nlp": "NLP",
        "vision": "Computer Vision",
    }
    for keyword, skill in keyword_skills.items():
        if keyword in text:
            skills.append(skill)
    return dedupe(skills)


def repo_quality_score(repo: GitHubRepoSummary) -> int:
    score = 12
    if repo.description and repo.description != "No description provided.":
        score += min(12, 5 + len(repo.description) // 22)
    if repo.topics:
        score += min(len(repo.topics), 6) * 2
    score += min(14, round(math.log10(repo.stars + 1) * 7))
    score += min(6, round(math.log10(repo.forks + 1) * 4))
    score += min(2, round(math.log10(repo.watchers + 1) * 2))
    score += max(0, 9 - min(repo.open_issues, 40) // 5)
    score += min(6, round(math.log10(repo.size_kb + 1) * 2)) if repo.size_kb else 0
    score += 4 if repo.has_readme_signal else 0
    score += 3 if repo.has_license else 0
    score += 2 if repo.has_releases_signal else 0
    score += min(14, LANGUAGE_COMPLEXITY.get(repo.language, 8))
    if repo.project_type != "General":
        score += 3
    if repo.updated_at:
        age = days_since(repo.updated_at)
        if age <= 30:
            score += 8
        elif age <= 180:
            score += 5
        elif age > 900:
            score -= 10
    score = calibrated_score("projects", score)
    if repo.stars < 10 and repo.forks < 3:
        score = min(score, 72)
    elif repo.stars < 100:
        score = min(score, 82)
    elif repo.stars < 1000:
        score = min(score, 90)
    elif repo.stars < 10000:
        score = min(score, 92)
    elif repo.stars < 50000:
        score = min(score, 94)
    if not repo.has_readme_signal:
        score = min(score, 88)
    if repo.updated_at and days_since(repo.updated_at) > 1200:
        score = min(score, 86)
    return score


def calculate_project_quality_score(repos: list[GitHubRepoSummary]) -> int:
    if not repos:
        return 0
    top_repos = sorted(repos, key=lambda repo: repo.quality_score, reverse=True)[:5]
    return calibrated_score("projects", sum(repo.quality_score for repo in top_repos) / len(top_repos))


def calculate_activity_level(repos: list[GitHubRepoSummary]) -> str:
    if not repos:
        return "No public activity"
    recent_count = sum(1 for repo in repos if repo.updated_at and days_since(repo.updated_at) <= 120)
    if recent_count >= 5:
        return "High"
    if recent_count >= 2:
        return "Medium"
    return "Low"


def calculate_github_score(
    repo_count: int,
    stars: int,
    forks: int,
    followers: int,
    language_count: int,
    category_count: int,
    ai_project_count: int,
    web_project_count: int,
    activity_level: str,
    project_quality_score: int,
    documentation_score: int,
    recent_ratio: float,
) -> int:
    score = 0
    score += min(8, round(repo_count / 5))
    score += min(17, round(math.log10(stars + 1) * 4.5))
    score += min(10, round(math.log10(forks + 1) * 3.5))
    score += min(12, round(math.log10(followers + 1) * 4))
    score += min(language_count, 8)
    score += min(category_count, 8)
    score += min(ai_project_count, 3) * 2
    score += min(web_project_count, 3)
    score += {"High": 8, "Medium": 5, "Low": 2}.get(activity_level, 0)
    score += round(project_quality_score * 0.25)
    score += round(documentation_score * 0.06)
    score += round(recent_ratio * 6)
    score = calibrated_score("github", score)
    if stars < 1000 and followers < 500:
        score = min(score, 78)
    elif stars < 10000 and followers < 3000:
        score = min(score, 88)
    elif stars < 50000 and followers < 10000:
        score = min(score, 90)
    elif stars < 100000 and followers < 50000:
        score = min(score, 94)
    return score


def portfolio_strength(score: int) -> str:
    if score >= 80:
        return "Strong"
    if score >= 55:
        return "Developing"
    if score >= 30:
        return "Early"
    return "Needs public proof of work"


def build_recommendations(
    summaries: list[GitHubRepoSummary],
    ai_project_count: int,
    web_project_count: int,
    activity_level: str,
    top_skills: list[str],
) -> list[str]:
    recommendations = []
    if ai_project_count == 0:
        recommendations.append("Build one production-level AI project with a clear README and deployed demo.")
    if web_project_count == 0:
        recommendations.append("Add one full-stack or API project to show product-building ability.")
    if activity_level != "High":
        recommendations.append("Update or publish projects consistently so recent activity is visible.")
    if summaries and any(repo.description == "No description provided." for repo in summaries[:5]):
        recommendations.append("Add descriptions and topics to your strongest repositories.")
    if not top_skills:
        recommendations.append("Use public repositories to demonstrate your strongest technical skills.")
    return recommendations[:4] or ["Your GitHub portfolio is strong. Add one polished flagship project to make it recruiter-ready."]


def infer_careers(category_counts: dict[str, int], top_skills: list[str], repos: list[GitHubRepoSummary]) -> list[dict[str, str]]:
    primary = strongest_category(repos) or next(iter(category_counts), "General")
    skill_text = " ".join(top_skills).casefold()
    top_skill_text = " ".join(top_skills[:6]).casefold()
    total_categories = max(1, sum(category_counts.values()))
    ai_share = category_counts.get("AI / ML", 0) / total_categories
    if primary == "AI / ML" or ai_share >= 0.35:
        primary = "AI / ML"
    elif primary == "Systems Programming" or any(term in top_skill_text for term in ["low-level programming", "kernel development", "memory management"]):
        primary = "Systems Programming"
    elif any(term in top_skill_text for term in ["react", "frontend architecture", "frontend engineering"]):
        primary = "Frontend Web"
    elif any(term in top_skill_text for term in ["backend development", "rest apis", "software architecture"]):
        primary = "Backend Web"
    mapping = {
        "Backend Web": [
            ("Backend Engineer", "Backend, automation, API, or service-oriented repositories show backend depth."),
            ("Software Engineer", "Your repositories show broad software-building and architecture signals."),
            ("Platform Engineer", "Automation and backend tooling can transfer into platform teams."),
        ],
        "Frontend Web": [
            ("Frontend Engineer", "React, frontend architecture, or browser-focused repositories show frontend depth."),
            ("Web Platform Engineer", "Your portfolio suggests strong web tooling and user-interface engineering ability."),
            ("Software Engineer", "Frontend projects still demonstrate broader product engineering strength."),
        ],
        "Systems Programming": [
            ("Systems Software Engineer", "Your repositories show low-level languages, systems concepts, or operating-system work."),
            ("Kernel Engineer", "Kernel, memory, runtime, or C/C++ signals indicate systems depth."),
            ("Platform Engineer", "Strong infrastructure or runtime projects transfer well to platform teams."),
        ],
        "AI / ML": [
            ("AI Engineer", "Machine learning, model, NLP, or computer-vision repositories show applied AI proof."),
            ("Machine Learning Engineer", "Your portfolio indicates model-building and deployment potential."),
            ("MLOps Engineer", "Production AI projects benefit from deployment and evaluation skills."),
        ],
        "Web Development": [
            ("Backend Engineer", "API, backend, and service repositories show product engineering ability."),
            ("Full Stack Engineer", "Frontend plus backend signals support end-to-end product work."),
            ("Software Engineer", "General software architecture and shipped projects map to software roles."),
        ],
        "Cloud": [
            ("Cloud Engineer", "Cloud, deployment, and infrastructure repositories show operations readiness."),
            ("DevOps Engineer", "CI/CD and automation skills map to DevOps teams."),
        ],
        "DevOps": [
            ("DevOps Engineer", "Automation, pipelines, and deployment projects indicate DevOps fit."),
            ("Site Reliability Engineer", "Reliability and operations tooling can support SRE paths."),
        ],
        "Cybersecurity": [
            ("Cybersecurity Analyst", "Security repositories show threat, defense, or assessment capability."),
            ("Security Engineer", "Security tooling and engineering signals support security engineering roles."),
        ],
        "Mobile": [
            ("Mobile Engineer", "Mobile repositories show app delivery and platform-specific experience."),
            ("Android/iOS Developer", "Native or cross-platform mobile work supports app roles."),
        ],
        "Libraries": [
            ("Open Source Maintainer", "Library projects show API design and maintenance skill."),
            ("Developer Tools Engineer", "Reusable packages indicate developer-experience thinking."),
        ],
    }
    careers = mapping.get(primary, [("Software Engineer", "Your public repositories show general software-building proof.")])
    if ai_share >= 0.2 and any("Machine Learning" in skill for skill in top_skills) and primary != "AI / ML":
        careers.append(("AI Engineer", "Some repositories include ML or data signals that could support an AI path."))
    return [{"career": career, "why": why} for career, why in careers[:4]]


def strongest_category(repos: list[GitHubRepoSummary]) -> str:
    scores: dict[str, float] = {}
    for repo in repos:
        impact = repo.quality_score + math.log10(repo.stars + 1) * 8 + math.log10(repo.forks + 1) * 5
        scores[repo.project_type] = scores.get(repo.project_type, 0) + impact
    if not scores:
        return "General"
    return sorted(scores.items(), key=lambda item: item[1], reverse=True)[0][0]


def portfolio_strengths_weaknesses(
    repos: list[GitHubRepoSummary],
    top_skills: list[str],
    category_counts: dict[str, int],
    activity_level: str,
) -> tuple[list[str], list[str]]:
    strengths = []
    weaknesses = []
    if repos:
        strengths.append(f"Strongest repository quality reaches {max(repo.quality_score for repo in repos)}%.")
    if len(category_counts) >= 3:
        strengths.append("Portfolio shows project diversity across multiple categories.")
    if top_skills:
        strengths.append("Inferred skills include " + ", ".join(top_skills[:4]) + ".")
    if activity_level == "High":
        strengths.append("Recent repository activity is visible.")
    if any(repo.description == "No description provided." for repo in repos[:8]):
        weaknesses.append("Some repositories need clearer descriptions.")
    if any(not repo.topics for repo in repos[:8]):
        weaknesses.append("Add GitHub topics to make project classification stronger.")
    if activity_level != "High":
        weaknesses.append("Recent activity is limited; refresh flagship repositories.")
    if repos and sum(repo.has_license for repo in repos) / len(repos) < 0.25:
        weaknesses.append("Most repositories do not show license metadata.")
    return strengths[:5], weaknesses[:5]


def repo_difficulty(language: str, project_type: str, size_kb: int, stars: int) -> str:
    complexity = LANGUAGE_COMPLEXITY.get(language, 8)
    if project_type in {"Systems Programming", "Cybersecurity", "Frameworks"}:
        complexity += 4
    if size_kb > 5000 or stars > 1000:
        complexity += 4
    if complexity >= 20:
        return "Advanced"
    if complexity >= 14:
        return "Intermediate"
    return "Beginner"


def has_readme_signal(repo: dict[str, Any], topics: list[str]) -> bool:
    text = " ".join([repo.get("name") or "", repo.get("description") or "", " ".join(topics)]).casefold()
    return bool(repo.get("description")) and (len(repo.get("description") or "") >= 28 or "readme" in text or bool(topics))


def average_documentation_score(repos: list[GitHubRepoSummary]) -> int:
    if not repos:
        return 0
    scores = [88 if repo.has_readme_signal and repo.description != "No description provided." else 45 if repo.description != "No description provided." else 10 for repo in repos]
    return calibrated_score("ats_readiness", sum(scores) / len(scores))


def recent_activity_ratio(repos: list[GitHubRepoSummary]) -> float:
    if not repos:
        return 0.0
    return sum(1 for repo in repos if repo.updated_at and days_since(repo.updated_at) <= 180) / len(repos)


def calculate_years_active(created_at: str) -> int:
    if not created_at:
        return 0
    return max(0, round(days_since(created_at) / 365))


def open_source_level(stars: int, forks: int, followers: int, quality: int) -> str:
    impact = math.log10(stars + 1) * 10 + math.log10(forks + 1) * 8 + math.log10(followers + 1) * 6 + quality * 0.2
    if impact >= 95:
        return "Exceptional"
    if impact >= 70:
        return "High"
    if impact >= 45:
        return "Moderate"
    if impact >= 20:
        return "Emerging"
    return "Early"


def days_since(iso_datetime: str) -> int:
    updated = datetime.fromisoformat(iso_datetime.replace("Z", "+00:00"))
    return (datetime.now(timezone.utc) - updated).days


def dedupe(items: list[str]) -> list[str]:
    seen = set()
    result = []
    for item in items:
        key = item.casefold()
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result
