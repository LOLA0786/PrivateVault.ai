import json

from datetime import datetime

from pv_economics.metrics.economics_metrics import (
    agent_cost_total,
    agent_success_total,
    agent_failure_total,
    agent_waste_score,
    agent_roi_score
)


class EconomicsCollector:

    FILE = "economics_events.jsonl"

    def record(self, event):

        payload = {
            "timestamp":
                datetime.utcnow().isoformat(),

            **event
        }

        with open(
            self.FILE,
            "a"
        ) as f:

            f.write(
                json.dumps(payload)
                + "\n"
            )

        agent = event.get(
            "agent",
            "unknown"
        )

        cost = float(
            event.get(
                "cost_usd",
                0
            )
        )

        agent_cost_total.labels(
            agent=agent
        ).inc(cost)

        if event.get(
            "success",
            False
        ):
            agent_success_total.labels(
                agent=agent
            ).inc()
        else:
            agent_failure_total.labels(
                agent=agent
            ).inc()

        agent_waste_score.labels(
            agent=agent
        ).set(
            float(
                event.get(
                    "waste_score",
                    0
                )
            )
        )

        agent_roi_score.labels(
            agent=agent
        ).set(
            float(
                event.get(
                    "roi_score",
                    0
                )
            )
        )
