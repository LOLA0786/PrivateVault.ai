class WasteEngine:

    def evaluate(
        self,
        retries=0,
        input_tokens=0,
        output_tokens=0
    ):

        score = 0

        score += retries * 10

        if input_tokens > 5000:
            score += 10

        if input_tokens > 10000:
            score += 20

        if input_tokens > 20000:
            score += 20

        if output_tokens > 5000:
            score += 10

        return min(score, 100)
