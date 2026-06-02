class ToolWaste:

    def analyze(
        self,
        total_calls,
        useful_calls
    ):

        wasted = max(
            total_calls - useful_calls,
            0
        )

        return {
            "wasted_calls": wasted,
            "waste_percent":
                round(
                    wasted /
                    max(total_calls, 1)
                    * 100,
                    2
                )
        }
