"""
Economics Collector — single write path for all execution economics.
Writes to SQLite store + Prometheus. JSONL retained as secondary audit log.
"""
import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from pv_economics.metrics.economics_metrics import (
    agent_cost_total,
    agent_success_total,
    agent_failure_total,
    agent_waste_score,
    agent_roi_score,
)
from pv_economics.storage.economics_store import EconomicsStore

_store = EconomicsStore()


class EconomicsCollector:

    JSONL_FILE = "economics_events.jsonl"

    def __init__(self, store: Optional[EconomicsStore] = None):
        self._store = store or _store

    def record(self, event: Dict[str, Any]) -> int:
        """
        Record a complete economics event.
        Returns the store row ID.
        """
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **event,
        }

        # JSONL audit trail (append-only, immutable)
        with open(self.JSONL_FILE, "a") as f:
            f.write(json.dumps(payload) + "\n")

        # Durable store
        row_id = self._store.record(event)

        # Prometheus live metrics
        agent = event.get("agent", "unknown")

        agent_cost_total.labels(agent=agent).inc(
            float(event.get("cost_usd", 0))
        )

        if event.get("success", False):
            agent_success_total.labels(agent=agent).inc()
        else:
            agent_failure_total.labels(agent=agent).inc()

        agent_waste_score.labels(agent=agent).set(
            float(event.get("waste_score", 0))
        )
        agent_roi_score.labels(agent=agent).set(
            float(event.get("roi_score", 0))
        )

        return row_id
