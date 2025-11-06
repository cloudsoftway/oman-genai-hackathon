
from typing import Any, Dict, List
from pydantic import BaseModel

# ------------------------------------------------------------
# Pydantic models
# ------------------------------------------------------------
class CVData(BaseModel):
    id: str
    source_file: str
    role: str
    personal_info: Dict[str, Any]
    summary: str
    skills: Dict[str, Any]
    experience: List[Dict[str, Any]]
    education: List[Dict[str, Any]]
    certifications: List[Any]
    projects: List[Any]
    languages: List[Any]
    side_notes: str


class CVEligibilityResult(BaseModel):
    decision: str
    match_score: float
    missing_must_have_skills: List[str]
    missing_education: bool
    experience_gap_years: float
    notes: str

