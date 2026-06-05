"""
Waste Engine — composite waste score from all waste dimensions.
Aggregates context, tool, retrieval, and retry waste into one 0–100 score.
"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class WasteBreakdown:
    total_score: float
    retry_waste: float
    context_waste: float
    tool_waste: float
    retrieval_waste: float
    dominant_cause: str
    recommendations: list = field(default_factory=list)


class WasteEngine:

    # Cost per 1K tokens by model tier (USD)
    TOKEN_COST = {
        "mini":     0.00015,
        "standard": 0.0015,
        "pro":      0.015,
        "default":  0.0015,
    }

    def evaluate(
        self,
        retries:         int   = 0,
        input_tokens:    int   = 0,
        output_tokens:   int   = 0,
        used_tokens:     int   = 0,
        total_tool_calls: int  = 0,
        useful_tool_calls: int = 0,
        retrieved_docs:  int   = 0,
        cited_docs:      int   = 0,
        model_tier:      str   = "default",
        token_budget:    int   = 8000,
    ) -> WasteBreakdown:

        scores = {}

        # Retry waste — each retry is a full re-spend
        scores["retry"] = min(retries * 15, 40)

        # Context waste — tokens sent but not semantically used
        context_ratio = 0.0
        if input_tokens > 0:
            unused = max(input_tokens - (used_tokens or input_tokens // 2), 0)
            context_ratio = unused / input_tokens
        # Also penalise for exceeding budget
        budget_overrun = max(input_tokens - token_budget, 0) / max(token_budget, 1)
        scores["context"] = min((context_ratio * 30) + (budget_overrun * 20), 35)

        # Tool waste — calls that produced no useful output
        if total_tool_calls > 0:
            wasted_ratio = max(total_tool_calls - useful_tool_calls, 0) / total_tool_calls
            scores["tool"] = min(wasted_ratio * 20, 20)
        else:
            scores["tool"] = 0.0

        # Retrieval waste — docs fetched but never cited
        if retrieved_docs > 0:
            uncited_ratio = max(retrieved_docs - cited_docs, 0) / retrieved_docs
            scores["retrieval"] = min(uncited_ratio * 15, 15)
        else:
            scores["retrieval"] = 0.0

        total = round(
            min(
                scores["retry"] + scores["context"] +
                scores["tool"]  + scores["retrieval"],
                100
            ),
            2
        )

        dominant = max(scores, key=scores.get)

        recs = []
        if scores["retry"] > 10:
            recs.append("Add pre-flight validation to reduce retries")
        if scores["context"] > 10:
            recs.append("Compress or summarise context before injection")
        if scores["tool"] > 5:
            recs.append("Gate tool calls behind intent classifier")
        if scores["retrieval"] > 5:
            recs.append("Tune retrieval top-k or relevance threshold")

        return WasteBreakdown(
            total_score=total,
            retry_waste=round(scores["retry"], 2),
            context_waste=round(scores["context"], 2),
            tool_waste=round(scores["tool"], 2),
            retrieval_waste=round(scores["retrieval"], 2),
            dominant_cause=dominant,
            recommendations=recs,
        )
