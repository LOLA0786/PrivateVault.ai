from dataclasses import replace
"""
PrivateVault Runtime Gateway.

Canonical runtime entrypoint.

Every privileged execution passes through this gateway.
"""

from pv_runtime.execution_controller.controller import ExecutionController

from pv_runtime.capability_issuer import issue_capability
from pv_runtime.authorization_service import authorize

from pv_runtime.adapters.runtime_adapter import attach_capability

from pv_runtime.loop.manager import LoopManager
from pv_runtime.loop.governor import LoopGovernor
from pv_runtime.loop.economics import LoopEconomicsEngine
from pv_runtime.loop.evidence import record_iteration
from pv_runtime.loop.receipt import generate_receipt


_controller = ExecutionController()

_loop_manager = LoopManager()
_loop_governor = LoopGovernor()
_loop_economics = LoopEconomicsEngine()


def execute(
    runtime_context,
    loop_context=None,
):
    """
    Runtime execution pipeline.

    Loop
        ↓
    Governor
        ↓
    Capability
        ↓
    Authorization
        ↓
    Execution
        ↓
    Economics
        ↓
    Evidence
        ↓
    Receipt
    """

    #
    # Loop lifecycle
    #

    if loop_context is None:

        loop_context = _loop_manager.start(
            goal=str(runtime_context.intent),
            runtime_context=runtime_context,
        )

    else:

        loop_context = _loop_manager.next_iteration(
            loop_context,
            runtime_context,
        )

    #
    # Loop governance
    #

    governor = _loop_governor.evaluate(
        loop_context
    )

    if not governor.allowed:

        loop_context = record_iteration(loop_context)

        receipt = generate_receipt(loop_context)

        return {
            "status": governor.action,
            "reason": governor.reason,
            "executed": False,
            "loop": loop_context,
            "loop_receipt": receipt,
        }

    #
    # Capability
    #

    capability = issue_capability(
        principal=runtime_context.agent_id,
        action=runtime_context.intent.get(
            "action",
            "",
        ),
    )

    runtime_context = attach_capability(
        runtime_context,
        capability,
    )

    loop_context = replace(
        loop_context,
        runtime_context=runtime_context,
    )

    #
    # Authorization
    #

    try:

        authorize(runtime_context)

    except Exception as e:

        #
        # Authorization failure is itself immutable evidence.
        #

        loop_context = record_iteration(
            loop_context
        )

        receipt = generate_receipt(
            loop_context
        )

        return {
            "status": "BLOCK",
            "reason": str(e),
            "executed": False,
            "loop": loop_context,
            "loop_receipt": receipt,
        }

    #
    # Execution
    #

    execution = _controller.execute_context(
        runtime_context
    )

    #
    # Economics
    #
    # Placeholder values until ExecutionController
    # exports real metrics.
    #

    metrics = execution.get("metrics")

    loop_context = _loop_economics.update(
        loop_context,
        outcome={
            "success": execution.get("status") == "SUCCESS",
            "business_value": 0,
        },
        cost_usd=metrics.cost_usd if metrics else 0,
        latency_ms=metrics.latency_ms if metrics else 0,
        input_tokens=metrics.input_tokens if metrics else 0,
        used_tokens=metrics.used_tokens if metrics else 0,
        total_tool_calls=metrics.total_tool_calls if metrics else 0,
        useful_tool_calls=metrics.useful_tool_calls if metrics else 0,
    )

    #
    # Cryptographic evidence
    #

    loop_context = record_iteration(
        loop_context
    )

    #
    # Immutable receipt
    #

    receipt = generate_receipt(
        loop_context
    )

    execution["capability"] = capability

    execution["loop"] = loop_context
    execution["loop_receipt"] = receipt

    return execution