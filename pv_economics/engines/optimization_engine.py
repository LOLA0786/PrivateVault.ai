class OptimizationEngine:

    def suggest(self, execution):

        savings = []

        if execution.retries > 2:
            savings.append(
                "Reduce retries"
            )

        if execution.input_tokens > 10000:
            savings.append(
                "Compress context"
            )

        return savings
