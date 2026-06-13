class AdversarialWaste:

    def evaluate(
        self,
        collusion_attempts=0,
        stitch_attempts=0,
        unicode_attempts=0,
        blocked_attempts=0
    ):

        score = (
            collusion_attempts * 20 +
            stitch_attempts * 10 +
            unicode_attempts * 5 +
            blocked_attempts * 2
        )

        return {
            "score": min(score,100)
        }
