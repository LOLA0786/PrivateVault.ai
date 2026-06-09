from intent_binding import assert_intent_binding
from approval_binding import assert_approval_binding
from jwt_capability import verify_jwt_cap


def authorize_execution(
    declared_intent,
    executed_intent,
    approval,
    capability_token,
    action,
    principal,
):
    assert_intent_binding(
        declared_intent,
        executed_intent
    )

    assert_approval_binding(
        declared_intent,
        approval
    )

    verify_jwt_cap(
        capability_token,
        action,
        principal
    )

    return True
