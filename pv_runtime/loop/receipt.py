"""
Loop Receipt.

Produces an immutable receipt for a completed loop.
"""

import hashlib
import json

from pv_runtime.loop.models import LoopContext


def generate_receipt(loop: LoopContext):

    receipt = {
        "loop_id": loop.loop_id,
        "goal": loop.goal,
        "iterations": loop.iteration,
        "max_iterations": loop.max_iterations,

        "economics": {
            "total_cost": loop.economics.total_cost,
            "context_bytes": loop.economics.context_bytes,
            "referenced_bytes": loop.economics.referenced_bytes,
            "wasted_bytes": loop.economics.wasted_bytes,
        },

        "health": {
            "score": loop.health.score,
            "converging": loop.health.converging,
            "drift": loop.health.drift_detected,
            "stop_reason": loop.health.stop_reason,
        },

        "evidence": {
            "previous_hash": loop.evidence.previous_hash,
            "current_hash": loop.evidence.current_hash,
            "merkle_root": loop.evidence.merkle_root,
        },

        "metadata": dict(loop.metadata),
    }

    receipt["receipt_hash"] = hashlib.sha256(
        json.dumps(
            receipt,
            sort_keys=True,
            default=str,
        ).encode()
    ).hexdigest()

    return receipt
