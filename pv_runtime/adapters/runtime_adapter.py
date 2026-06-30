"""
Runtime Adapter.

Converts legacy dictionary-based runtime objects into immutable runtime
models. This module contains no execution logic.
"""

from pv_runtime.models.decision import Decision
from pv_runtime.models.approval import Approval
from pv_runtime.models.capability import Capability
from pv_runtime.models.runtime_context import RuntimeContext


def build_decision(decision_dict):
    if decision_dict is None:
        return None

    return Decision(
        allowed=decision_dict.get("allowed", False),
        reason=decision_dict.get("reason", ""),
        risk_score=decision_dict.get("risk_score", 0.0),
        policy_version=decision_dict.get("policy_version", ""),
        metadata=decision_dict.get("metadata", {}),
    )


def build_approval(approval_dict):
    if approval_dict is None:
        return None

    return Approval(
        approved=approval_dict.get("approved", True),
        approver=approval_dict.get("approver", ""),
        intent_hash=approval_dict.get("intent_hash", ""),
        approval_hash=approval_dict.get("approval_hash", ""),
        approval_id=approval_dict.get("approval_id", ""),
        expires_at=approval_dict.get("expires_at", 0),
    )


def build_capability(capability_dict):
    if capability_dict is None:
        return None

    return Capability(
        token=capability_dict.get("token", ""),
        capability_id=capability_dict.get("capability_id", ""),
        principal=capability_dict.get("principal", ""),
        action=capability_dict.get("action", ""),
        issued_at=capability_dict.get("issued_at", 0),
        expires_at=capability_dict.get("expires_at", 0),
        single_use=capability_dict.get("single_use", True),
    )


def build_runtime_context(
    *,
    agent_id,
    identity,
    tenant,
    intent,
    context,
    simulation,
    risk,
    decision,
    approval,
    runtime_security,
    capability=None,
    execution=None,
    evidence=None,
):
    return RuntimeContext(
        agent_id=agent_id,
        identity=identity,
        tenant=tenant,
        intent=intent,
        context=context,
        simulation=simulation,
        risk=risk,
        decision=build_decision(decision),
        approval=build_approval(approval),
        capability=build_capability(capability),
        runtime_security=runtime_security,
        execution=execution or {},
        evidence=evidence or {},
    )
