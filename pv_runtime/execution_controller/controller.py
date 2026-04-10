
from typing import Dict, Any

from pv_runtime.wallet.wallet_engine import WalletEngine
from pv_runtime.context_graph.graph_engine import ContextGraph
from pv_runtime.tool_firewall.tool_validator import ToolValidator
from pv_runtime.rollback.rollback_engine import RollbackEngine
from pv_runtime.idempotency.idempotency_store import IdempotencyStore
from pv_runtime.event_store.event_store import EventStore
from pv_runtime.locks.lock_manager import LockManager


class ExecutionController:

    def __init__(self):
        self.wallet = WalletEngine()
        self.graph = ContextGraph()
        self.tool_validator = ToolValidator()
        self.rollback_engine = RollbackEngine()
        self.idempotency = IdempotencyStore()
        self.event_store = EventStore()
        self.lock_manager = LockManager()

    def execute(self, agent_id: str, action: Dict[str, Any]) -> Dict[str, Any]:

        id_check = self.idempotency.check_or_store(agent_id, action)
        if id_check.get("duplicate"):
            return {
                "status": "DUPLICATE",
                "cached_result": id_check["result"]
            }

        self.event_store.append_event(
            "ACTION_REQUESTED",
            {"agent": agent_id, "action": action}
        )

        lock_key = f"{agent_id}:{action.get('action')}"

        def _execute():
            try:
                self.graph.record_intent(agent_id, action)

                if not self.wallet.is_within_budget(agent_id, action):
                    self.event_store.append_event(
                        "ACTION_BLOCKED",
                        {"agent": agent_id, "action": action, "reason": "budget"}
                    )
                    return {"status": "BLOCK", "reason": "Budget exceeded"}

                validation = self.tool_validator.validate(action)
                if not validation["valid"]:
                    self.event_store.append_event(
                        "ACTION_BLOCKED",
                        {"agent": agent_id, "action": action, "reason": validation["reason"]}
                    )
                    return {"status": "BLOCK", "reason": validation["reason"]}

                result = self._execute_action(action)

                self.graph.record_outcome(agent_id, action, result)

                self.event_store.append_event(
                    "ACTION_EXECUTED",
                    {"agent": agent_id, "action": action, "result": result}
                )

                self.idempotency.check_or_store(agent_id, action, result)

                return {"status": "SUCCESS", "result": result}

            except Exception as e:
                rollback_result = self.rollback_engine.rollback(action)

                self.event_store.append_event(
                    "ACTION_FAILED",
                    {
                        "agent": agent_id,
                        "action": action,
                        "error": str(e),
                        "rollback": rollback_result
                    }
                )

                return {
                    "status": "FAILED",
                    "error": str(e),
                    "rollback": rollback_result
                }

        return self.lock_manager.execute_with_lock(lock_key, _execute)

    def _execute_action(self, action: Dict[str, Any]):
        # 🔥 Proper failure injection
        if action.get("fail"):
            raise Exception("Simulated failure")

        return {
            "executed": True,
            "action": action
        }

