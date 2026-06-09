from pv_runtime_v2.trust_fabric.trust_state import (
    TrustState,
)

from pv_runtime_v2.trust_fabric.capability_token import (
    CapabilityToken,
)


class LocalEnforcer:

    MINIMUM_TRUST_SCORE = 0.75

    def authorize(
        self,
        trust_state: TrustState,
        capability_token: CapabilityToken,
        requested_capability: str,
    ) -> bool:

        if trust_state.is_quarantined:
            return False

        if (
            trust_state.trust_score
            < self.MINIMUM_TRUST_SCORE
        ):
            return False

        if (
            requested_capability
            not in capability_token.capabilities
        ):
            return False

        return True
