#!/usr/bin/env python3

import json
import hashlib
import sys
from pv_runtime.evidence.receipt_signer import verify_receipt

LOG = sys.argv[1] if len(sys.argv) > 1 else "decision_receipts.log"


def canonical(receipt):
    r = dict(receipt)
    r.pop("receipt_hash", None)
    return json.dumps(
        r,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode()


prev = "GENESIS"
ok = True

with open(LOG) as f:
    for i, line in enumerate(f, 1):
        r = json.loads(line)

        expected = hashlib.sha256(canonical(r)).hexdigest()

        if expected != r["receipt_hash"]:
            print(f"[FAIL] Receipt {i}: receipt_hash mismatch")
            ok = False
        else:
            print(f"[ OK ] Receipt {i}: receipt hash valid")

        if verify_receipt(r):
            print(f"[ OK ] Receipt {i}: signature valid")
        else:
            print(f"[FAIL] Receipt {i}: signature invalid")
            ok = False

        if r["previous_receipt_hash"] != prev:
            print(f"[FAIL] Receipt {i}: previous hash mismatch")
            ok = False
        else:
            print(f"[ OK ] Receipt {i}: chain link valid")

        prev = r["receipt_hash"]

print()

if ok:
    print("✅ CHAIN VERIFIED")
else:
    print("❌ CHAIN BROKEN")
