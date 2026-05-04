from dataclasses import dataclass


@dataclass(frozen=True)
class CostContext:
    input_tokens: int
    output_tokens: int
    risk_score: float
