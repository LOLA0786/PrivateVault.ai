"""
Benchmark Engine — compares execution cost against peer baselines.
Baselines are seeded from real LLM pricing benchmarks (June 2025).
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class BenchmarkResult:
    current_cost:          float
    benchmark_cost:        float
    delta:                 float
    percentile_estimate:   int     # estimated cost percentile vs peers
    verdict:               str     # optimal / acceptable / expensive / critical


# Seed baselines: median cost per 1K tokens (input+output blended) by task type
_BASELINES = {
    "simple_qa":       0.0003,
    "rag_query":       0.0012,
    "code_generation": 0.0025,
    "multi_agent":     0.0080,
    "default":         0.0015,
}


class BenchmarkEngine:

    def compare(
        self,
        current_cost:   float,
        task_type:      str   = "default",
        input_tokens:   int   = 0,
        benchmark_cost: Optional[float] = None,
    ) -> BenchmarkResult:

        if benchmark_cost is None:
            base_per_1k     = _BASELINES.get(task_type, _BASELINES["default"])
            benchmark_cost  = base_per_1k * max(input_tokens / 1000, 1)

        if benchmark_cost <= 0:
            benchmark_cost = 0.0001

        delta = current_cost - benchmark_cost
        ratio = current_cost / benchmark_cost

        # Rough percentile estimate from ratio
        percentile = int(min(max(ratio * 50, 1), 99))

        verdict = (
            "optimal"    if ratio <= 0.8  else
            "acceptable" if ratio <= 1.2  else
            "expensive"  if ratio <= 2.0  else
            "critical"
        )

        return BenchmarkResult(
            current_cost=round(current_cost, 6),
            benchmark_cost=round(benchmark_cost, 6),
            delta=round(delta, 6),
            percentile_estimate=percentile,
            verdict=verdict,
        )
