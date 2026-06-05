"""
Savings Estimator — projects savings from applying optimizations.
Works from OptimizationEngine output, not from pre-known costs.
"""
from dataclasses import dataclass
from typing import List


@dataclass
class SavingsReport:
    current_cost:           float
    projected_cost:         float
    total_savings:          float
    savings_percent:        float
    annualised_savings_usd: float
    top_lever:              str


class SavingsEstimator:

    def estimate(
        self,
        current_cost:    float,
        suggestions:     list,     # List[OptimizationSuggestion]
        executions_per_day: float = 1000.0,
    ) -> SavingsReport:

        if not suggestions:
            return SavingsReport(
                current_cost=current_cost,
                projected_cost=current_cost,
                total_savings=0.0,
                savings_percent=0.0,
                annualised_savings_usd=0.0,
                top_lever="none",
            )

        total_savings_per_exec = sum(
            s.estimated_savings_usd for s in suggestions
        )

        projected = max(current_cost - total_savings_per_exec, 0)
        savings_pct = round(
            total_savings_per_exec / max(current_cost, 0.0001) * 100, 2
        )

        annualised = round(
            total_savings_per_exec * executions_per_day * 365, 2
        )

        top_lever = max(
            suggestions, key=lambda s: s.estimated_savings_usd
        ).category

        return SavingsReport(
            current_cost=round(current_cost, 6),
            projected_cost=round(projected, 6),
            total_savings=round(total_savings_per_exec, 6),
            savings_percent=savings_pct,
            annualised_savings_usd=annualised,
            top_lever=top_lever,
        )
