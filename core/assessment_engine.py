from models.schemas import AssessmentResult
from config.settings import settings

from typing import Dict, List

class AssessmentEngine:
    def __init__(self, rag_manager):
        self.rag_manager = rag_manager

    def assess_cv(self, cv_text: str) -> AssessmentResult:
        analysis = self.rag_manager.analyze_text(cv_text)
        return AssessmentResult(
            criteria_matches=analysis['criteria_matches'],
            rating=self._calculate_rating(analysis),
            unmet_criteria=self._identify_unmet_criteria(analysis)
        )

    def _calculate_rating(self, analysis: Dict) -> str:
        good_criteria_count = 0
        for criterion, matches in analysis['criteria_matches'].items():
            good_matches = [m for m in matches if m['confidence'] >= 0.6]
            if good_matches:
                good_criteria_count += 1

        if good_criteria_count >= 5:
            return "high"
        elif good_criteria_count >= 3:
            return "medium"
        return "low"

    def _identify_unmet_criteria(self, analysis: dict) -> List[str]:
        return [
            criterion for criterion in settings.CRITERIA
            if not analysis['criteria_matches'].get(criterion)
        ]