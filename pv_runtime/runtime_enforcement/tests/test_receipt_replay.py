import pytest

from jwt_capability import issue_jwt_cap, verify_jwt_cap

ACTION = "process_payment"
PRINCIPAL = "agent_001"

def test_capability_token_single_use():

    token = issue_jwt_cap(
        "decision-123",
        ACTION,
        PRINCIPAL,
    )

    verify_jwt_cap(
        token,
        ACTION,
        PRINCIPAL,
    )

    with pytest.raises(Exception) as e:
        verify_jwt_cap(
            token,
            ACTION,
            PRINCIPAL,
        )

    assert str(e.value) == "REPLAY_DETECTED"
