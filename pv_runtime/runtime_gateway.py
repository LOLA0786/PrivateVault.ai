"""
PrivateVault Runtime Gateway.

Every privileged execution should eventually enter the runtime through
this gateway.

Today this is a thin wrapper around ExecutionController.

Future responsibilities include:

- Capability verification
- World-state validation
- TOCTOU protection
- Session risk evaluation
- Topology risk evaluation
- Execution attestation
"""

from pv_runtime.execution_controller.controller import ExecutionController
from pv_runtime.capability_issuer import issue_capability
from pv_runtime.adapters.runtime_adapter import attach_capability


_controller = ExecutionController()


def execute(runtime_context):
    """
    Canonical runtime entrypoint.

    Accepts an immutable RuntimeContext and delegates execution to the
    ExecutionController.
    """

    capability = issue_capability(
        principal=runtime_context.agent_id,
        action=runtime_context.intent.get("action", ""),
    )

    runtime_context = attach_capability(
        runtime_context,
        capability,
    )

    return _controller.execute_context(runtime_context)
