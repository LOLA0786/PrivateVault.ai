from dataclasses import dataclass


@dataclass
class CostMetrics:
    total_estimated: float = 0.0
    total_saved: float = 0.0

    def record_estimate(self, cost: float) -> None:
        self.total_estimated += cost

    def record_saved(self, saved: float) -> None:
        self.total_saved += saved
