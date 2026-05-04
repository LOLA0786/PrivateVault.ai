from dataclasses import dataclass


@dataclass(frozen=True)
class CostPolicy:
    max_cost_per_action: float
    max_daily_budget: float

    def allows(self, estimated_cost: float) -> bool:
        return estimated_cost <= self.max_cost_per_action
