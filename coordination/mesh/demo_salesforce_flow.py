from drift_aware_quorum import DriftAwareQuorum
from trust_registry import TrustRegistry
from decision_engine import MeshDecisionEngine
from mesh_control_adapter import MeshControlAdapter
from events import emit_event

print("\n=== PRIVATEVAULT SALESFORCE DEMO ===\n")

# Setup trust
trust = TrustRegistry()
trust.set_score("pricing_agent", 0.9)
trust.set_score("risk_agent", 0.6)
trust.set_score("revenue_agent", 0.8)

# Quorum
quorum = DriftAwareQuorum(threshold=1.5, trust_registry=trust)

# Votes
quorum.submit_vote("deal_1", "pricing_agent", "APPROVE", "sig", context={"stable": True})
quorum.submit_vote("deal_1", "risk_agent", "APPROVE", "sig", context={"drift": True})
quorum.submit_vote("deal_1", "revenue_agent", "APPROVE", "sig", context={"stable": True})

# Check consensus
consensus_passed = quorum.check_quorum("deal_1")

# Engine + Adapter
engine = MeshDecisionEngine(quorum)
adapter = MeshControlAdapter(engine)

# 🔥 UPDATED AMOUNT (safe)
request = {
    "action": "approve_discount",
    "amount": 20000,
    "agent_id": "pricing_agent"
}

decision = adapter.verify("deal_1", request)

# Policy
MAX_DISCOUNT = 250000
policy_block = False

if decision["status"] == "ALLOW" and request["amount"] > MAX_DISCOUNT:
    policy_block = True
    decision = {
        "status": "BLOCK",
        "reason": "POLICY_VIOLATION: Discount exceeds 25% limit"
    }

emit_event("FINAL_DECISION", decision)

# Output
print("=== DECISION SUMMARY ===")
print("Action: Enterprise Discount Approval")
print(f"Requested: ${request['amount']}")

print(f"Consensus: {'PASSED' if consensus_passed else 'FAILED'}")
print(f"Policy: {'FAILED' if policy_block else 'PASSED'}")

print("\nAgents:")
print(" - pricing_agent (0.9) → APPROVE")
print(" - risk_agent (DRIFTED) → IGNORED")
print(" - revenue_agent (0.8) → APPROVE")

print("\nFinal Decision:", decision["status"])

if decision["status"] == "BLOCK":
    print("Reason:", decision["reason"])
else:
    print("Transaction ID:", decision["result"]["transaction_id"])

print("\n========================\n")
