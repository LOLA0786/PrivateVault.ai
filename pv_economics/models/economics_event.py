from dataclasses import dataclass


@dataclass
class EconomicsEvent:

    agent: str

    task: str

    cost_usd: float

    success: bool

    trust_score: float

    roi_score: float

    waste_score: float

    latency_ms: float

    model: str
