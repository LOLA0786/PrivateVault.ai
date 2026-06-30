"""
Canonical execution adapter.

This module preserves the historical execute_action(intent, decision)
API while routing execution through the enterprise ExecutionController.

DO NOT execute tools directly from here.
"""

from pv_runtime.execution_controller.controller import ExecutionController

# Singleton controller for the process.
_controller = ExecutionController()


def execute_action(intent, decision):
    """
    Legacy compatibility wrapper.

    Parameters
    ----------
    intent : dict
        Normalized intent.

    decision : dict
        Canonical decision object.
        Expected:
            {
                "allowed": bool,
                ...
            }
    """

    if not decision.get("allowed", False):
        return {
            "executed": False,
            "reason": "blocked_by_policy",
        }

    agent_id = (
        intent.get("agent_id")
        or intent.get("principal")
        or "pv-runtime"
    )

    return _controller.execute(
        agent_id=agent_id,
        action=intent,
    )
