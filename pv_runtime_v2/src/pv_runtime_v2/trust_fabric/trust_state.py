from dataclasses import dataclass
from datetime import datetime


@dataclass(
    frozen=True,
    slots=True,
)
class TrustState:

    agent_id: str

    trust_score: float

    risk_score: float

    policy_version: str

    capability_hash: str

    is_quarantined: bool

    updated_at: datetime
