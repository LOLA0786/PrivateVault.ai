
import json

REQUIRED = {
    "schema_version",
    "receipt_hash",
    "previous_receipt_hash",
    "timestamp",
    "decision",
    "reason",
    "decision_id",
    "jti",
    "canonical_action",
    "semantic_convergence",
    "enterprise_state",
    "constraints",
    "invariants",
    "sha256",
    "signature",
}

with open("decision_receipts.log") as f:
    receipt = json.loads(next(f))

missing = REQUIRED - receipt.keys()

assert not missing, f"Missing fields: {missing}"

assert receipt["schema_version"] == "1.0"
