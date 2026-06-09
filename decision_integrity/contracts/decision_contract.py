from dataclasses import dataclass


@dataclass
class DecisionContract:
    decision_id: str

    intent_hash: str

    policy_hash: str

    capability_token_hash: str

    context_integrity_score: float

    decision_integrity_score: float

    authorized: bool

    outcome: str
