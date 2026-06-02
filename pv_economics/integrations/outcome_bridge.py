from pv_economics.collectors.economics_collector import EconomicsCollector


class OutcomeBridge:

    def __init__(self):
        self.collector = EconomicsCollector()

    def record(
        self,
        outcome,
        cost_usd,
        agent="unknown",
        task="unknown"
    ):

        success = bool(
            getattr(outcome, "success", False)
        )

        business_result = getattr(
            outcome,
            "business_result",
            {}
        )

        business_value = float(
            business_result.get(
                "business_value",
                0
            )
        )

        roi = 0

        if cost_usd > 0:
            roi = round(
                business_value / cost_usd,
                2
            )

        self.collector.record(
            {
                "agent": agent,
                "task": task,
                "cost_usd": cost_usd,
                "success": success,
                "business_value": business_value,
                "roi_score": roi,
                "waste_score": 0
            }
        )
