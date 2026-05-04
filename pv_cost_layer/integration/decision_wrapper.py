from typing import Any, Dict, Callable, Optional

from pv_cost_layer.estimator.cost_estimator import CostEstimator, Pricing
from pv_cost_layer.router.model_router import ModelRouter
from pv_cost_layer.metrics.cost_metrics import CostMetrics
from pv_cost_layer.cache.decision_cache import DecisionCache
from pv_cost_layer.types import CostContext


class DecisionWrapper:
    def __init__(
        self,
        decision_fn: Callable[[Dict[str, Any]], Dict[str, Any]],
        pricing: Optional[Pricing] = None,
        enable_cache: bool = False,
    ):
        self._decision_fn = decision_fn
        self._estimator = CostEstimator(pricing)
        self._router = ModelRouter()
        self._metrics = CostMetrics()
        self._cache = DecisionCache() if enable_cache else None

    def _cache_key(self, ctx: CostContext) -> str:
        return f"{ctx.input_tokens}:{ctx.output_tokens}:{ctx.risk_score}"

    def decide(self, context: Dict[str, Any]) -> Dict[str, Any]:
        input_tokens = int(context.get("input_tokens", 0))
        output_tokens = int(context.get("output_tokens", 0))
        risk_score = float(context.get("risk_score", 0.0))

        ctx = CostContext(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            risk_score=risk_score,
        )

        if self._cache:
            cached = self._cache.get(self._cache_key(ctx))
            if cached:
                return cached

        estimate = self._estimator.estimate(
            input_tokens=ctx.input_tokens,
            output_tokens=ctx.output_tokens,
        )

        routing = self._router.route(ctx.risk_score)

        result = self._decision_fn(context)

        if isinstance(result, dict):
            meta = result.setdefault("meta", {})
            meta["cost"] = {
                "input_tokens": estimate.input_tokens,
                "output_tokens": estimate.output_tokens,
                "estimated_cost": estimate.total_cost,
            }
            meta["routing"] = {
                "model": routing.model,
                "tier": routing.tier,
            }

        if self._cache:
            self._cache.set(self._cache_key(ctx), result)

        return result
