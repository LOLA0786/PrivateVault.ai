import hashlib
import json
import time


def create_runtime_receipt(result):

    receipt = {
        "timestamp": time.time(),
        "decision": (
            "ALLOW"
            if result["passed"]
            else "BLOCK"
        ),
        "canonical_action": result["canonical_action"],
        "semantic_convergence": result.get(
            "semantic_convergence"
        ),
        "enterprise_state": result.get(
            "enterprise_state"
        ),
        "constraints": result.get(
            "constraints"
        ),
        "invariants": result.get(
            "invariants"
        ),
    }

    receipt["sha256"] = hashlib.sha256(
        json.dumps(
            receipt,
            sort_keys=True,
            default=str,
        ).encode()
    ).hexdigest()

    return receipt
