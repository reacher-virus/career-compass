from __future__ import annotations

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query
from services.country_intelligence import (
    SUPPORTED_COUNTRIES,
    CountryCareerIntelligence,
    get_country_career_intelligence,
)
from services.career_engine import load_careers

router = APIRouter(prefix="/api/countries", tags=["Countries"])

COUNTRY_ALIASES = {
    "united states": "USA",
    "united states of america": "USA",
    "us": "USA",
    "uk": "United Kingdom",
    "britain": "United Kingdom",
    "great britain": "United Kingdom",
    "uae": "UAE",
    "united arab emirates": "UAE",
    "south korea": "South Korea",
    "korea": "South Korea",
}


def normalize_country(name: str) -> str:
    cleaned = (name or "").strip()
    alias = COUNTRY_ALIASES.get(cleaned.casefold())
    if alias:
        return alias
    for c in SUPPORTED_COUNTRIES:
        if c.casefold() == cleaned.casefold():
            return c
    return cleaned


@router.get("")
def get_countries() -> Dict[str, Any]:
    return {
        "countries": SUPPORTED_COUNTRIES,
        "total": len(SUPPORTED_COUNTRIES),
    }


@router.get("/intelligence")
def get_country_intelligence(
    country: str = Query(..., description="Country name"),
    career: str = Query("Software Engineer", description="Target career name"),
) -> Dict[str, Any]:
    normalized_c = normalize_country(country)
    if normalized_c not in SUPPORTED_COUNTRIES:
        # Fallback to USA or India
        normalized_c = "USA" if "state" in country.casefold() or "us" in country.casefold() else "India"
    
    careers = load_careers()
    career_data = careers.get(career, {})
    intel: CountryCareerIntelligence = get_country_career_intelligence(career, normalized_c, career_data)
    return intel.__dict__
