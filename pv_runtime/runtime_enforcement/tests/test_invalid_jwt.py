from uuid import uuid4

from jwt_capability import (
    issue_jwt_cap,
    verify_jwt_cap,
)

token = issue_jwt_cap(
    decision_id=str(uuid4()),
    action="transfer",
    principal="gateway-test",
)

print("VALID TOKEN")

# Corrupt one character without changing the length
bad = token[:-1] + ("A" if token[-1] != "A" else "B")

print("TOKEN CORRUPTED")

try:
    verify_jwt_cap(
        bad,
        action="transfer",
        principal="gateway-test",
    )

    raise AssertionError("INVALID TOKEN ACCEPTED")

except Exception as e:

    assert str(e) == "INVALID_CAPABILITY_TOKEN"

    print(str(e))
    print("PASS")
