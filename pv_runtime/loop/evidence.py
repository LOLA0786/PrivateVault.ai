"""
Loop Evidence Engine.

Creates a cryptographic chain for every loop iteration.
"""

import hashlib
import json
from dataclasses import replace

from pv_runtime.loop.models import (
    LoopContext,
    LoopEvidence,
)


def _sha256(obj) -> str:
    return hashlib.sha256(
        json.dumps(
            obj,
            sort_keys=True,
            default=str,
        ).encode()
    ).hexdigest()


def record_iteration(loop: LoopContext) -> LoopContext:
    """
    Record one immutable loop iteration.

    current_hash =
        SHA256(
            previous_hash +
            runtime_context +
            iteration
        )
    """

    previous = loop.evidence.current_hash

    payload = {
        "previous_hash": previous,
        "iteration": loop.iteration,
        "runtime_context": loop.runtime_context,
    }

    current = _sha256(payload)

    evidence = LoopEvidence(
        previous_hash=previous,
        current_hash=current,
        merkle_root=current,
    )

    return replace(
        loop,
        evidence=evidence,
    )
