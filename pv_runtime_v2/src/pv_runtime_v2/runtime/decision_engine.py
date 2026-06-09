from pv_runtime_v2.trust_fabric.local_enforcer import LocalEnforcer
from pv_runtime_v2.consensus.weighted_quorum import WeightedQuorum
from pv_runtime_v2.evidence.evidence_chain import EvidenceChain


class DecisionEngine:

    def __init__(self):

        self.enforcer = LocalEnforcer()
        self.quorum = WeightedQuorum()

    def authorize(
        self,
        trust_state,
        capability_token,
        capability,
        votes,
    ):

        if not self.enforcer.authorize(
            trust_state,
            capability_token,
            capability,
        ):
            return False

        return self.quorum.approved(
            votes
        )
