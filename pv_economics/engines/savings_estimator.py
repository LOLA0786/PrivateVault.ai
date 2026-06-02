class SavingsEstimator:

    def estimate(
        self,
        current_cost,
        optimized_cost
    ):

        savings = max(
            current_cost - optimized_cost,
            0
        )

        return {
            "current_cost":
                current_cost,

            "optimized_cost":
                optimized_cost,

            "savings":
                savings,

            "savings_percent":
                round(
                    savings /
                    max(current_cost, 1),
                    2
                )
        }
