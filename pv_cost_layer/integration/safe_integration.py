from typing import Any, Dict, Callable
import os

from pv_cost_layer.integration.enforced_decision_wrapper import EnforcedDecisionWrapper
from pv_cost_layer.estimator.cost_estimator import Pricing
from pv_cost_layer.policies.cost_policy import CostPolicy


ENABLE_COST_CONTROL = os.getenv("PV_ENABLE_COST", "false").lower() == "true"


def wrap_decision(decision_fn: Callable[[Dict[str, Any]], Dict[str, Any]]):
    if not ENABLE_COST_CONTROL:
        return decision_fn

    wrapper = EnforcedDecisionWrapper(
        decision_fn=decision_fn,
        pricing=Pricing(
            input_per_token=float(os.getenv("PV_COST_INPUT", "0.000001")),
            output_per_token=float(os.getenv("PV_COST_OUTPUT", "0.000002")),
        ),
        cost_policy=CostPolicy(
            max_cost_per_action=float(os.getenv("PV_MAX_COST", "0.01")),
            max_daily_budget=float(os.getenv("PV_MAX_BUDGET", "100")),
        ),
        enable_cache=False,
    )

    return wrapper.decide
