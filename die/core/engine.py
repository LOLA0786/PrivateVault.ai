"""
die.core.engine
================
DecisionIntegrityEngine — the single entry point for DIE.

Orchestrates the full pipeline:
    DecisionObject
        → AssumptionExtractor
        → StressTester
        → StabilityScorer
        → ExecutionGate
        → DIEResult

This is the ONLY class external code should instantiate.
All components are internal implementation details.

Usage
-----
    from die import DecisionIntegrityEngine, DecisionObject

    engine = DecisionIntegrityEngine()

    decision = DecisionObject(
        action="offer_discount",
        goal="increase_conversion",
        context={"user_type": "new_customer", "cart_value": 120},
        constraints={"max_discount": 20, "margin_floor": 15},
    )

    result = engine.evaluate(decision)
    print(result.status)       # PASS | RESTRICTED | BLOCKED
    print(result.to_dict())    # full JSON-serialisable output
"""

import logging
from die.core.decision_object     import DecisionObject
from die.core.assumption_extractor import AssumptionExtractor
from die.core.stress_tester       import StressTester
from die.core.stability_scorer    import StabilityScorer
from die.core.execution_gate      import ExecutionGate, DIEResult

logger = logging.getLogger(__name__)


class DecisionIntegrityEngine:
    """
    Pre-execution decision correctness validator.
    Instantiate once and reuse — all components are stateless.
    """

    def __init__(self) -> None:
        self._extractor = AssumptionExtractor()
        self._tester    = StressTester()
        self._scorer    = StabilityScorer()
        self._gate      = ExecutionGate()

    def evaluate(self, decision: DecisionObject) -> DIEResult:
        """
        Full DIE pipeline evaluation.
        Returns DIEResult with status PASS / RESTRICTED / BLOCKED.
        """

        # 0. Validate the decision object itself
        errors = decision.validate()
        if errors:
            from die.core.execution_gate import ExecutionStatus
            return DIEResult(
                status=ExecutionStatus.BLOCKED,
                reason=f"malformed decision object: {'; '.join(errors)}",
            )

        logger.debug("DIE: evaluating action='%s'", decision.action)

        # 1. Extract assumptions
        extraction = self._extractor.extract(decision)
        logger.debug("DIE: extracted %d assumptions, %d flags",
                     len(extraction.assumptions), len(extraction.flags))

        # 2. Stress test
        stress_results = self._tester.run(decision)
        logger.debug("DIE: ran %d stress scenarios", len(stress_results))

        # 3. Score stability
        score = self._scorer.score(stress_results, decision)
        logger.debug("DIE: stability score=%.2f type=%s",
                     score.value, score.decision_type)

        # 4. Gate
        result = self._gate.decide(score, extraction)
        logger.info(
            "DIE: action='%s' → %s (score=%.2f)",
            decision.action, result.status.value, result.decision_score,
        )

        return result
