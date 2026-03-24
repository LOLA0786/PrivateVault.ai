from drift_aware_quorum import DriftAwareQuorum
from trust_registry import TrustRegistry
from decision_engine import MeshDecisionEngine
from agent_policy_engine import PolicyEngine
import hashlib
import json
from datetime import datetime, timezone

def run_scenario(amount):

    print("\n====================================")
    print(f"SCENARIO: Request Amount = ${amount}")
    print("====================================\n")

    policy_engine = PolicyEngine()

    request = {
        "action": "approve_discount",
        "amount": amount
    }

    ACTION_ID = f"deal_{amount}"

    # Trust
    trust = TrustRegistry()
    trust.set_score("pricing_agent", 0.9)
    trust.set_score("risk_agent", 0.7)
    trust.set_score("revenue_agent", 0.8)

    agents = ["pricing_agent", "risk_agent", "revenue_agent"]

    quorum = DriftAwareQuorum(threshold=1.5, trust_registry=trust)

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

        print(f"{agent} ({trust.get(agent):.1f}) → {decision}")
        print(f"   ↳ reason: {reason}")

    # Consensus
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

    # Policy
    MAX_DISCOUNT = 250000

    policy_pass = True
    policy_reason = "Within allowed limit"

    if request["amount"] > MAX_DISCOUNT:
        policy_pass = False
        policy_reason = "Discount exceeds 25% limit"

    print("\n=== POLICY CHECK ===")
    print(f"Policy Result: {'PASS' if policy_pass else 'FAIL'}")
    print(f"Reason: {policy_reason}")

    # Final
    if consensus == "APPROVE" and policy_pass:
        final_status = "ALLOW"
    else:
        final_status = "BLOCK"

    print("\n=== FINAL DECISION ===")
    print(final_status)

    # Proof
    payload = {
        "request": request,
        "agents": results,
        "consensus": consensus,
        "policy_pass": policy_pass,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    proof = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

    print("\n=== CRYPTO PROOF ===")
    print(proof)

    print("\nDecision Path:")
    print("Agent Policies → Consensus → Policy → Final Outcome")

    print("\n====================================\n")


print("\n=== PRIVATEVAULT: UNIFIED DEMO ===")

# 🔴 Scenario 1 → BLOCK
run_scenario(300000)

# 🟢 Scenario 2 → ALLOW
run_scenario(20000)

print("=== END OF DEMO ===\n")
