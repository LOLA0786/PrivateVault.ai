import statistics


class VarianceReport:

    @staticmethod
    def summarize(values: list[float]):

        return {
            "mean": statistics.mean(values),
            "std": statistics.stdev(values)
            if len(values) > 1
            else 0.0,
            "min": min(values),
            "max": max(values),
        }
