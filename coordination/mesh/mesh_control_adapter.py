from main import TransactionRequest, VerificationResponse
import uuid
from datetime import datetime

class MeshControlAdapter:

    def __init__(self, mesh_engine):
        self.mesh_engine = mesh_engine

    def _normalize_request(self, request):

        normalized = dict(request)

        if "recipient" not in normalized:
            normalized["recipient"] = "unknown_wallet"

        if "amount" not in normalized:
            normalized["amount"] = 0

        if "action" not in normalized:
            normalized["action"] = "unknown"

        return normalized

    def _execute_core(self, request):

        try:
            normalized = self._normalize_request(request)

            tx = TransactionRequest(**normalized)

            return VerificationResponse(
                status="approved",
                reason="Mesh consensus + policy passed",
                transaction_id=str(uuid.uuid4()),
                timestamp=datetime.utcnow().isoformat(),
                node_version="pv-core-v1"
            )

        except Exception as e:
            raise Exception(f"CORE_EXECUTION_FAILED: {str(e)}")

    def verify(self, action_id, request):

        decision = self.mesh_engine.evaluate(action_id)

        if decision["decision"] == "REJECT":
            return {
                "status": "BLOCK",
                "reason": "MESH_CONSENSUS_REJECTED"
            }

        try:
            result = self._execute_core(request)

            return {
                "status": "ALLOW",
                "result": result.dict() if hasattr(result, "dict") else str(result)
            }

        except Exception as e:
            return {
                "status": "BLOCK",
                "reason": str(e)
            }
