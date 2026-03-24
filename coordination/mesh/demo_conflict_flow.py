from drift_aware_quorum import DriftAwareQuorum
from trust_registry import TrustRegistry
from decision_engine import MeshDecisionEngine
from agent_policy_engine import PolicyEngine

print("\n=== MULTI-AGENT CONFLICT DEMO (WITH EXPLANATION) ===\n")

policy_engine = PolicyEngine()

request = {
    "action": "approve_discount",
    "amount": 300000
}

# Trust
trust = TrustRegistry()
trust.set_score("pricing_agent", 0.9)
trust.set_score("risk_agent", 0.7)
trust.set_score("revenue_agent", 0.8)

# Quorum
quorum = DriftAwareQuorum(threshold=1.5, trust_registry=trust)

agents = ["pricing_agent", "risk_agent", "revenue_agent"]

results = {}

for agent in agents:
    decision, reason = policy_engine.evaluate(agent, request)
    results[agent] = (decision, reason)

    quorum.submit_vote(
        "deal_conflict",
        agent,
        decision,
        "sig",
        context={"stable": True}
    )

# Final decision
engine = MeshDecisionEngine(quorum)
decision = engine.evaluate("deal_conflict")

print("=== AGENT DECISIONS ===")

for agent in agents:
    d, r = results[agent]
    trust_score = trust.get(agent)
    print(f"{agent} ({trust_score:.1f}) → {d}")
    print(f"   ↳ reason: {r}")

approve_score = sum(
    trust.get(a) for a in agents if results[a][0] == "APPROVE"
)
reject_score = sum(
    trust.get(a) for a in agents if results[a][0] == "REJECT"
)

print("\n=== SCORE BREAKDOWN ===")
print(f"APPROVE = {approve_score:.2f}")
print(f"REJECT  = {reject_score:.2f}")
print("Threshold = 1.50")

print("\n=== FINAL DECISION ===")
print(decision["decision"])

print("\nExplanation:")
print("Decision derived from policy-driven agent reasoning + trust-weighted consensus")

print("\nDecision Path: Agent Policies → Consensus → Final Outcome")

print("\n========================\n")
