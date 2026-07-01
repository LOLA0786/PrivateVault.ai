"""
Canonical Loop State Machine.
"""

from enum import Enum


class LoopState(str, Enum):
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
    TERMINATED = "TERMINATED"
    COMPLETED = "COMPLETED"


_ALLOWED = {
    LoopState.CREATED: {
        LoopState.RUNNING,
        LoopState.TERMINATED,
    },
    LoopState.RUNNING: {
        LoopState.PAUSED,
        LoopState.APPROVAL_REQUIRED,
        LoopState.COMPLETED,
        LoopState.TERMINATED,
    },
    LoopState.PAUSED: {
        LoopState.RUNNING,
        LoopState.TERMINATED,
    },
    LoopState.APPROVAL_REQUIRED: {
        LoopState.RUNNING,
        LoopState.TERMINATED,
    },
    LoopState.COMPLETED: set(),
    LoopState.TERMINATED: set(),
}


def transition(current, target):

    if target not in _ALLOWED[current]:
        raise Exception(
            f"INVALID_LOOP_TRANSITION:{current}->{target}"
        )

    return target
