"""
Firewall Hook — emits an economics event on every firewall decision.
Drop this into policy_engine.py or ai_firewall_core.py at the decision
return point. Zero performance impact: runs async-style via a background
thread so it never adds latency to the sub-2ms enforcement path.
"""
import threading
from typing import Any, Dict, Optional

from pv_economics.integrations.outcome_bridge import OutcomeBridge

_bridge = OutcomeBridge()


def emit_firewall_economics(
    decision:       str,          # "ALLOW" / "BLOCK" / "REVIEW"
    agent:          str,
    action:         str,
    workflow:       str   = "",
    model:          str   = "",
    input_tokens:   int   = 0,
    output_tokens:  int   = 0,
    latency_ms:     float = 0.0,
    cost_usd:       float = 0.0,
    retries:        int   = 0,
    customer_id:    str   = "",
    policy_id:      str   = "",
    extras:         Optional[Dict] = None,
) -> None:
    """
    Non-blocking fire-and-forget.
    Call this at the end of every firewall decision — adds ~0ms to hot path.
    """
    def _emit():
        from pv_economics.events.outcome_event import ExecutionOutcome

        # Map firewall decision to outcome shape
        success = decision == "ALLOW"
        partial = decision == "REVIEW"

        outcome = ExecutionOutcome(
            success=success,
            partial=partial,
            business_result={},
            error_code=None if success else f"firewall_{decision.lower()}",
            error_severity="low" if decision == "REVIEW" else (
                "medium" if decision == "BLOCK" else None
            ),
        )

        _bridge.record(
            outcome=outcome,
            cost_usd=cost_usd,
            agent=agent,
            task=action,
            workflow=workflow,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=latency_ms,
            retries=retries,
            customer_id=customer_id,
            executions_per_day=10000.0,
        )

    t = threading.Thread(target=_emit, daemon=True)
    t.start()
