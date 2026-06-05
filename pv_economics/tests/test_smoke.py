"""
Smoke test — verifies the full OutcomeBridge pipeline runs end-to-end.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from pv_economics.events.outcome_event import build_outcome_event
from pv_economics.integrations.outcome_bridge import OutcomeBridge

def test_full_pipeline():
    outcome = build_outcome_event(
        success=True,
        business_result={"business_value": 50.0},
    )

    bridge = OutcomeBridge()
    result = bridge.record(
        outcome=outcome,
        cost_usd=0.012,
        agent="loan_approval_agent",
        workflow="retail_lending",
        task="credit_check",
        model="claude-sonnet-4",
        input_tokens=8500,
        output_tokens=300,
        used_tokens=6000,
        latency_ms=340,
        retries=1,
        total_tool_calls=4,
        useful_tool_calls=3,
        retrieved_docs=5,
        cited_docs=3,
        business_value=50.0,
        historical_success_rate=0.92,
        historical_avg_cost=0.010,
        executions_per_day=5000.0,
    )

    assert result["econ_grade"] in ("A","B","C","D","F"), "grade missing"
    assert result["waste_score"] > 0,                     "waste not computed"
    assert result["roi_score"]   > 0,                     "roi not computed"
    assert result["extras"]["suggestions"] is not None,   "suggestions missing"
    assert result["extras"]["savings"]["annualised_savings_usd"] >= 0

    print("\n✓ Full pipeline smoke test passed")
    print(f"  Grade:           {result['econ_grade']}")
    print(f"  Econ score:      {result['econ_score']}")
    print(f"  Waste score:     {result['waste_score']}")
    print(f"  ROI ratio:       {result['roi_score']}")
    top = result['extras']['suggestions']
    print(f"  Top suggestion:  {top[0]['action'] if top else 'none'}")
    print(f"  Annual savings: ${result['extras']['savings']['annualised_savings_usd']:,.2f}")

if __name__ == "__main__":
    test_full_pipeline()
