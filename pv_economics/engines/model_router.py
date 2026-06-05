"""
Model Router — recommends model tier based on task complexity and cost budget.
Uses real model cost data, not hardcoded fictional names.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class ModelRecommendation:
    provider:        str
    model:           str
    tier:            str
    cost_per_1k_in:  float   # USD
    cost_per_1k_out: float   # USD
    rationale:       str


# Real pricing as of mid-2025 (update via config in prod)
_MODELS = {
    "mini": {
        "provider": "anthropic",
        "model":    "claude-haiku-3-5",
        "cost_in":  0.00025,
        "cost_out": 0.00125,
    },
    "standard": {
        "provider": "anthropic",
        "model":    "claude-sonnet-4",
        "cost_in":  0.003,
        "cost_out": 0.015,
    },
    "pro": {
        "provider": "anthropic",
        "model":    "claude-opus-4",
        "cost_in":  0.015,
        "cost_out": 0.075,
    },
}


class ModelRouter:

    def recommend(
        self,
        complexity:      str   = "standard",  # simple / standard / complex
        max_cost_usd:    Optional[float] = None,
        input_tokens:    int   = 1000,
        output_tokens:   int   = 500,
        requires_tools:  bool  = False,
    ) -> ModelRecommendation:

        tier_map = {
            "simple":   "mini",
            "standard": "standard",
            "complex":  "pro",
        }
        tier = tier_map.get(complexity, "standard")

        # If budget is tight, downgrade
        if max_cost_usd is not None:
            for candidate in ["mini", "standard", "pro"]:
                m = _MODELS[candidate]
                est_cost = (
                    input_tokens  / 1000 * m["cost_in"] +
                    output_tokens / 1000 * m["cost_out"]
                )
                if est_cost <= max_cost_usd:
                    tier = candidate
                    break

        m = _MODELS[tier]

        rationale = (
            f"Estimated cost ${(input_tokens/1000*m['cost_in'] + output_tokens/1000*m['cost_out']):.5f} "
            f"for {input_tokens}+{output_tokens} tokens. "
            f"Tier '{tier}' selected for '{complexity}' complexity."
        )

        return ModelRecommendation(
            provider=m["provider"],
            model=m["model"],
            tier=tier,
            cost_per_1k_in=m["cost_in"],
            cost_per_1k_out=m["cost_out"],
            rationale=rationale,
        )
