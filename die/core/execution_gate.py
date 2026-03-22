"""
die.core.execution_gate
========================
Component 4 of DIE — the final output.

Converts stability score + assumption flags into an execution decision:
    PASS        — execute unconditionally
    RESTRICTED  — execute only with guards (conditions listed)
    BLOCKED     — do not execute under any circumstances

This output feeds directly into ai_firewall_core.py as an upstream pre-filter.
If status is BLOCKED, ai_firewall_core never sees the request.

Integration point
-----------------
    # In ai_firewall_core.py or middleware.py:
    from die import DecisionIntegrityEngine, DecisionObject

    die = DecisionIntegrityEngine()
    result = die.evaluate(decision_object)

    if result.status == ExecutionStatus.BLOCKED:
        return {"allowed": False, "reason": result.reason}

    if result.status == ExecutionStatus.RESTRICTED:
        # enforce result.required_conditions before proceeding

Usage
-----
    from die.core.execution_gate import ExecutionGate, ExecutionStatus

    gate = ExecutionGate()
    result = gate.decide(score, extraction_result)
    print(result.status, result.required_conditions)
"""

from dataclasses import dataclass, field
from enum import Enum
from die.core.stability_scorer import StabilityScore
from die.core.assumption_extractor import ExtractionResult


class ExecutionStatus(str, Enum):
    PASS       = "PASS"
    RESTRICTED = "RESTRICTED"
    BLOCKED    = "BLOCKED"


@dataclass
class DIEResult:
    status:              ExecutionStatus
    reason:              str
    required_conditions: list[str] = field(default_factory=list)
    decision_score:      float = 0.0
    decision_type:       str = ""
    failure_modes:       list[str] = field(default_factory=list)
    assumption_flags:    list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "status":              self.status.value,
            "reason":              self.reason,
            "required_conditions": self.required_conditions,
            "decision_score":      self.decision_score,
            "decision_type":       self.decision_type,
            "failure_modes":       self.failure_modes,
            "assumption_flags":    self.assumption_flags,
        }

    @property
    def allowed(self) -> bool:
        return self.status != ExecutionStatus.BLOCKED


class ExecutionGate:

    # Thresholds — tune these as ground truth accumulates
    PASS_THRESHOLD       = 0.80
    RESTRICTED_THRESHOLD = 0.50

    def decide(
        self,
        score:      StabilityScore,
        extraction: ExtractionResult,
    ) -> DIEResult:
        """
        Emit final execution decision based on score and assumption flags.
        """

        # Hard block: critical assumption flags always block
        critical_flags = [
            f for f in extraction.flags
            if "no constraints" in f or "manual review" in f
        ]
        if critical_flags:
            return DIEResult(
                status=ExecutionStatus.BLOCKED,
                reason="critical assumption flags — decision not structurally sound",
                assumption_flags=extraction.flags,
                decision_score=score.value,
                decision_type=score.decision_type,
                failure_modes=score.failure_modes,
            )

        # Score-based gate
        if score.value >= self.PASS_THRESHOLD:
            return DIEResult(
                status=ExecutionStatus.PASS,
                reason="decision is stable across context variations",
                decision_score=score.value,
                decision_type=score.decision_type,
            )

        if score.value >= self.RESTRICTED_THRESHOLD:
            return DIEResult(
                status=ExecutionStatus.RESTRICTED,
                reason="decision holds only under specific conditions",
                required_conditions=score.safe_scope,
                decision_score=score.value,
                decision_type=score.decision_type,
                failure_modes=score.failure_modes,
                assumption_flags=extraction.flags,
            )

        return DIEResult(
            status=ExecutionStatus.BLOCKED,
            reason="decision is too fragile — fails under too many context variations",
            decision_score=score.value,
            decision_type=score.decision_type,
            failure_modes=score.failure_modes,
            assumption_flags=extraction.flags,
        )
