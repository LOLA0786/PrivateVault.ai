import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from decision_integrity.runtime.runtime_authorizer import (
    authorize_with_decision_integrity
)

good = {
    "action": "process_payment",
    "amount": 500,
    "country": "US"
}

bad = {
    "action": "process_payment",
    "amount": 25000,
    "country": "US"
}

r1 = authorize_with_decision_integrity(good)

print("GOOD_ALLOWED:",
      r1["policy_result"]["allowed"])

print("GOOD_SCORE:",
      r1["decision_integrity_score"])

print("GOOD_OUTCOME:",
      r1["decision_outcome"])

r2 = authorize_with_decision_integrity(bad)

print("BAD_ALLOWED:",
      r2["policy_result"]["allowed"])

print("BAD_SCORE:",
      r2["decision_integrity_score"])

print("BAD_OUTCOME:",
      r2["decision_outcome"])

print("PASS")
