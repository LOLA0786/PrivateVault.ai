"""
Loop Budget Enforcement.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LoopBudget:
    max_cost: float = 100.0
    max_tokens: int = 100000
    max_tool_calls: int = 1000


def verify_budget(loop, budget):

    if loop.economics.total_cost > budget.max_cost:
        raise Exception("LOOP_BUDGET_EXCEEDED")

    if loop.economics.context_bytes > budget.max_tokens:
        raise Exception("TOKEN_BUDGET_EXCEEDED")

    return True
