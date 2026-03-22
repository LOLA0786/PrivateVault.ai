"""
die.core.assumption_extractor
==============================
Component 1 of DIE.

Forces implicit logic in a DecisionObject into explicit, auditable assumptions.
If assumptions are vague or unjustified, they are flagged immediately.
A decision with unresolved flags does not proceed to stress testing.

Design principle
----------------
Every agent decision is built on assumptions about the world.
Most of those assumptions are never stated.
This component makes them stated — so they can be tested.

Example
-------
    Decision: offer_discount to new_customer
    Extracted assumptions:
        - User is price-sensitive
        - Discount improves conversion
        - Margin can absorb the discount
        - Market competition justifies the incentive

Usage
-----
    from die.core.assumption_extractor import AssumptionExtractor
    from die.core.decision_object import DecisionObject

    extractor = AssumptionExtractor()
    result = extractor.extract(decision)
    if result.has_flags:
        print(result.flags)  # vague or missing assumptions
"""

from dataclasses import dataclass, field
from die.core.decision_object import DecisionObject


@dataclass
class ExtractionResult:
    assumptions: list[str] = field(default_factory=list)
    flags:       list[str] = field(default_factory=list)

    @property
    def has_flags(self) -> bool:
        return len(self.flags) > 0

    def to_dict(self) -> dict:
        return {
            "assumptions": self.assumptions,
            "flags":       self.flags,
            "has_flags":   self.has_flags,
        }


class AssumptionExtractor:
    """
    Rule-based assumption extractor (Phase 1).
    LLM-backed extraction is Phase 2 — plug in via override of extract().
    """

    # Maps action keywords → assumptions that must hold
    _ACTION_ASSUMPTIONS: dict[str, list[str]] = {
        "discount":    [
            "user is price-sensitive",
            "discount improves conversion",
            "margin can absorb discount",
            "market conditions justify incentive",
        ],
        "payment":     [
            "recipient account is verified",
            "amount is within authorised limits",
            "transaction is not a duplicate",
            "user has sufficient balance",
        ],
        "transfer":    [
            "source identity is authenticated",
            "destination is not on sanctions list",
            "transfer amount is within daily limit",
            "no active fraud flag on account",
        ],
        "delete":      [
            "data is not subject to retention policy",
            "user has delete permission",
            "deletion is irreversible — confirmed",
        ],
        "approve":     [
            "approval authority is within scope",
            "decision criteria are met",
            "no conflict of interest exists",
        ],
    }

    def extract(self, decision: DecisionObject) -> ExtractionResult:
        """
        Extract assumptions from a DecisionObject.
        Returns ExtractionResult with assumptions and any flags.
        """
        assumptions: list[str] = []
        flags:       list[str] = []

        # Match action against known assumption sets
        matched = False
        for keyword, known_assumptions in self._ACTION_ASSUMPTIONS.items():
            if keyword in decision.action.lower():
                assumptions.extend(known_assumptions)
                matched = True

        if not matched:
            flags.append(
                f"no assumption template for action '{decision.action}' — "
                "manual review required"
            )

        # Flag if context is suspiciously thin
        if len(decision.context) < 2:
            flags.append(
                "context has fewer than 2 fields — "
                "decision may be under-specified"
            )

        # Flag if no constraints at all
        if not decision.constraints:
            flags.append(
                "no constraints defined — "
                "decision has no enforceable limits"
            )

        return ExtractionResult(assumptions=assumptions, flags=flags)
