"""
Success Engine — graded task success, not binary.
Considers partial completions, error severity, and SLA adherence.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class SuccessResult:
    score: float           # 0–100
    tier: str              # full / partial / failed
    sla_met: bool
    error_penalty: float


class SuccessEngine:

    SLA_DEFAULTS = {
        "latency_ms": 2000,
        "cost_usd":   0.10,
    }

    def evaluate(
        self,
        outcome: dict,
        latency_ms: float = 0.0,
        cost_usd:   float = 0.0,
        sla_overrides: Optional[dict] = None,
    ) -> SuccessResult:

        sla = {**self.SLA_DEFAULTS, **(sla_overrides or {})}

        base_success = outcome.get("success", False)
        partial      = outcome.get("partial", False)
        error_code   = outcome.get("error_code", None)

        # Base score
        if base_success:
            score = 100.0
        elif partial:
            score = 50.0
        else:
            score = 0.0

        # SLA penalties
        latency_penalty = 0.0
        if latency_ms > sla["latency_ms"]:
            overrun_ratio   = (latency_ms - sla["latency_ms"]) / sla["latency_ms"]
            latency_penalty = min(overrun_ratio * 15, 20)

        cost_penalty = 0.0
        if cost_usd > sla["cost_usd"]:
            cost_overrun  = (cost_usd - sla["cost_usd"]) / sla["cost_usd"]
            cost_penalty  = min(cost_overrun * 10, 15)

        error_penalty = 0.0
        if error_code:
            severity_map = {"critical": 30, "high": 20, "medium": 10, "low": 5}
            error_penalty = severity_map.get(
                outcome.get("error_severity", "medium"), 10
            )

        total_penalty = latency_penalty + cost_penalty + error_penalty
        final_score   = round(max(score - total_penalty, 0), 2)

        sla_met = (latency_ms <= sla["latency_ms"]) and (cost_usd <= sla["cost_usd"])

        tier = (
            "full"    if final_score >= 90 else
            "partial" if final_score >= 40 else
            "failed"
        )

        return SuccessResult(
            score=final_score,
            tier=tier,
            sla_met=sla_met,
            error_penalty=round(error_penalty, 2),
        )
