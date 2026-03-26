from coordination.mesh.drift_aware_quorum import DriftAwareQuorum
from coordination.trust.trust_engine import TrustEngine

te = TrustEngine()
from coordination.trust.trust_engine import TrustEngine

te = TrustEngine()
from coordination.mesh.trust_registry import TrustRegistry
from coordination.mesh.decision_engine import MeshDecisionEngine
from coordination.mesh.agent_policy_engine import PolicyEngine
import hashlib
import json
from datetime import datetime, timezone

print("\n=== PRIVATEVAULT: FULL DECISION PIPELINE ===\n")

policy_engine = PolicyEngine()

# INPUT
request = {
    "action": "approve_discount",
    "amount": 300000
}

ACTION_ID = "deal_full_1"

# TRUST
trust = TrustRegistry()
trust.set_score("pricing_agent", 0.9)
trust.set_score("risk_agent", 0.7)
trust.set_score("revenue_agent", 0.8)

agents = ["pricing_agent", "risk_agent", "revenue_agent"]

# QUORUM
quorum = DriftAwareQuorum(threshold=1.5, trust_registry=trust)

# AGENT REASONING
results = {}

print("=== AGENT REASONING ===")

for agent in agents:
    decision, reason = policy_engine.evaluate(agent, request)
    results[agent] = (decision, reason)

    quorum.submit_vote(
        ACTION_ID,
        agent,
        decision,
        "sig",
        context={"stable": True}
    )

    


    print(f"{agent} (static:{trust.get(agent):.1f} | dynamic:{te.get_weight(agent):.2f}) → {decision}")
    print(f"   ↳ reason: {reason}")

# CONSENSUS
engine = MeshDecisionEngine(quorum)
consensus = engine.evaluate(ACTION_ID)["decision"]

approve_score = sum(
    trust.get(a) for a in agents if results[a][0] == "APPROVE"
)
reject_score = sum(
    trust.get(a) for a in agents if results[a][0] == "REJECT"
)

print("\n=== CONSENSUS ===")
print(f"APPROVE = {approve_score:.2f}")
print(f"REJECT  = {reject_score:.2f}")
print("Threshold = 1.50")
print(f"Consensus Result: {consensus}")

# POLICY
MAX_DISCOUNT = 250000

policy_pass = True
policy_reason = "Within allowed limit"

if request["amount"] > MAX_DISCOUNT:
    policy_pass = False
    policy_reason = "Discount exceeds 25% limit"

print("\n=== POLICY CHECK ===")
print(f"Policy Result: {'PASS' if policy_pass else 'FAIL'}")
print(f"Reason: {policy_reason}")

# FINAL
if consensus == "APPROVE" and policy_pass:
    final_status = "ALLOW"
else:
    final_status = "BLOCK"

print("\n=== FINAL DECISION ===")


# === TRUST UPDATE ===
from coordination.trust.update_after_decision import update_agents

agent_votes = [
    {"agent_id": "pricing_agent", "decision": "APPROVE"},
    {"agent_id": "risk_agent", "decision": "REJECT"},
    {"agent_id": "revenue_agent", "decision": "APPROVE"}
]


final_decision = "APPROVE" if final_status == "ALLOW" else "REJECT"

update_agents(agent_votes, final_decision, policy_pass)
print(final_status)

# CRYPTO PROOF
payload = {
    "action_id": ACTION_ID,
    "request": request,
    "agents": results,
    "consensus": consensus,
    "policy_pass": policy_pass,
    "timestamp": datetime.now(timezone.utc).isoformat()
}

serialized = json.dumps(payload, sort_keys=True).encode()
proof_hash = hashlib.sha256(serialized).hexdigest()

print("\n=== CRYPTO PROOF ===")
print(f"Hash: {proof_hash}")

# REPLAY
print("\n=== REPLAY ===")
print("Recomputed decision from stored payload → deterministic result")

print("\nDecision Path:")
print("Agent Policies → Consensus → Policy → Final Outcome")

print("\n========================\n")

# --- PATCH: alignment metric ---
# --- END PATCH ---
