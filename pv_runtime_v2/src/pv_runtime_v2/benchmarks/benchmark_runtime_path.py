import time

from pv_runtime_v2.trust_fabric.trust_state import TrustState
from pv_runtime_v2.runtime.request_contract import RuntimeRequest
from pv_runtime_v2.runtime.runtime_pipeline import RuntimePipeline


def run():

    pipeline = RuntimePipeline()

    trust = TrustState(
        agent_id="agent-1",
        trust_score=0.95,
        risk_score=0.05,
        policy_version="v1",
        capability_hash="abc"
    )

    start = time.perf_counter()

    for i in range(10000):

        request = RuntimeRequest(
            request_id=str(i),
            agent_id="agent-1",
            capability="approve_loan",
            payload_hash="xyz"
        )

        pipeline.execute(
            request,
            trust
        )

    elapsed = (
        time.perf_counter()
        - start
    ) * 1000

    print(f"10000 decisions: {elapsed:.4f} ms")


if __name__ == "__main__":
    run()
