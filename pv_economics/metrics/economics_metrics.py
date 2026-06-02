try:
    from prometheus_client import Counter, Gauge

    agent_cost_total = Counter(
        "pv_agent_cost_total_usd",
        "Total cost by agent",
        ["agent"]
    )

    agent_success_total = Counter(
        "pv_agent_success_total",
        "Successful executions",
        ["agent"]
    )

    agent_failure_total = Counter(
        "pv_agent_failure_total",
        "Failed executions",
        ["agent"]
    )

    agent_waste_score = Gauge(
        "pv_agent_waste_score",
        "Waste score by agent",
        ["agent"]
    )

    agent_roi_score = Gauge(
        "pv_agent_roi_score",
        "ROI score by agent",
        ["agent"]
    )

except ImportError:

    class _NoopMetric:

        def labels(self, **kwargs):
            return self

        def inc(self, *args, **kwargs):
            pass

        def set(self, *args, **kwargs):
            pass

    agent_cost_total = _NoopMetric()
    agent_success_total = _NoopMetric()
    agent_failure_total = _NoopMetric()
    agent_waste_score = _NoopMetric()
    agent_roi_score = _NoopMetric()
