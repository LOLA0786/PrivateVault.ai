class ContextWaste:

    def analyze(
        self,
        sent_tokens,
        used_tokens
    ):

        wasted = max(
            sent_tokens - used_tokens,
            0
        )

        return {
            "wasted_tokens": wasted,
            "waste_percent":
                round(
                    wasted /
                    max(sent_tokens, 1)
                    * 100,
                    2
                )
        }
