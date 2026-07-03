
#!/usr/bin/env python3

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import hashlib
import sys
from collections import Counter

from pv_runtime.evidence.receipt_signer import verify_receipt

LOG = sys.argv[1] if len(sys.argv) > 1 else "decision_receipts.log"

REQUIRED = {
    "schema_version",
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
    "previous_receipt_hash",
    "receipt_hash",
}

def canonical(receipt):
    r = dict(receipt)

    # append_receipt() hashes the signed receipt.
    # Only receipt_hash itself is excluded.
    r.pop("receipt_hash", None)

    return json.dumps(
        r,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode()

prev = "GENESIS"

counts = Counter()

ok = True

receipts = []

with open(LOG) as f:
    receipts = [json.loads(x) for x in f if x.strip()]

for i, r in enumerate(receipts, 1):

    counts[r["decision"]] += 1

    missing = REQUIRED - r.keys()

    if missing:
        print(f"[FAIL] Receipt {i}: missing {sorted(missing)}")
        ok = False

    expected = hashlib.sha256(canonical(r)).hexdigest()

    if expected != r["receipt_hash"]:
        print(f"[FAIL] Receipt {i}: hash")
        ok = False

    if not verify_receipt(r):
        print(f"[FAIL] Receipt {i}: signature")
        ok = False

    if r["previous_receipt_hash"] != prev:
        print(f"[FAIL] Receipt {i}: chain")
        ok = False

    prev = r["receipt_hash"]

print()

print("Receipt Schema :", "v1.0")
print("Receipts       :", len(receipts))
print("ALLOW          :", counts["ALLOW"])
print("REJECT         :", counts["REJECT"])
print()

print("PASS" if ok else "FAIL")

sys.exit(0 if ok else 1)
