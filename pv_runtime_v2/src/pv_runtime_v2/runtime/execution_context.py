from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionContext:

    request_id: str

    agent_id: str

    capability: str

    trust_score: float = 0.0

    consensus_score: float = 0.0

    economic_score: float = 0.0
