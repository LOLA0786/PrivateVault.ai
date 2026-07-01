from privatevault.evidence.merkle_chain import MerkleChain

from pv_core.policy.policy_service import evaluate

from pv_runtime.capability_issuer import issue_capability


class PrivateVaultAdapter:

    def __init__(self):
        self.merkle = MerkleChain()

    def evaluate_policy(self, request):

        result = evaluate(

            request.intent.description,

            {
                "goal": request.goal.description,
                "action": request.proposed_action.action_type,
                "target": request.proposed_action.target,
                "parameters": request.proposed_action.parameters,
            }

        )

        if isinstance(result, bool):

            return {
                "status": "approved" if result else "denied",
                "reason_code": "POLICY_EVALUATED"
            }

        if isinstance(result, dict):

            return {
                "status": result.get("status", "approved"),
                "reason_code": result.get(
                    "reason_code",
                    "POLICY_EVALUATED"
                )
            }

        return {
            "status": "approved",
            "reason_code": "POLICY_OK"
        }

    def evaluate_intent(self, request):

        return {
            "valid": True
        }

    def issue_capability(self, request):

        capability = issue_capability(

            principal=request.principal.actor_id,

            action=request.proposed_action.action_type

        )

        return {
            "jwt": capability.token,
            "constraints": {
                "single_use": capability.single_use,
                "expires_at": capability.expires_at,
            }
        }

    def collect_economics(self, request):

        return {
            "cost": 0.08,
            "budget_remaining": 9.92
        }

    def compute_health(self, request):

        return {
            "risk": 0.03,
            "trust": 0.99
        }

    def record_evidence(self, request, decision):

        return self.merkle.add(
            decision["receipt_hash"]
        )
