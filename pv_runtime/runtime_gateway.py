"""
PrivateVault Runtime Gateway.

Every privileged execution should eventually enter the runtime through
this gateway.
"""

from pv_runtime.execution_controller.controller import ExecutionController
from pv_runtime.capability_issuer import issue_capability
from pv_runtime.adapters.runtime_adapter import attach_capability
from pv_runtime.authorization_service import authorize


_controller = ExecutionController()


def execute(runtime_context):
    """
    Canonical runtime entrypoint.

    1. Issue execution capability.
    2. Attach capability to immutable RuntimeContext.
    3. Perform authorization.
    4. Execute.
    """

    capability = issue_capability(
        principal=runtime_context.agent_id,
        action=runtime_context.intent.get("action", ""),
    )

    runtime_context = attach_capability(
        runtime_context,
        capability,
    )

    authorize(runtime_context)

    return _controller.execute_context(runtime_context)
