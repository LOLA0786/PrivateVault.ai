from approval_binding import (
    assert_approval_binding
)


def verify_approval_binding(
    snapshot,
    intent,
    approval
):

    try:

        assert_approval_binding(
            intent,
            approval
        )

        snapshot.metadata[
            "approval_binding"
        ] = "VALID"

        return True

    except Exception as e:

        snapshot.metadata[
            "approval_binding"
        ] = str(e)

        snapshot.policy_context_conflict = True

        return False
