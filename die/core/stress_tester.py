"""
die.core.stress_tester
=======================
Component 2 of DIE.

Simulates context variations and evaluates whether the decision still holds,
becomes harmful, or violates constraints under each variation.

This is the core differentiator of DIE:
    A decision that looks valid in one context may be harmful in another.
    Stress testing surfaces fragility before execution.

Stress scenarios are generated from:
    1. Context field inversions (flip values to edge cases)
    2. Constraint boundary probes (what if a limit is just breached?)
    3. Domain-specific risk scenarios (fraud, low demand, edge users)

Usage
-----
    from die.core.stress_tester import StressTester
    from die.core.decision_object import DecisionObject

    tester = StressTester()
    results = tester.run(decision)
    failures = [r for r in results if not r.holds]
"""

from dataclasses import dataclass, field
from typing import Any
from die.core.decision_object import DecisionObject


@dataclass
class ScenarioResult:
    scenario:       dict[str, Any]
    holds:          bool
    failure_reason: str = ""

    def to_dict(self) -> dict:
        return {
            "scenario":       self.scenario,
            "holds":          self.holds,
            "failure_reason": self.failure_reason,
        }


class StressTester:
    """
    Generates synthetic context variations and tests the decision against each.
    Phase 1: rule-based scenario generation.
    Phase 2: LLM-generated adversarial scenarios.
    """

    # Domain-specific risk scenarios to always probe
    _RISK_SCENARIOS: list[dict[str, Any]] = [
        {"fraud_risk":   "high"},
        {"user_type":    "loyal_customer"},
        {"market":       "low_demand"},
        {"cart_value":   5},
        {"account_age":  "1_day"},
    ]

    def run(self, decision: DecisionObject) -> list[ScenarioResult]:
        """
        Run all stress scenarios against the decision.
        Returns list of ScenarioResult — one per scenario tested.
        """
        results: list[ScenarioResult] = []

        # Probe constraint boundaries
        for key, limit in decision.constraints.items():
            if isinstance(limit, (int, float)):
                # Test just below the limit
                scenario = {key: limit * 0.1}
                result = self._evaluate(decision, scenario)
                results.append(result)

        # Run domain risk scenarios
        for scenario in self._RISK_SCENARIOS:
            result = self._evaluate(decision, scenario)
            results.append(result)

        return results

    def _evaluate(
        self, decision: DecisionObject, scenario: dict[str, Any]
    ) -> ScenarioResult:
        """
        Evaluate whether the decision holds under a given context variation.
        Merges scenario into context and checks against constraints.
        """
        merged_context = {**decision.context, **scenario}

        # Fraud risk always blocks
        if merged_context.get("fraud_risk") == "high":
            return ScenarioResult(
                scenario=scenario,
                holds=False,
                failure_reason="decision unsafe under high fraud risk",
            )

        # Check numeric constraint boundaries
        for constraint_key, limit in decision.constraints.items():
            if isinstance(limit, (int, float)):
                context_val = merged_context.get(constraint_key)
                if isinstance(context_val, (int, float)) and context_val < limit * 0.2:
                    return ScenarioResult(
                        scenario=scenario,
                        holds=False,
                        failure_reason=(
                            f"{constraint_key}={context_val} breaches "
                            f"minimum threshold ({limit * 0.2:.1f})"
                        ),
                    )

        return ScenarioResult(scenario=scenario, holds=True)
