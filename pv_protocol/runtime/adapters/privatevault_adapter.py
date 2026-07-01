from datetime import UTC, datetime

from privatevault.evidence.merkle_chain import MerkleChain

from pv_core.policy.policy_service import evaluate
from pv_core.intent.intent_service import normalize

from pv_runtime.capability_issuer import issue_capability

from pv_runtime_v2.economics.economics_engine import EconomicsEngine
from pv_runtime_v2.consensus.health_calculator import HealthCalculator


class PrivateVaultAdapter:

    def __init__(self):

        self.merkle = MerkleChain()

        self.economics = EconomicsEngine()

        self.health = HealthCalculator()

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

        return normalize(
            {
                "action": request.proposed_action.action_type,
                "goal": request.goal.description,
            },
            request.principal.actor_id,
        )

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

        score = self.economics.evaluate(
            trust_score=0.99,
            consensus_score=0.98,
        )

        return {
            "economics_score": score,
            "budget_remaining": 9.92,
        }

    def compute_health(self, request):

        health = self.health.evaluate(
            cluster_id=request.loop.loop_id,
            healthy_agents=10,
            quarantined_agents=0,
        )

        return {
            "cluster_id": health.cluster_id,
            "health_score": health.health_score,
            "healthy_agents": health.healthy_agents,
            "quarantined_agents": health.quarantined_agents,
        }

    def record_evidence(self, request, decision):

        return self.merkle.add(
            decision["receipt_hash"]
        )
