"""
ROI Engine — time-adjusted return on AI spend.
Computes annualised ROI, not just a ratio.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class ROIResult:
    ratio: float           # business_value / cost
    annualised_roi: float  # projected annual return %
    payback_days: float    # days to break even
    confidence: str        # high / medium / low


class ROIEngine:

    def evaluate(
        self,
        cost: float,
        business_value: float,
        execution_duration_s: float = 1.0,
        confidence_signals: int = 1,
    ) -> ROIResult:

        if cost <= 0:
            return ROIResult(
                ratio=0.0,
                annualised_roi=0.0,
                payback_days=float("inf"),
                confidence="low",
            )

        ratio = round(business_value / cost, 4)

        # Annualise: extrapolate from one execution to a year of similar runs
        executions_per_year = (365 * 24 * 3600) / max(execution_duration_s, 1)
        annual_value = business_value * executions_per_year
        annual_cost  = cost * executions_per_year
        annualised_roi = round(
            (annual_value - annual_cost) / max(annual_cost, 0.0001) * 100, 2
        )

        payback_days = round(
            cost / max(business_value / 365, 0.0001), 2
        )

        confidence = (
            "high"   if confidence_signals >= 5  else
            "medium" if confidence_signals >= 2  else
            "low"
        )

        return ROIResult(
            ratio=ratio,
            annualised_roi=annualised_roi,
            payback_days=payback_days,
            confidence=confidence,
        )
