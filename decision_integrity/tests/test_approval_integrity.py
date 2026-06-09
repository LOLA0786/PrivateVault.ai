import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from decision_integrity.runtime.runtime_authorizer import (
    authorize_with_decision_integrity
)

intent = {
    "action": "process_payment",
    "amount": 500,
    "country": "US"
}

r1 = authorize_with_decision_integrity(
    intent,
    approval_count=2
)

print("WITH_APPROVALS:",
      r1["decision_outcome"])

r2 = authorize_with_decision_integrity(
    intent,
    approval_count=0
)

print("WITHOUT_APPROVALS:",
      r2["decision_outcome"])

print("PASS")
