"""
Trust Engine — execution-level trust scoring with history and decay.
NOT the same as the agent identity trust engine in trust_store.py.
This measures: did this execution behave as expected economically?
"""
from dataclasses import dataclass
from typing import Optional
import math


@dataclass
class TrustResult:
    score: float           # 0–100
    drift_flag: bool       # True if score deviates >20pts from baseline
    decay_applied: float   # penalty from time since last execution


class EconTrustEngine:
    """
    Economic trust: how reliably does this agent deliver
    expected outcomes at expected cost?
    """

    DECAY_HALF_LIFE_HOURS = 24.0

    def evaluate(
        self,
        outcome: dict,
        historical_success_rate: float = 1.0,   # 0–1
        historical_avg_cost:     float = 0.0,
        current_cost:            float = 0.0,
        hours_since_last_run:    float = 0.0,
        baseline_trust:          float = 80.0,
    ) -> TrustResult:

        base = 95.0 if outcome.get("success") else 40.0

        # History adjustment: pull toward observed reliability
        history_adjustment = (historical_success_rate - 0.5) * 20
        base = max(min(base + history_adjustment, 100), 0)

        # Cost anomaly penalty: current cost much higher than historical?
        cost_penalty = 0.0
        if historical_avg_cost > 0 and current_cost > 0:
            cost_ratio = current_cost / historical_avg_cost
            if cost_ratio > 1.5:
                cost_penalty = min((cost_ratio - 1.5) * 15, 20)

        # Temporal decay: stale agents are less trusted
        decay = 0.0
        if hours_since_last_run > 0:
            decay = base * (
                1 - math.exp(
                    -0.693 * hours_since_last_run / self.DECAY_HALF_LIFE_HOURS
                )
            ) * 0.2   # cap decay contribution at 20% of base

        final_score = round(max(base - cost_penalty - decay, 0), 2)

        drift_flag = abs(final_score - baseline_trust) > 20

        return TrustResult(
            score=final_score,
            drift_flag=drift_flag,
            decay_applied=round(decay, 2),
        )


# Backwards-compatible alias used by __init__.py
class TrustEngine(EconTrustEngine):
    def evaluate(self, outcome: dict, **kwargs) -> TrustResult:
        return super().evaluate(outcome, **kwargs)
