from decision_engine import MeshDecisionEngine
from weighted_quorum import WeightedQuorum
from trust_registry import TrustRegistry
from mesh_control_adapter import MeshControlAdapter

# setup trust
trust = TrustRegistry()
trust.set_score("A", 0.9)
trust.set_score("B", 0.8)

# quorum
quorum = WeightedQuorum(threshold=1.5, trust_registry=trust)

# votes
quorum.submit_vote("tx1", "A", "APPROVE", "sig")
quorum.submit_vote("tx1", "B", "APPROVE", "sig")

# engine
engine = MeshDecisionEngine(quorum)

# adapter
adapter = MeshControlAdapter(engine)

# mock request
request = {
    "action": "transfer",
    "amount": 10000,
    "agent_id": "A"
}

print(adapter.verify("tx1", request))
