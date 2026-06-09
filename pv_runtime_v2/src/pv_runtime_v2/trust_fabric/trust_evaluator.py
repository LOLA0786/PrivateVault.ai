from .trust_state import TrustState


class TrustEvaluator:

    def evaluate(
        self,
        trust_state: TrustState
    ) -> float:

        return max(
            0.0,
            min(
                1.0,
                trust_state.trust_score
            )
        )
