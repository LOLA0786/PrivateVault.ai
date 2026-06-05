"""
Economics Score — composite score for a single execution.
Weighted aggregate of success, trust, waste, and ROI tier.
"""
from dataclasses import dataclass


@dataclass
class EconomicsScoreResult:
    score: float
    grade: str     # A / B / C / D / F
    breakdown: dict


class EconomicsScore:

    WEIGHTS = {
        "success": 0.35,
        "trust":   0.30,
        "waste":   0.20,   # inverted: (100 - waste)
        "roi":     0.15,   # capped at 100
    }

    def calculate(
        self,
        success: float,
        trust:   float,
        waste:   float,
        roi_ratio: float = 1.0,
    ) -> EconomicsScoreResult:

        roi_score = min(roi_ratio * 20, 100)   # ratio of 5 = perfect score

        weighted = (
            success              * self.WEIGHTS["success"] +
            trust                * self.WEIGHTS["trust"]   +
            (100 - waste)        * self.WEIGHTS["waste"]   +
            roi_score            * self.WEIGHTS["roi"]
        )

        score = round(max(min(weighted, 100), 0), 2)

        grade = (
            "A" if score >= 90 else
            "B" if score >= 75 else
            "C" if score >= 60 else
            "D" if score >= 40 else
            "F"
        )

        breakdown = {
            "success_contribution": round(success * self.WEIGHTS["success"], 2),
            "trust_contribution":   round(trust   * self.WEIGHTS["trust"],   2),
            "waste_contribution":   round((100 - waste) * self.WEIGHTS["waste"], 2),
            "roi_contribution":     round(roi_score * self.WEIGHTS["roi"],    2),
        }

        return EconomicsScoreResult(score=score, grade=grade, breakdown=breakdown)
