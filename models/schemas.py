from pydantic import BaseModel
from typing import List, Dict

class CriteriaMatch(BaseModel):
    evidence: str
    explanation: str
    source: str
    confidence: float

class AssessmentResult(BaseModel):
    criteria_matches: Dict[str, List[CriteriaMatch]]
    rating: str
    unmet_criteria: List[str]