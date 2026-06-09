class QualityMetrics:

    @staticmethod
    def accuracy(
        total: int,
        correct: int,
    ):

        return (
            correct
            / total
        )
