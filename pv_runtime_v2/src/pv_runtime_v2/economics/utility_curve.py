import math


class UtilityCurve:

    def confidence(
        self,
        agents: int,
        trust: float,
    ) -> float:

        return (
            1.0
            - math.exp(
                -agents * trust / 10
            )
        )
