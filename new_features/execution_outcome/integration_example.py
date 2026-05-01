#!/usr/bin/env python3
# ONE LINE INTEGRATION - anywhere after action execution
from closed_loop_wrapper import fire_closed_loop

# Example: after any tool/API call
outcome_data = {
    "success": True,
    "business_result": {"tx_id": "real-123", "amount": 5000},
    "metrics": {"latency_ms": 1200}
}
proof = fire_closed_loop("your_intent_hash_here", outcome_data)
print("✅ Closed loop fired:", proof[:16])
