import time
from datetime import datetime, timedelta

from pv_runtime_v2.trust_fabric.trust_state import TrustState
from pv_runtime_v2.trust_fabric.capability_token import CapabilityToken

from pv_runtime_v2.consensus.weighted_quorum import (
    Vote,
)

from pv_runtime_v2.runtime.decision_engine import (
    DecisionEngine,
)

from pv_runtime_v2.evidence.evidence_chain import (
    EvidenceChain,
)


def run():

    trust = TrustState(
        agent_id="agent-1",
        trust_score=0.95,
        risk_score=0.01,
        policy_version="v1",
        capability_hash="abc",
        updated_at=datetime.utcnow(),
    )

    token = CapabilityToken(
        token_id="tok-1",
        agent_id="agent-1",
        capabilities=frozenset(
            {"approve_loan"}
        ),
        issued_at=datetime.utcnow(),
        expires_at=datetime.utcnow()
        + timedelta(hours=1),
        signature="sig",
    )

    votes = [
        Vote(weight=1.0, approve=True),
        Vote(weight=1.0, approve=True),
        Vote(weight=1.0, approve=True),
    ]

    engine = DecisionEngine()

    start = time.perf_counter()

    for _ in range(100000):

        engine.authorize(
            trust,
            token,
            "approve_loan",
            votes,
        )

        EvidenceChain.hash_event(
            "root",
            "payload",
        )

    elapsed = (
        time.perf_counter()
        - start
    ) * 1000

    print(
        f"100000 decisions = {elapsed:.2f} ms"
    )


if __name__ == "__main__":
    run()
