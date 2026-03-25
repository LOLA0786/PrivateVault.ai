from coordination.trust.update_after_decision import update_agents
from coordination.trust.trust_engine import TrustEngine

trust_engine = TrustEngine()

agent_votes = [
    {"agent_id": "pricing_agent", "decision": "APPROVE"},
    {"agent_id": "risk_agent", "decision": "APPROVE"},
    {"agent_id": "revenue_agent", "decision": "APPROVE"}
]

final_decision = "APPROVE"
policy_passed = True

print("=== BEFORE WEIGHTS ===")
for v in agent_votes:
    print(v["agent_id"], trust_engine.get_weight(v["agent_id"]))

update_agents(agent_votes, final_decision, policy_passed)

# reload
trust_engine = TrustEngine()

print("\n=== AFTER WEIGHTS ===")
for v in agent_votes:
    print(v["agent_id"], trust_engine.get_weight(v["agent_id"]))
