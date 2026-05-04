from typing import Dict, Any, Callable

from pv_core.safety.execution_gate import allow_execution
from pv_cost_layer.policies.cost_policy import CostPolicy


POLICY = CostPolicy(max_cost_per_action=0.01, max_daily_budget=100)

COST_MAP = {
    "gpt": 0.012,
    "grok": 0.004,
    "local": 0.000,
}

FALLBACK_ORDER = ["gpt", "grok", "local"]


def get_candidates(provider: str):
    if provider not in FALLBACK_ORDER:
        return FALLBACK_ORDER
    idx = FALLBACK_ORDER.index(provider)
    return FALLBACK_ORDER[idx:]


def execute_with_controls(execute_fn: Callable[[Dict[str, Any]], Dict[str, Any]],
                          context: Dict[str, Any]) -> Dict[str, Any]:

    action = context.get("action", context)

    # rate limit
    if not allow_execution(action):
        return {"executed": False, "blocked": True, "reason": "rate_limited"}

    provider = context.get("provider", "gpt")
    candidates = get_candidates(provider)

    for p in candidates:
        predicted_cost = COST_MAP.get(p, 0.01)

        if predicted_cost > POLICY.max_cost_per_action:
            continue

        new_context = dict(context)
        new_context["provider"] = p

        result = execute_fn(new_context)

        # success case
        if result.get("success", False):
            result["used_provider"] = p
            result["predicted_cost"] = predicted_cost
            result["attempt_chain"] = candidates
            return result

    # if all fail
    return {
        "executed": False,
        "blocked": True,
        "reason": "all_providers_failed_or_expensive",
        "attempt_chain": candidates,
    }
