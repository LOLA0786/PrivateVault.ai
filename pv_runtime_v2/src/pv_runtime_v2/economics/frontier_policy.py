from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class FrontierPolicy:

    trust: float

    impact: float

    latency_ms: float

    failure_risk: float

    max_agents: int = 1000
