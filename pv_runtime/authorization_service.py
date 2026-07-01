"""
PrivateVault Authorization Service.

This module is the single authorization entrypoint for privileged
runtime execution.

It performs authorization only.

It does NOT execute tools.
"""

from pv_runtime.runtime_enforcement.runtime_gate import (
    authorize_execution,
)


def authorize(runtime_context):
    """
    Authorize execution for a RuntimeContext.

    Raises an exception if authorization fails.
    Returns True on success.
    """

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

    authorize_execution(
        declared_intent=dict(runtime_context.intent),
        executed_intent=dict(runtime_context.intent),
        approval={
            "intent_hash": approval.intent_hash,
        },
        capability_token=capability.token,
        action=capability.action,
        principal=capability.principal,
    )

    return True
