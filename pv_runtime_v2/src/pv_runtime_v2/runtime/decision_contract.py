from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class RuntimeDecision:

    request_id: str

    agent_id: str

    capability: str

    trust_score: float

    consensus_score: float

    economic_score: float

    approved: bool

    evidence_hash: str
