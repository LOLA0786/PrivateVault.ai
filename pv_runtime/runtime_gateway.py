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


_controller = ExecutionController()


def execute(runtime_context):
    """
    Canonical runtime entrypoint.

    Accepts an immutable RuntimeContext and delegates execution to the
    ExecutionController.
    """

    return _controller.execute_context(runtime_context)
