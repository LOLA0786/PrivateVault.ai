from coordination.trust.trust_engine import TrustEngine

trust_engine = TrustEngine()

def compute_weighted_consensus(agent_votes):
    scores = {"APPROVE": 0.0, "REJECT": 0.0}

    for vote in agent_votes:
        weight = trust_engine.get_weight(vote["agent_id"])
        scores[vote["decision"]] += weight

    return scores
