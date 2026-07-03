from pv_runtime.adversarial.runtime_gate_wrapper import (
    authorize_execution_with_adversarial,
)


def authorize_tool_call(
    user_id,
    tool_name,
    declared_intent=None,
    executed_intent=None,
    approval=None,
    capability_token=None,
    evidence=None,
):

    try:

        if (
            declared_intent is not None
            and executed_intent is not None
            and approval is not None
            and capability_token is not None
        ):

            runtime_result = authorize_execution_with_adversarial(
                declared_intent=declared_intent,
                executed_intent=executed_intent,
                approval=approval,
                capability_token=capability_token,
                action=tool_name,
                principal=user_id,
                evidence=evidence,
            )

            return {
                "authorized": runtime_result["authorized"],
                "executed": True,
                "signature": f"sig_{user_id}_{tool_name}",
                "runtime_receipt": runtime_result["runtime_receipt"],
            }

    except Exception as e:

        return {
            "authorized": False,
            "executed": False,
            "error": str(e),
        }
