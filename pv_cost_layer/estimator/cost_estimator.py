from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Pricing:
    input_per_token: float
    output_per_token: float


@dataclass(frozen=True)
class CostEstimate:
    input_tokens: int
    output_tokens: int
    total_cost: float


class CostEstimator:
    def __init__(self, pricing: Optional[Pricing] = None):
        self._pricing = pricing or Pricing(0.0, 0.0)

    def estimate(self, input_tokens: int = 0, output_tokens: int = 0) -> CostEstimate:
        cost = (
            input_tokens * self._pricing.input_per_token
            + output_tokens * self._pricing.output_per_token
        )
        return CostEstimate(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_cost=cost,
        )
