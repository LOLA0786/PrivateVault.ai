import hashlib

from decision_integrity.contracts.decision_contract import (
    DecisionContract
)


def sha256(v):
    return hashlib.sha256(
        str(v).encode()
    ).hexdigest()


def build_decision_contract(snapshot):

    token_hash = sha256(
        "|".join(snapshot.capability_tokens)
    )

    return DecisionContract(
        decision_id=snapshot.decision_id,
        intent_hash=snapshot.intent_hash,
        policy_hash=snapshot.policy_hash,
        capability_token_hash=token_hash,
        context_integrity_score=(
            sum(snapshot.context_trust_scores)
            / len(snapshot.context_trust_scores)
            if snapshot.context_trust_scores
            else 1.0
        ),
        decision_integrity_score=snapshot.decision_integrity_score,
        authorized=snapshot.outcome == "AUTHORIZED",
        outcome=snapshot.outcome
    )
