from typing import Iterable

from pv_runtime_v2.consensus.leader_state import (
    LeaderState,
)


class ByzantineQuorum:

    def available(
        self,
        leaders: Iterable[
            LeaderState
        ],
    ) -> bool:

        leaders = list(
            leaders
        )

        total = len(
            leaders
        )

        healthy = sum(
            1
            for l in leaders
            if l.healthy
        )

        return (
            healthy
            > (2 * total / 3)
        )
