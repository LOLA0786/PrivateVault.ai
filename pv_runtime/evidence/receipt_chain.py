import hashlib
import json
import os

CHAIN_FILE = "decision_receipts.log"


def _last_hash():
    if not os.path.exists(CHAIN_FILE):
        return "GENESIS"

    with open(CHAIN_FILE, "r") as f:
        lines = [l.strip() for l in f if l.strip()]

    if not lines:
        return "GENESIS"

    return json.loads(lines[-1])["receipt_hash"]


def append_receipt(receipt: dict):
    receipt["previous_receipt_hash"] = _last_hash()

    canonical = json.dumps(
        receipt,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )

    receipt["receipt_hash"] = hashlib.sha256(
        canonical.encode()
    ).hexdigest()

    with open(CHAIN_FILE, "a") as f:
        f.write(json.dumps(receipt) + "\n")

    return receipt
