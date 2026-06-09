class UtilityFunction:

    def score(
        self,
        value: float,
        cost: float,
    ) -> float:

        return (
            value - cost
        )
