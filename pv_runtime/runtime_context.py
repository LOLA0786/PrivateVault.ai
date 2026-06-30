"""
PrivateVault Runtime Context

This module defines the canonical runtime context passed through the
execution pipeline.

Nothing executes directly from this module.
It only builds the immutable execution context.
"""

from copy import deepcopy


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
    enforcement,
    runtime_security,
):
    """
    Construct the canonical runtime context.

    The returned object is intentionally execution-agnostic.
    Execution metadata (results, evidence, replay, receipts)
    is attached later in the pipeline.
    """

    runtime_context = {
        "agent_id": agent_id,

        "identity": deepcopy(identity),
        "tenant": deepcopy(tenant),

        "intent": deepcopy(intent),
        "context": deepcopy(context),

        "simulation": deepcopy(simulation),
        "risk": deepcopy(risk),

        "decision": deepcopy(decision),
        "approval": deepcopy(approval),
        "enforcement": deepcopy(enforcement),

        "runtime_security": deepcopy(runtime_security),

        #
        # Execution-time fields
        #
        "capability_token": None,
        "execution": None,

        #
        # Future runtime extensions
        #
        "snapshot_hash": None,
        "world_state_hash": None,
        "policy_version": None,
        "session_id": None,
        "lease_id": None,
        "evidence": {},
    }

    return runtime_context
