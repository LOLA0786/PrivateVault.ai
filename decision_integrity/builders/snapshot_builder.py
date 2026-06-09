import hashlib
import json
import uuid

from decision_integrity.schemas.decision_integrity_snapshot import (
    DecisionIntegritySnapshot
)


def sha256(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def build_snapshot(
    actor_id: str,
    agent_id: str,
    intent_text: str,
    policy_version: str,
    policy_hash: str,
    capability_tokens=None,
    trust_score: float = 0.0,
    tools_requested=None,
    tools_authorized=None,
    approval_chain=None,
    execution_contract_hash: str = ""
):

    capability_tokens = capability_tokens or []
    tools_requested = tools_requested or []
    tools_authorized = tools_authorized or []
    approval_chain = approval_chain or []

    intent_hash = sha256(intent_text)

    snapshot = DecisionIntegritySnapshot(
        decision_id=str(uuid.uuid4()),
        timestamp="",
        actor_id=actor_id,
        agent_id=agent_id,
        intent_hash=intent_hash,
        intent_text=intent_text,
        policy_version=policy_version,
        policy_hash=policy_hash,
        capability_tokens=capability_tokens,
        trust_score=trust_score,
        tools_requested=tools_requested,
        tools_authorized=tools_authorized,
        approval_chain=approval_chain,
        execution_contract_hash=execution_contract_hash,
    )

    return snapshot


def snapshot_dict(snapshot):
    return snapshot.__dict__


def snapshot_hash(snapshot):
    payload = json.dumps(
        snapshot_dict(snapshot),
        sort_keys=True,
        default=str
    )

    return sha256(payload)
