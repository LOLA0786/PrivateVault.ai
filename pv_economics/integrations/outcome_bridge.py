"""
Outcome Bridge — connects execution outcomes to the economics layer.
The single integration point for PrivateVault firewall → economics.
"""
from typing import Any, Dict, Optional

from pv_economics.collectors.economics_collector import EconomicsCollector
from pv_economics.engines.roi_engine             import ROIEngine
from pv_economics.engines.waste_engine           import WasteEngine
from pv_economics.engines.success_engine         import SuccessEngine
from pv_economics.engines.trust_engine           import TrustEngine
from pv_economics.engines.economics_score        import EconomicsScore
from pv_economics.engines.optimization_engine    import OptimizationEngine
from pv_economics.engines.savings_estimator      import SavingsEstimator


class OutcomeBridge:

    def __init__(self):
        self.collector   = EconomicsCollector()
        self.roi         = ROIEngine()
        self.waste       = WasteEngine()
        self.success_eng = SuccessEngine()
        self.trust_eng   = TrustEngine()
        self.econ_score  = EconomicsScore()
        self.optimizer   = OptimizationEngine()
        self.savings     = SavingsEstimator()

    def record(
        self,
        outcome:                 Any,
        cost_usd:                float,
        agent:                   str   = "unknown",
        task:                    str   = "unknown",
        workflow:                str   = "",
        model:                   str   = "",
        input_tokens:            int   = 0,
        output_tokens:           int   = 0,
        used_tokens:             int   = 0,
        latency_ms:              float = 0.0,
        retries:                 int   = 0,
        total_tool_calls:        int   = 0,
        useful_tool_calls:       int   = 0,
        retrieved_docs:          int   = 0,
        cited_docs:              int   = 0,
        business_value:          float = 0.0,
        sla_overrides:           Optional[Dict] = None,
        historical_success_rate: float = 1.0,
        historical_avg_cost:     float = 0.0,
        customer_id:             str   = "",
        execution_duration_s:    float = 1.0,
        executions_per_day:      float = 1000.0,
    ) -> Dict[str, Any]:

        success_flag = bool(getattr(outcome, "success", False))
        outcome_dict = {
            "success":        success_flag,
            "partial":        getattr(outcome, "partial",        False),
            "error_code":     getattr(outcome, "error_code",     None),
            "error_severity": getattr(outcome, "error_severity", "medium"),
        }

        if business_value == 0:
            biz = getattr(outcome, "business_result", {})
            business_value = float(
                biz.get("business_value", 0) if isinstance(biz, dict) else 0
            )

        roi_result = self.roi.evaluate(
            cost=cost_usd,
            business_value=business_value,
            execution_duration_s=execution_duration_s,
        )

        waste_result = self.waste.evaluate(
            retries=retries,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            used_tokens=used_tokens,
            total_tool_calls=total_tool_calls,
            useful_tool_calls=useful_tool_calls,
            retrieved_docs=retrieved_docs,
            cited_docs=cited_docs,
        )

        success_result = self.success_eng.evaluate(
            outcome=outcome_dict,
            latency_ms=latency_ms,
            cost_usd=cost_usd,
            sla_overrides=sla_overrides,
        )

        trust_result = self.trust_eng.evaluate(
            outcome=outcome_dict,
            historical_success_rate=historical_success_rate,
            historical_avg_cost=historical_avg_cost,
            current_cost=cost_usd,
        )

        score_result = self.econ_score.calculate(
            success=success_result.score,
            trust=trust_result.score,
            waste=waste_result.total_score,
            roi_ratio=roi_result.ratio,
        )

        suggestions = self.optimizer.suggest(
            cost_usd=cost_usd,
            retries=retries,
            input_tokens=input_tokens,
            used_tokens=used_tokens,
            total_tool_calls=total_tool_calls,
            useful_tool_calls=useful_tool_calls,
            retrieved_docs=retrieved_docs,
            cited_docs=cited_docs,
        )

        savings_report = self.savings.estimate(
            current_cost=cost_usd,
            suggestions=suggestions,
            executions_per_day=executions_per_day,
        )

        event = {
            "agent":          agent,
            "workflow":       workflow,
            "task":           task,
            "model":          model,
            "input_tokens":   input_tokens,
            "output_tokens":  output_tokens,
            "latency_ms":     latency_ms,
            "retries":        retries,
            "cost_usd":       cost_usd,
            "success":        success_flag,
            "business_value": business_value,
            "roi_score":      roi_result.ratio,
            "waste_score":    waste_result.total_score,
            "econ_score":     score_result.score,
            "econ_grade":     score_result.grade,
            "customer_id":    customer_id,
            "extras": {
                "waste_breakdown": waste_result.__dict__,
                "success_detail":  success_result.__dict__,
                "trust_detail":    trust_result.__dict__,
                "score_breakdown": score_result.breakdown,
                "roi_detail":      roi_result.__dict__,
                "suggestions":     [s.__dict__ for s in suggestions],
                "savings":         savings_report.__dict__,
            },
        }

        row_id = self.collector.record(event)
        event["store_id"] = row_id

        return event
