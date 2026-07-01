from dataclasses import asdict
"""
Protocol -> Runtime adapter.

Converts ActionRequest into the internal RuntimeContext and
converts RuntimeGateway output back into ActionResponse.
"""

from pv_protocol.protocol import DecisionRuntime

from pv_protocol.action_request import (
    ActionRequest,
)

from pv_protocol.action_response import (
    ActionResponse,
    DecisionResult,
    ExecutionResult,
    CapabilityGrant,
    ReceiptReference,
)

from pv_runtime.runtime_gateway import execute

from pv_protocol.request_builder import build_runtime_context


class RuntimeAdapter(DecisionRuntime):

    def evaluate(
        self,
        request: ActionRequest,
    ) -> ActionResponse:

        #
        # Protocol -> Runtime
        #

        runtime_context = build_runtime_context(
            request
        )

        #
        # Execute runtime
        #

        result = execute(runtime_context)

        #
        # BLOCK
        #

        if result["status"] == "BLOCK":

            return ActionResponse(

                request_id=request.request_id,

                decision=DecisionResult(
                    allowed=False,
                    reason=result["reason"],
                ),

                execution=ExecutionResult(
                    executed=False,
                    status="BLOCK",
                ),

                receipt=ReceiptReference(
                    receipt_hash=result["loop_receipt"]["receipt_hash"],
                    merkle_root=result["loop_receipt"]["evidence"]["merkle_root"],
                ),

                metadata={
                    "loop": result["loop"],
                },
            )

        #
        # SUCCESS
        #

        receipt = result["loop_receipt"]

        return ActionResponse(

            request_id=request.request_id,

            decision=DecisionResult(
                allowed=True,
                reason="allowed",
            ),

            execution=ExecutionResult(
                executed=True,
                status="SUCCESS",
                result=result["result"],
            ),

            capability=CapabilityGrant(
                token=result.get("capability", ""),
            ),

            receipt=ReceiptReference(
                receipt_hash=receipt["receipt_hash"],
                merkle_root=receipt["evidence"]["merkle_root"],
            ),

            metrics=(
                asdict(result["metrics"])
                if result.get("metrics")
                else {}
            ),

            metadata={
                "loop": result["loop"],
            },
        )
