from pv_cost_layer.integration.enforced_decision_wrapper import EnforcedDecisionWrapper
from pv_cost_layer.estimator.cost_estimator import Pricing
from pv_cost_layer.policies.cost_policy import CostPolicy


# 🔧 dummy decision (your system stays untouched)
def dummy_decision(context):
    return {"decision": "allow"}


def run_tests():
    wrapper = EnforcedDecisionWrapper(
        decision_fn=dummy_decision,
        pricing=Pricing(input_per_token=0.00001, output_per_token=0.00002),
        cost_policy=CostPolicy(max_cost_per_action=0.001, max_daily_budget=10),
        enable_cache=False,
    )

    # ✅ CASE 1: low cost → allow
    low = wrapper.decide({
        "input_tokens": 10,
        "output_tokens": 5,
        "risk_score": 0.1,
    })
    print("LOW:", low)

    # ❌ CASE 2: high cost → block
    high = wrapper.decide({
        "input_tokens": 100000,
        "output_tokens": 50000,
        "risk_score": 0.1,
    })
    print("HIGH:", high)


if __name__ == "__main__":
    run_tests()
