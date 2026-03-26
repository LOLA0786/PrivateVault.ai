from coordination.trust.trust_engine import TrustEngine

trust_engine = TrustEngine()

def compute_weighted_consensus(agent_votes):
    scores = {"APPROVE": 0.0, "REJECT": 0.0}

    for vote in agent_votes:
        weight = trust_engine.get_weight(vote["agent_id"])
        scores[vote["decision"]] += weight

    return scores

# --- PATCH: pre-consensus penalty & reward ---

# --- PATCH: pre-consensus penalty & reward ---
def _adjust_weight(agent):
    w = _adjust_weight(agent)
    last = getattr(agent, "last_outcome", {}) or {}

    if last.get("policy_violation"):
        w *= 0.5
    if last.get("correct"):
        w *= 1.15

    return w
# --- END PATCH ---
