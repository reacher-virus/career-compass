import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_all():
    print("Testing /api/health...")
    r = client.get("/api/health")
    assert r.status_code == 200, f"Health failed: {r.text}"
    print("Health OK:", r.json())

    print("Testing /api/careers...")
    r = client.get("/api/careers")
    assert r.status_code == 200
    data = r.json()
    print(f"Careers count: {data['total_careers']}, domains: {len(data['domains'])}")

    print("Testing /api/countries...")
    r = client.get("/api/countries")
    assert r.status_code == 200
    print(f"Countries count: {r.json()['total']}")

    print("Testing /api/countries/intelligence...")
    r = client.get("/api/countries/intelligence?country=United%20States&career=AI%20Engineer")
    assert r.status_code == 200
    print("Country intel currency:", r.json().get("currency"))

    print("Testing /api/mentor/questions...")
    r = client.get("/api/mentor/questions")
    assert r.status_code == 200
    print("Questions count:", r.json().get("total_questions"))

    print("Testing /api/analysis...")
    payload = {
        "profile": {
            "name": "Alex Smith",
            "degree": "B.Tech Computer Science",
            "branch": "Computer Science",
            "current_year": "3rd Year",
            "gpa": 8.5,
            "skills": ["Python", "FastAPI", "React", "Docker", "Machine Learning"],
            "projects": ["Built an AI Career Coach using LLMs and React", "Fullstack Ecommerce in Python"],
            "certifications": ["AWS Certified Cloud Practitioner"],
            "internships": ["Software Engineering Intern at Tech Corp"],
            "languages": ["English", "Spanish"],
            "achievements": ["1st Place Hackathon Winner 2025"],
            "weekly_study_hours": 12,
            "career_goal": "AI Engineer",
            "target_country": "United States"
        }
    }
    r = client.post("/api/analysis", json=payload)
    assert r.status_code == 200, f"Analysis failed: {r.text}"
    res = r.json()
    print("Analysis success! Readiness score:", res["readiness"]["score"], "Probability:", res["success_probability"])
    print("Digital twin stages:", len(res["digital_twin"]))
    print("Roadmap items:", len(res["roadmap"]))

    print("Testing /api/mentor/chat...")
    chat_payload = {
        "question": "What should I focus on next?",
        "context": {
            "career_goal": "AI Engineer",
            "readiness_score": 80,
            "missing_skills": ["MLOps", "PyTorch"],
            "matched_skills": ["Python", "Docker"]
        },
        "history": []
    }
    r = client.post("/api/mentor/chat", json=chat_payload)
    assert r.status_code == 200, f"Mentor chat failed: {r.text}"
    print("Mentor chat reply length:", len(r.json()["answer"]))

    print("Testing /api/reports/pdf...")
    pdf_payload = {
        "generated_at": "2026-08-31T02:20:00",
        "profile": {
            "name": "Alex Smith",
            "career_goal": "AI Engineer",
            "target_country": "USA"
        },
        "readiness": {
            "score": 80,
            "matched_skills": ["Python", "FastAPI"],
            "missing_skills": ["MLOps"]
        },
        "success_probability": 72,
        "country_intelligence": {
            "currency": "USD",
            "average_salary": "$150k"
        }
    }
    r = client.post("/api/reports/pdf", json=pdf_payload)
    assert r.status_code == 200, f"PDF report failed: {r.text}"
    assert len(r.content) > 1000, "PDF content too small"
    print("PDF generated successfully! Size bytes:", len(r.content))

    print("Testing /api/profiles/recent...")
    r = client.get("/api/profiles/recent")
    assert r.status_code == 200
    print("Recent profiles count:", len(r.json()))

    print("ALL API TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_all()
