class EconomicsScore:

    def calculate(
        self,
        success,
        trust,
        waste
    ):

        return round(
            (
                success * 0.4 +
                trust * 0.4 +
                (100 - waste) * 0.2
            ),
            2
        )
