from typing import Dict

from pv_runtime_v2.trust_fabric.trust_state import (
    TrustState,
)


class TrustCache:

    def __init__(self):

        self._cache: Dict[
            str,
            TrustState
        ] = {}

    def put(
        self,
        state: TrustState,
    ) -> None:

        self._cache[
            state.agent_id
        ] = state

    def get(
        self,
        agent_id: str,
    ) -> TrustState | None:

        return self._cache.get(
            agent_id
        )

    def size(
        self,
    ) -> int:

        return len(
            self._cache
        )
