from coordination.mesh.weighted_quorum import WeightedQuorum
from coordination.mesh.trust_registry import TrustRegistry
from coordination.mesh.decision_engine import MeshDecisionEngine
from coordination.mesh.mesh_control_adapter import MeshControlAdapter

# trust setup
trust = TrustRegistry()
trust.set_score("agent_A", 0.9)
trust.set_score("agent_B", 0.8)

# quorum
quorum = WeightedQuorum(threshold=1.5, trust_registry=trust)

# votes
quorum.submit_vote("tx100", "agent_A", "APPROVE", "sig")
quorum.submit_vote("tx100", "agent_B", "APPROVE", "sig")

# engine + adapter
engine = MeshDecisionEngine(quorum)
adapter = MeshControlAdapter(engine)

# action
request = {
    "action": "transfer",
    "amount": 50000,
    "agent_id": "agent_A"
}

decision = adapter.verify("tx100", request)

print("FINAL DECISION:")
print(decision)
