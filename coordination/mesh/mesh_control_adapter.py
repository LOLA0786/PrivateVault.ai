from pv_mesh_enforcer import enforce
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
            action = {
                "tool": request.get("action", "unknown"),
                "params": request
            }
            agent_chain = ["mesh", "executor"]

            if not enforce(action, agent_chain):
                return {
                    "status": "BLOCK",
                    "reason": "PRIVATEVAULT_BLOCKED"
                }
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

class TransactionRequest:
    def __init__(self, amount, user_id, risk_score):
        self.amount = amount
        self.user_id = user_id
        self.risk_score = risk_score

class VerificationResponse:
    def __init__(self, approved, reason):
        self.approved = approved
        self.reason = reason
