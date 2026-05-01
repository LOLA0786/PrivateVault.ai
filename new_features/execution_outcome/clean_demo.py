#!/usr/bin/env python3
"""
PrivateVault – Execution Closed-Loop Demo
Execution → Feedback → Future Cognition & Execution
"""

from new_features.execution_outcome.closed_loop_wrapper import fire_closed_loop
import time

print("🚀 PrivateVault Execution Closed-Loop Demo")
print("=" * 80)
print("Demonstrates: perception → cognition → action → feedback loop\n")

scenarios = [
    {
        "success": True,
        "business_result": {"tx_id": "fin-987654", "amount": 5000, "status": "completed"},
        "metrics": {"latency_ms": 3148, "cost_usd": 0.12},
        "human_feedback": "Treasury lead approved"
    },
    {
        "success": False,
        "business_result": {"error": "limit_exceeded"},
        "metrics": {"latency_ms": 523},
        "human_feedback": "Policy hard block applied"
    },
    {
        "success": True,
        "business_result": {"tx_id": "med-456789", "status": "completed"},
        "metrics": {"latency_ms": 1890},
        "downstream_impact": {"compliance_score": 1.0}
    }
]

for i, data in enumerate(scenarios, 1):
    print(f"📌 Scenario {i} – Agent Action Executed")
    intent_hash = f"demo_intent_{i}_{int(time.time())}"
    proof = fire_closed_loop(intent_hash, data)
    print(f"   ✅ Captured | Success: {data['success']} | Merkle proof: {proof[:16]}...")
    print(f"   🔄 TruthLayer updated → future cognition")
    print(f"   ⚖️  Trust Consensus updated")
    print(f"   🏆 PPO reward signal generated")
    print(f"   📦 LORk + Replay + Merkle chain sealed\n")
    time.sleep(0.4)

print("🎯 Closed-Loop Complete")
print("   • Execution captured at T+0 (deterministic)")
print("   • Feedback fed into TruthLayer, Trust Consensus, PPO reward")
print("   • All decisions immutable & replayable")
print("\n✅ Ready to show live in the call!")
