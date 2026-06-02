class BenchmarkEngine:

    def compare(
        self,
        current_cost,
        benchmark_cost
    ):

        if benchmark_cost <= 0:
            return {}

        delta = current_cost - benchmark_cost

        return {
            "current_cost": current_cost,
            "benchmark_cost": benchmark_cost,
            "difference": delta,
            "percent_above_benchmark":
                round(delta / benchmark_cost * 100, 2)
        }
