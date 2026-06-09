class TrustUpdater:

    @staticmethod
    def update(
        trust: float,
        correct: bool,
        reward: float = 0.002,
        penalty: float = 0.003,
    ):

        if correct:
            trust += reward
        else:
            trust -= penalty

        return max(
            0.05,
            min(
                trust,
                1.0,
            ),
        )
