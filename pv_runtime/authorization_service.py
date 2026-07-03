"""
PrivateVault Authorization Service.
"""

from pv_runtime.runtime_enforcement.runtime_gate import authorize_execution

from pv_runtime.models.evidence_bundle import EvidenceBundle


def authorize(runtime_context):

    decision = runtime_context.decision

    if decision is None:
        raise Exception("MISSING_DECISION")

    if not decision.allowed:
        raise Exception("DECISION_DENIED")

    approval = runtime_context.approval

    if approval is None:
        raise Exception("MISSING_APPROVAL")

    capability = runtime_context.capability

    if capability is None:
        raise Exception("MISSING_CAPABILITY")

    evidence = runtime_context.evidence

    if not isinstance(evidence, EvidenceBundle):
        evidence = EvidenceBundle()

    evidence.user_request = dict(runtime_context.intent)

    evidence.planner = dict(runtime_context.execution)

    evidence.approval = {
        "intent_hash": approval.intent_hash,
    }

    evidence.capability = {
        "token": capability.token,
        "action": capability.action,
        "principal": capability.principal,
    }

    authorize_execution(
        declared_intent=evidence.user_request,
        executed_intent=evidence.planner,
        evidence=evidence.to_dict(),
        approval=evidence.approval,
        capability_token=capability.token,
        action=capability.action,
        principal=capability.principal,
    )

    return True
