import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from decision_integrity.builders.snapshot_builder import (
    build_snapshot
)

from decision_integrity.builders.decision_authorization import (
    authorize_decision
)

from decision_integrity.builders.decision_contract_builder import (
    build_decision_contract
)

s = build_snapshot(
    actor_id="user",
    agent_id="loan-agent",
    intent_text="approve loan",
    policy_version="v17",
    policy_hash="policy17",
    trust_score=0.99,
    capability_tokens=[
        "LOAN_APPROVAL"
    ]
)

authorize_decision(s)

contract = build_decision_contract(s)

print("decision_id:", contract.decision_id)
print("authorized:", contract.authorized)
print("outcome:", contract.outcome)
print("PASS")
