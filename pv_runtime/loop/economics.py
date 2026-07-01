"""
Loop Economics.

Aggregates existing economics engines for an autonomous loop.
"""

from dataclasses import replace

from pv_runtime.loop.models import LoopContext, LoopEconomics

from pv_economics.engines.context_waste import ContextWaste
from pv_economics.engines.tool_waste import ToolWaste
from pv_economics.engines.waste_engine import WasteEngine
from pv_economics.engines.roi_engine import ROIEngine
from pv_economics.engines.success_engine import SuccessEngine
from pv_economics.engines.economics_score import EconomicsScore


_context = ContextWaste()
_tool = ToolWaste()
_waste = WasteEngine()
_roi = ROIEngine()
_success = SuccessEngine()
_score = EconomicsScore()


class LoopEconomicsEngine:

    def update(
        self,
        loop: LoopContext,
        *,
        outcome: dict,
        cost_usd: float,
        latency_ms: float,
        input_tokens: int,
        used_tokens: int,
        total_tool_calls: int,
        useful_tool_calls: int,
    ):

        context = _context.analyze(
            input_tokens,
            used_tokens,
        )

        tool = _tool.analyze(
            total_tool_calls,
            useful_tool_calls,
        )

        waste = _waste.evaluate(
            retries=loop.economics.retries,
            input_tokens=input_tokens,
            output_tokens=0,
            used_tokens=used_tokens,
            total_tool_calls=total_tool_calls,
            useful_tool_calls=useful_tool_calls,
        )

        success = _success.evaluate(
            outcome,
            latency_ms=latency_ms,
            cost_usd=cost_usd,
        )

        roi = _roi.evaluate(
            cost=cost_usd,
            business_value=outcome.get(
                "business_value",
                0,
            ),
        )

        economics_score = _score.calculate(
            success=success.score,
            trust=100,
            waste=waste.total_score,
            roi_ratio=roi.ratio,
        )

        economics = LoopEconomics(
            total_cost=loop.economics.total_cost + cost_usd,

            token_cost=loop.economics.token_cost,

            tool_cost=loop.economics.tool_cost,

            context_bytes=input_tokens,

            referenced_bytes=used_tokens,

            wasted_bytes=context["wasted_tokens"],

            retries=loop.economics.retries,

            rollbacks=loop.economics.rollbacks,
        )

        return replace(
            loop,
            economics=economics,
            metadata={
                **dict(loop.metadata),
                "economics_score": economics_score.score,
                "economics_grade": economics_score.grade,
                "waste_score": waste.total_score,
                "roi": roi.ratio,
                "success": success.score,
            },
        )
