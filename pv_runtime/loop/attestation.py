"""
Loop Attestation.
"""

import hashlib
import json


def attest(loop):

    payload = {
        "loop": loop.loop_id,
        "iteration": loop.iteration,
        "goal": loop.goal,
        "evidence": loop.evidence.current_hash,
        "economics": loop.economics.total_cost,
    }

    return hashlib.sha256(
        json.dumps(
            payload,
            sort_keys=True,
        ).encode()
    ).hexdigest()
