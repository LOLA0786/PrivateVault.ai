from dataclasses import dataclass


@dataclass
class EconomicsReport:

    agent: str

    trust_score: float

    success_score: float

    waste_score: float

    roi_score: float

    cost_usd: float

    optimization_potential: float
