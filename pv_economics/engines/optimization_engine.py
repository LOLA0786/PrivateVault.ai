"""
Optimization Engine — ranked, quantified recommendations.
Each suggestion includes estimated savings in USD and waste points.
"""
from dataclasses import dataclass, field
from typing import List


@dataclass
class OptimizationSuggestion:
    action:           str
    category:         str    # context / tool / model / retry / retrieval
    estimated_savings_usd:  float
    waste_points_saved:     float
    priority:         str    # high / medium / low


class OptimizationEngine:

    def suggest(
        self,
        cost_usd:          float = 0.0,
        retries:           int   = 0,
        input_tokens:      int   = 0,
        used_tokens:       int   = 0,
        total_tool_calls:  int   = 0,
        useful_tool_calls: int   = 0,
        retrieved_docs:    int   = 0,
        cited_docs:        int   = 0,
        model_tier:        str   = "standard",
        avg_latency_ms:    float = 0.0,
    ) -> List[OptimizationSuggestion]:

        suggestions = []

        # Retry reduction
        if retries > 1:
            retry_cost_share = (retries / (retries + 1)) * cost_usd
            suggestions.append(OptimizationSuggestion(
                action="Add pre-execution validation to eliminate retries",
                category="retry",
                estimated_savings_usd=round(retry_cost_share * 0.7, 4),
                waste_points_saved=retries * 12.0,
                priority="high" if retries > 3 else "medium",
            ))

        # Context compression
        if input_tokens > 6000:
            compressible = max(input_tokens - 4000, 0)
            token_cost   = compressible / 1000 * 0.0015
            suggestions.append(OptimizationSuggestion(
                action=f"Compress context: ~{compressible:,} tokens reducible via summarisation",
                category="context",
                estimated_savings_usd=round(token_cost, 4),
                waste_points_saved=round(compressible / input_tokens * 25, 2),
                priority="high" if input_tokens > 15000 else "medium",
            ))

        # Model downgrade
        if model_tier == "pro" and cost_usd > 0.05:
            suggestions.append(OptimizationSuggestion(
                action="Evaluate if standard-tier model meets quality threshold",
                category="model",
                estimated_savings_usd=round(cost_usd * 0.85, 4),
                waste_points_saved=0.0,
                priority="medium",
            ))

        # Tool call reduction
        if total_tool_calls > 0:
            wasted = max(total_tool_calls - useful_tool_calls, 0)
            if wasted > 0:
                tool_cost_share = (wasted / total_tool_calls) * cost_usd * 0.3
                suggestions.append(OptimizationSuggestion(
                    action=f"Gate {wasted} redundant tool calls behind intent check",
                    category="tool",
                    estimated_savings_usd=round(tool_cost_share, 4),
                    waste_points_saved=round(wasted / total_tool_calls * 18, 2),
                    priority="medium",
                ))

        # Retrieval tuning
        if retrieved_docs > 0:
            uncited = max(retrieved_docs - cited_docs, 0)
            if uncited > retrieved_docs * 0.4:
                suggestions.append(OptimizationSuggestion(
                    action=f"Tune retrieval top-k: {uncited}/{retrieved_docs} docs unused",
                    category="retrieval",
                    estimated_savings_usd=round(cost_usd * 0.1, 4),
                    waste_points_saved=round(uncited / retrieved_docs * 12, 2),
                    priority="low",
                ))

        # Sort by savings descending
        suggestions.sort(
            key=lambda s: s.estimated_savings_usd, reverse=True
        )

        return suggestions
