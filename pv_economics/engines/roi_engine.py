class ROIEngine:

    def evaluate(
        self,
        cost,
        business_value
    ):

        if cost <= 0:
            return 0

        return round(
            business_value / cost,
            2
        )
