"""
Loop Governor.

Makes runtime decisions about whether an autonomous loop
may continue execution.
"""

from dataclasses import dataclass

from pv_runtime.loop.models import LoopContext


@dataclass(frozen=True, slots=True)
class GovernorDecision:

    allowed: bool

    reason: str

    action: str
    # CONTINUE
    # PAUSE
    # APPROVAL
    # TERMINATE


class LoopGovernor:

    MAX_WASTE = 80

    MIN_HEALTH = 50

    def evaluate(
        self,
        loop: LoopContext,
    ) -> GovernorDecision:

        if loop.iteration >= loop.max_iterations:

            return GovernorDecision(
                False,
                "MAX_ITERATIONS",
                "TERMINATE",
            )

        waste = 0

        if loop.economics.context_bytes > 0:

            waste = (
                loop.economics.wasted_bytes
                /
                loop.economics.context_bytes
            ) * 100

        if waste >= self.MAX_WASTE:

            return GovernorDecision(
                False,
                "CONTEXT_WASTE",
                "PAUSE",
            )

        if loop.health.score < self.MIN_HEALTH:

            return GovernorDecision(
                False,
                "LOW_HEALTH",
                "PAUSE",
            )

        if loop.health.drift_detected:

            return GovernorDecision(
                False,
                "DRIFT_DETECTED",
                "APPROVAL",
            )

        return GovernorDecision(
            True,
            "OK",
            "CONTINUE",
        )
