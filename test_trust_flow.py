from coordination.trust.update_after_decision import update_agents
from coordination.trust.trust_engine import TrustEngine

agent_votes = [
    {"agent_id": "pricing_agent", "decision": "APPROVE"},
    {"agent_id": "risk_agent", "decision": "REJECT"},
    {"agent_id": "revenue_agent", "decision": "APPROVE"}
]

final_decision = "BLOCK"
policy_passed = False

trust_engine = TrustEngine()

print("=== BEFORE WEIGHTS ===")
for v in agent_votes:
    print(v["agent_id"], trust_engine.get_weight(v["agent_id"]))

update_agents(agent_votes, final_decision, policy_passed)

# 🔥 RELOAD ENGINE (important)
trust_engine = TrustEngine()

print("\n=== AFTER WEIGHTS ===")
for v in agent_votes:
    print(v["agent_id"], trust_engine.get_weight(v["agent_id"]))
