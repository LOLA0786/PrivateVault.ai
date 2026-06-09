import hashlib

from auth import authorize_intent

from decision_integrity.runtime.intent_bridge import (
    canonical_intent_hash
)

from decision_integrity.runtime.approval_bridge import (
    verify_approval_binding
)

from decision_integrity.builders.snapshot_builder import (
    build_snapshot
)

from decision_integrity.builders.decision_authorization import (
    authorize_decision
)

from decision_integrity.builders.decision_contract_builder import (
    build_decision_contract
)


def sha256(v):
    return hashlib.sha256(
        str(v).encode()
    ).hexdigest()


def authorize_with_decision_integrity(
    intent,
    approval=None,
    policy_version="fintech-v1.1"
):

    policy_result = authorize_intent(
        intent,
        policy_version=policy_version
    )

    intent_hash = canonical_intent_hash(
        intent
    )

    snapshot = build_snapshot(
        actor_id="runtime",
        agent_id="privatevault-agent",
        intent_text=intent_hash,
        policy_version=policy_version,
        policy_hash=sha256(policy_version),
        trust_score=0.99,
    )

    snapshot.intent_hash = intent_hash

    verify_approval_binding(
        snapshot,
        intent,
        approval
    )

    if not policy_result.get("allowed"):
        snapshot.policy_context_conflict = True

    authorize_decision(snapshot)

    contract = build_decision_contract(
        snapshot
    )

    return {
        "policy_result": policy_result,
        "decision_integrity_score":
            snapshot.decision_integrity_score,
        "decision_outcome":
            snapshot.outcome,
        "decision_id":
            snapshot.decision_id,
        "intent_hash":
            intent_hash,
        "contract":
            contract,
        "snapshot":
            snapshot,
    }
