import random
import time

from pv_runtime_v2.trust_fabric.anomaly_detector import (
    AnomalyDetector,
)

from pv_runtime_v2.consensus.quarantine_manager import (
    QuarantineManager,
)


TOTAL_AGENTS = 10000
COMPROMISED = 500


def run():

    detector = (
        AnomalyDetector()
    )

    manager = (
        QuarantineManager()
    )

    trust_scores = [
        0.95
        for _ in range(
            TOTAL_AGENTS
        )
    ]

    compromised = random.sample(
        range(TOTAL_AGENTS),
        COMPROMISED,
    )

    for idx in compromised:

        trust_scores[idx] = 0.20

    start = (
        time.perf_counter()
    )

    quarantined = 0

    for score in trust_scores:

        if detector.compromised(
            score
        ):

            if manager.should_quarantine(
                score
            ):

                quarantined += 1

    elapsed = (
        time.perf_counter()
        - start
    ) * 1000

    print(
        f"detected={quarantined}"
    )

    print(
        f"latency={elapsed:.4f} ms"
    )


if __name__ == "__main__":
    run()
