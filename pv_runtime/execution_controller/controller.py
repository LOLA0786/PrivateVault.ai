import time

from typing import Dict, Any

from pv_runtime.retry.retry_engine import RetryEngine
from pv_runtime.wallet.wallet_engine import WalletEngine
from pv_runtime.context_graph.graph_engine import ContextGraph
from pv_runtime.tool_firewall.tool_validator import ToolValidator
from pv_runtime.rollback.rollback_engine import RollbackEngine
from pv_runtime.idempotency.idempotency_store import IdempotencyStore
from pv_runtime.event_store.event_store import EventStore
from pv_runtime.locks.lock_manager import LockManager

from pv_economics.events.outcome_event import build_outcome_event

from pv_runtime.telemetry.runtime_metrics import RuntimeMetrics

retry_engine = RetryEngine()


class ExecutionController:

    def __init__(self):
        self.wallet = WalletEngine()
        self.graph = ContextGraph()
        self.tool_validator = ToolValidator()
        self.rollback_engine = RollbackEngine()
        self.idempotency = IdempotencyStore()
        self.event_store = EventStore()
        self.lock_manager = LockManager()

    def execute_context(self, runtime_context):
        """
        Transitional API.

        Accepts the immutable RuntimeContext and delegates to the
        existing execute() implementation.
        """

        return self.execute(
            agent_id=runtime_context.agent_id,
            action=dict(runtime_context.intent),
        )

    def execute(
        self,
        agent_id: str,
        action: Dict[str, Any],
    ) -> Dict[str, Any]:

        self.event_store.append_event(
            "ACTION_REQUESTED",
            {
                "agent": agent_id,
                "action": action,
            },
        )

        lock_key = f"{action.get('action')}:{action.get('recipient')}"

        def _execute():

            started = time.perf_counter()

            metrics = RuntimeMetrics()

            try:

                #
                # IDEMPOTENCY
                #

                id_check = self.idempotency.check_or_store(
                    agent_id,
                    action,
                )

                if id_check.get("duplicate"):

                    metrics.latency_ms = (
                        time.perf_counter() - started
                    ) * 1000

                    return {
                        "status": "DUPLICATE",
                        "cached_result": id_check["result"],
                        "metrics": metrics,
                    }

                #
                # CONTEXT GRAPH
                #

                self.graph.record_intent(
                    agent_id,
                    action,
                )

                #
                # WALLET
                #

                if not self.wallet.is_within_budget(
                    agent_id,
                    action,
                ):

                    metrics.latency_ms = (
                        time.perf_counter() - started
                    ) * 1000

                    return {
                        "status": "BLOCK",
                        "reason": "Budget exceeded",
                        "metrics": metrics,
                    }

                #
                # TOOL VALIDATION
                #

                metrics.total_tool_calls += 1

                validation = self.tool_validator.validate(
                    action
                )

                if validation["valid"]:
                    metrics.useful_tool_calls += 1

                if not validation["valid"]:

                    metrics.latency_ms = (
                        time.perf_counter() - started
                    ) * 1000

                    return {
                        "status": "BLOCK",
                        "reason": validation["reason"],
                        "metrics": metrics,
                    }

                #
                # EXECUTION
                #

                result = self._execute_action(action)

                outcome = build_outcome_event(
                    success=True,
                    business_result={
                        "action": action.get("action"),
                        "business_value": 0,
                    },
                    metrics={},
                )

                self.event_store.append_event(
                    "EXECUTION_OUTCOME",
                    {
                        "agent": agent_id,
                        "outcome": outcome.__dict__,
                    },
                )

                self.graph.record_outcome(
                    agent_id,
                    action,
                    result,
                )

                self.event_store.append_event(
                    "ACTION_EXECUTED",
                    {
                        "agent": agent_id,
                        "action": action,
                        "result": result,
                    },
                )

                self.idempotency.check_or_store(
                    agent_id,
                    action,
                    result,
                )

                metrics.latency_ms = (
                    time.perf_counter() - started
                ) * 1000

                return {
                    "status": "SUCCESS",
                    "result": result,
                    "metrics": metrics,
                }

            except Exception as e:

                rollback_result = self.rollback_engine.rollback(
                    action
                )

                metrics.rollbacks += 1

                metrics.latency_ms = (
                    time.perf_counter() - started
                ) * 1000

                self.event_store.append_event(
                    "ACTION_FAILED",
                    {
                        "agent": agent_id,
                        "action": action,
                        "error": str(e),
                        "rollback": rollback_result,
                    },
                )

                return {
                    "status": "FAILED",
                    "error": str(e),
                    "rollback": rollback_result,
                    "metrics": metrics,
                }

        return retry_engine.execute_with_retry(
            lambda: self.lock_manager.execute_with_lock(
                lock_key,
                _execute,
            )
        )

    def _execute_action(
        self,
        action: Dict[str, Any],
    ):

        time.sleep(0.05)

        if action.get("fail"):
            raise Exception("Simulated failure")

        return {
            "executed": True,
            "action": action,
        }
