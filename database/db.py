from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

from models.user import UserProfile


DB_PATH = Path(__file__).resolve().parent / "users.db"


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                name TEXT NOT NULL,
                career_goal TEXT NOT NULL,
                target_country TEXT NOT NULL,
                readiness_score INTEGER NOT NULL,
                success_probability INTEGER NOT NULL,
                profile_json TEXT NOT NULL,
                analysis_json TEXT NOT NULL
            )
            """
        )


def save_profile(
    profile: UserProfile,
    analysis: dict[str, Any],
    success_probability: int,
) -> None:
    init_db()
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO profiles (
                created_at,
                name,
                career_goal,
                target_country,
                readiness_score,
                success_probability,
                profile_json,
                analysis_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.utcnow().isoformat(timespec="seconds"),
                profile.name,
                profile.career_goal,
                profile.target_country,
                analysis["score"],
                success_probability,
                json.dumps(profile.__dict__),
                json.dumps(analysis),
            ),
        )


def recent_profiles(limit: int = 5) -> list[dict[str, Any]]:
    init_db()
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT created_at, name, career_goal, target_country, readiness_score, success_probability
            FROM profiles
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]
