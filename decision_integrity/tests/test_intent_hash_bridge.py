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

r1 = authorize_with_decision_integrity(intent)
r2 = authorize_with_decision_integrity(intent)

print("HASH1:", r1["intent_hash"][:16])
print("HASH2:", r2["intent_hash"][:16])

print(
    "MATCH:",
    r1["intent_hash"] == r2["intent_hash"]
)

print("PASS")
