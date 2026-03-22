"""
die.core.stability_scorer
==========================
Component 3 of DIE.

Converts stress test results into a numeric stability score (0.0–1.0)
and classifies the decision as global / conditional / local.

Score interpretation
--------------------
    0.8 – 1.0  : stable    → likely PASS
    0.5 – 0.79 : fragile   → likely RESTRICTED (needs guards)
    0.0 – 0.49 : unstable  → likely BLOCKED

Decision types
--------------
    global      — holds across all tested variations, safe everywhere
    conditional — holds in some contexts but not others, needs guards
    local       — only safe in a narrow set of conditions, very fragile

Usage
-----
    from die.core.stability_scorer import StabilityScorer

    scorer = StabilityScorer()
    score = scorer.score(stress_results, decision)
    print(score.value, score.decision_type, score.failure_modes)
"""

from dataclasses import dataclass, field
from die.core.stress_tester import ScenarioResult
from die.core.decision_object import DecisionObject


@dataclass
class StabilityScore:
    value:         float                 # 0.0 – 1.0
    decision_type: str                   # global | conditional | local
    failure_modes: list[str] = field(default_factory=list)
    safe_scope:    list[str] = field(default_factory=list)
    confidence:    str = "medium"        # low | medium | high

    def to_dict(self) -> dict:
        return {
            "decision_score": round(self.value, 2),
            "decision_type":  self.decision_type,
            "failure_modes":  self.failure_modes,
            "safe_scope":     self.safe_scope,
            "confidence":     self.confidence,
        }


class StabilityScorer:

    def score(
        self,
        stress_results: list[ScenarioResult],
        decision: DecisionObject,
    ) -> StabilityScore:
        """
        Compute stability score from stress test results.
        """
        if not stress_results:
            return StabilityScore(
                value=0.0,
                decision_type="local",
                failure_modes=["no stress results — cannot assess stability"],
                confidence="low",
            )

        total   = len(stress_results)
        passing = sum(1 for r in stress_results if r.holds)
        ratio   = passing / total

        failure_modes = [
            r.failure_reason
            for r in stress_results
            if not r.holds and r.failure_reason
        ]

        # Derive safe scope from passing scenarios
        safe_scope = [
            f"{list(r.scenario.keys())[0]} = {list(r.scenario.values())[0]}"
            for r in stress_results
            if r.holds
        ]

        # Classify
        if ratio >= 0.8:
            decision_type = "global"
            confidence    = "high"
        elif ratio >= 0.5:
            decision_type = "conditional"
            confidence    = "medium"
        else:
            decision_type = "local"
            confidence    = "low"

        return StabilityScore(
            value=round(ratio, 2),
            decision_type=decision_type,
            failure_modes=list(set(failure_modes)),
            safe_scope=safe_scope[:5],   # top 5 safe conditions
            confidence=confidence,
        )
