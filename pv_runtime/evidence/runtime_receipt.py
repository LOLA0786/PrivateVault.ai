import hashlib
import json
import time

from pv_runtime.evidence.receipt_chain import append_receipt
from pv_runtime.evidence.receipt_signer import sign_receipt


def create_runtime_receipt(
    result,
    decision=None,
    reason=None,
):

    receipt = {
        "timestamp": time.time(),
        "decision": decision or (
            "ALLOW" if result.get("passed") else "REJECT"
        ),
        "reason": reason,
        "canonical_action": result.get("canonical_action"),
        "semantic_convergence": result.get("semantic_convergence"),
        "enterprise_state": result.get("enterprise_state"),
        "constraints": result.get("constraints"),
        "invariants": result.get("invariants"),
    }

    receipt["sha256"] = hashlib.sha256(
        json.dumps(
            receipt,
            sort_keys=True,
            default=str,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()

    receipt["signature"] = sign_receipt(receipt)

    append_receipt(receipt)

    return receipt
