from pv_runtime.runtime_enforcement.runtime_gate import (
    authorize_execution,
)

from pv_runtime.adversarial.runtime_enforcement_extension import (
    enforce_adversarial_risk,
)


def authorize_execution_with_adversarial(
    declared_intent,
    executed_intent,
    approval,
    capability_token,
    action,
    principal,
    payload=None,
):
    """
    Runtime authorization with optional adversarial validation.

    Production runtime (entrypoint.py) can pass the full payload.

    Lightweight callers and tests do not need to.
    """

    if payload is not None:
        enforce_adversarial_risk(payload)

    return authorize_execution(
        declared_intent=declared_intent,
        executed_intent=executed_intent,
        approval=approval,
        capability_token=capability_token,
        action=action,
        principal=principal,
    )
