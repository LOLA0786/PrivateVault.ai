from pv_runtime.retry.retry_engine import RetryEngine
retry_engine = RetryEngine()

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

        self.event_store.append_event(
            "ACTION_REQUESTED",
            {"agent": agent_id, "action": action}
        )

        lock_key = f"{action.get('action')}:{action.get('recipient')}"

        def _execute():
            try:
                # ✅ IDEMPOTENCY INSIDE LOCK
                id_check = self.idempotency.check_or_store(agent_id, action)
                if id_check.get("duplicate"):
                    return {
                        "status": "DUPLICATE",
                        "cached_result": id_check["result"]
                    }

                # CONTEXT GRAPH
                self.graph.record_intent(agent_id, action)

                # WALLET CHECK
                if not self.wallet.is_within_budget(agent_id, action):
                    return {"status": "BLOCK", "reason": "Budget exceeded"}

                # TOOL VALIDATION
                validation = self.tool_validator.validate(action)
                if not validation["valid"]:
                    return {"status": "BLOCK", "reason": validation["reason"]}

                # EXECUTION
                result = self._execute_action(action)

                self.graph.record_outcome(agent_id, action, result)

                self.event_store.append_event(
                    "ACTION_EXECUTED",
                    {"agent": agent_id, "action": action, "result": result}
                )

                # STORE IDEMPOTENCY RESULT
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

        return retry_engine.execute_with_retry(lambda: self.lock_manager.execute_with_lock(lock_key, _execute))

    def _execute_action(self, action: Dict[str, Any]):
        import time; time.sleep(0.05)

        if action.get("fail"):
            raise Exception("Simulated failure")

        return {
            "executed": True,
            "action": action
        }
