import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from approval_binding import (
    expected_approval_hash
)

from decision_integrity.runtime.runtime_authorizer import (
    authorize_with_decision_integrity
)

intent = {
    "action": "process_payment",
    "amount": 500,
    "recipient": "vendor-a",
    "currency": "USD",
    "country": "US"
}

valid_approval = {
    "intent_hash":
        expected_approval_hash(intent)
}

invalid_approval = {
    "intent_hash":
        "tampered_hash"
}

r1 = authorize_with_decision_integrity(
    intent,
    approval=valid_approval
)

print(
    "VALID_APPROVAL:",
    r1["decision_outcome"]
)

r2 = authorize_with_decision_integrity(
    intent,
    approval=invalid_approval
)

print(
    "INVALID_APPROVAL:",
    r2["decision_outcome"]
)

print("PASS")
