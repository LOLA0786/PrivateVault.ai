from trust_fabric.trust_evaluator import TrustEvaluator
from consensus.consensus_engine import ConsensusEngine
from economics.economics_engine import EconomicsEngine

from runtime.request_contract import RuntimeRequest
from runtime.decision_contract import RuntimeDecision


class RuntimePipeline:

    def __init__(self):

        self.trust = TrustEvaluator()

        self.consensus = ConsensusEngine()

        self.economics = EconomicsEngine()

    def execute(
        self,
        request,
        trust_state
    ):

        trust_score = self.trust.evaluate(
            trust_state
        )

        consensus_score = (
            self.consensus.evaluate(
                trust_score
            )
        )

        economic_score = (
            self.economics.evaluate(
                trust_score,
                consensus_score
            )
        )

        approved = (
            economic_score >= 0.75
        )

        return RuntimeDecision(
            request_id=request.request_id,
            agent_id=request.agent_id,
            capability=request.capability,
            trust_score=trust_score,
            consensus_score=consensus_score,
            economic_score=economic_score,
            approved=approved,
            evidence_hash="pending"
        )
