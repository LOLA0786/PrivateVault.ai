from coordination.trust.trust_engine import TrustEngine

trust_engine = TrustEngine()

def update_agents(agent_votes, final_decision, policy_passed):
    for vote in agent_votes:

        # 🔥 Better correctness definition
        correct = (vote["decision"] == final_decision)
            vote["decision"] == final_decision
            and policy_passed
        )

        outcome = {
            "correct": correct,
            "policy_violation": not policy_passed and vote["decision"] == "APPROVE"
        }

        new_weight = trust_engine.update_trust(vote["agent_id"], outcome)
        print(f"[TRUST UPDATE] {vote['agent_id']} → {new_weight}")
