"""
Economics Store — SQLite for durable records, Redis for live aggregates.
Falls back to SQLite-only if Redis is unavailable.
"""
import json
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any

try:
    import redis
    _REDIS_AVAILABLE = True
except ImportError:
    _REDIS_AVAILABLE = False


DB_PATH = Path("pv_economics_store.db")


class EconomicsStore:

    _lock = threading.Lock()

    def __init__(
        self,
        db_path:    Path = DB_PATH,
        redis_url:  str  = "redis://localhost:6379/2",
    ):
        self.db_path  = db_path
        self._redis   = None

        if _REDIS_AVAILABLE:
            try:
                self._redis = redis.from_url(redis_url, decode_responses=True)
                self._redis.ping()
            except Exception:
                self._redis = None

        self._init_db()

    # ------------------------------------------------------------------
    # Schema
    # ------------------------------------------------------------------

    def _init_db(self):
        with self._conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS executions (
                    id            INTEGER PRIMARY KEY AUTOINCREMENT,
                    ts            TEXT    NOT NULL,
                    agent         TEXT    NOT NULL,
                    workflow      TEXT,
                    task          TEXT,
                    model         TEXT,
                    input_tokens  INTEGER DEFAULT 0,
                    output_tokens INTEGER DEFAULT 0,
                    latency_ms    REAL    DEFAULT 0,
                    retries       INTEGER DEFAULT 0,
                    cost_usd      REAL    DEFAULT 0,
                    success       INTEGER DEFAULT 0,
                    waste_score   REAL    DEFAULT 0,
                    roi_score     REAL    DEFAULT 0,
                    econ_score    REAL    DEFAULT 0,
                    econ_grade    TEXT,
                    customer_id   TEXT,
                    extras        TEXT
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_agent_ts
                ON executions (agent, ts)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_workflow
                ON executions (workflow, ts)
            """)

    def _conn(self):
        return sqlite3.connect(self.db_path)

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def record(self, event: Dict[str, Any]) -> int:
        ts = datetime.now(timezone.utc).isoformat()

        with self._lock, self._conn() as conn:
            cur = conn.execute("""
                INSERT INTO executions
                    (ts, agent, workflow, task, model,
                     input_tokens, output_tokens, latency_ms, retries,
                     cost_usd, success, waste_score, roi_score,
                     econ_score, econ_grade, customer_id, extras)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                ts,
                event.get("agent",         "unknown"),
                event.get("workflow",       ""),
                event.get("task",           ""),
                event.get("model",          ""),
                event.get("input_tokens",   0),
                event.get("output_tokens",  0),
                event.get("latency_ms",     0.0),
                event.get("retries",        0),
                event.get("cost_usd",       0.0),
                int(event.get("success",    False)),
                event.get("waste_score",    0.0),
                event.get("roi_score",      0.0),
                event.get("econ_score",     0.0),
                event.get("econ_grade",     ""),
                event.get("customer_id",    ""),
                json.dumps(event.get("extras", {})),
            ))
            row_id = cur.lastrowid

        # Live Redis aggregates
        if self._redis:
            agent = event.get("agent", "unknown")
            pipe  = self._redis.pipeline()
            pipe.incrbyfloat(f"pv:econ:agent:{agent}:cost",    event.get("cost_usd", 0))
            pipe.incr(       f"pv:econ:agent:{agent}:runs")
            pipe.incrbyfloat(f"pv:econ:agent:{agent}:waste",   event.get("waste_score", 0))
            pipe.incrbyfloat(f"pv:econ:agent:{agent}:roi",     event.get("roi_score",   0))
            pipe.incr(       f"pv:econ:agent:{agent}:success", event.get("success", 0))
            pipe.expire(     f"pv:econ:agent:{agent}:cost",    86400 * 7)
            pipe.execute()

        return row_id

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def get_agent_summary(self, agent: str, days: int = 7) -> Dict[str, Any]:
        """Aggregated stats for one agent over the last N days."""
        with self._conn() as conn:
            row = conn.execute("""
                SELECT
                    COUNT(*)                      AS runs,
                    SUM(cost_usd)                 AS total_cost,
                    AVG(cost_usd)                 AS avg_cost,
                    SUM(success)                  AS successes,
                    AVG(waste_score)              AS avg_waste,
                    AVG(roi_score)                AS avg_roi,
                    AVG(econ_score)               AS avg_econ_score,
                    AVG(latency_ms)               AS avg_latency_ms,
                    SUM(input_tokens + output_tokens) AS total_tokens
                FROM executions
                WHERE agent = ?
                  AND ts >= datetime('now', ?)
            """, (agent, f"-{days} days")).fetchone()

        if not row or row[0] == 0:
            return {"agent": agent, "runs": 0}

        runs = row[0] or 0
        return {
            "agent":          agent,
            "runs":           runs,
            "total_cost_usd": round(row[1] or 0, 6),
            "avg_cost_usd":   round(row[2] or 0, 6),
            "success_rate":   round((row[3] or 0) / max(runs, 1), 4),
            "avg_waste":      round(row[4] or 0, 2),
            "avg_roi":        round(row[5] or 0, 4),
            "avg_econ_score": round(row[6] or 0, 2),
            "avg_latency_ms": round(row[7] or 0, 2),
            "total_tokens":   row[8] or 0,
        }

    def get_workflow_summary(
        self, workflow: str, days: int = 7
    ) -> Dict[str, Any]:
        with self._conn() as conn:
            rows = conn.execute("""
                SELECT
                    agent,
                    COUNT(*)        AS runs,
                    SUM(cost_usd)   AS cost,
                    AVG(waste_score) AS waste,
                    SUM(success)    AS successes
                FROM executions
                WHERE workflow = ?
                  AND ts >= datetime('now', ?)
                GROUP BY agent
            """, (workflow, f"-{days} days")).fetchall()

        return {
            "workflow": workflow,
            "agents": [
                {
                    "agent":        r[0],
                    "runs":         r[1],
                    "cost_usd":     round(r[2] or 0, 6),
                    "avg_waste":    round(r[3] or 0, 2),
                    "success_rate": round((r[4] or 0) / max(r[1], 1), 4),
                }
                for r in rows
            ],
        }

    def get_recent(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self._conn() as conn:
            rows = conn.execute("""
                SELECT ts, agent, workflow, task, cost_usd,
                       success, waste_score, roi_score, econ_score, econ_grade
                FROM executions
                ORDER BY ts DESC
                LIMIT ?
            """, (limit,)).fetchall()

        cols = ["ts","agent","workflow","task","cost_usd",
                "success","waste_score","roi_score","econ_score","econ_grade"]
        return [dict(zip(cols, r)) for r in rows]
