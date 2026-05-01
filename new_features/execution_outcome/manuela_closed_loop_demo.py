#!/usr/bin/env python3
"""
PrivateVault Execution Closed-Loop Demo
"""
from closed_loop_wrapper import fire_closed_loop
import json, time

print("🚀 PrivateVault Execution Closed-Loop Demo")
print("="*70)

scenarios = [
    {"success": True,  "business_result": {"tx_id": "fin-987654", "amount": 5000}, "metrics": {"latency_ms": 3148}, "human_feedback": "Treasury approved"},
    {"success": False, "business_result": {"error": "limit_exceeded"}, "metrics": {"latency_ms": 523}, "human_feedback": "Policy hard block"},
    {"success": True,  "business_result": {"tx_id": "med-456789", "status": "completed"}, "metrics": {"latency_ms": 1890}, "downstream_impact": {"compliance_score": 1.0}}
]

for i, data in enumerate(scenarios, 1):
    print(f"\n📌 Scenario {i} - Agent Action Executed")
    proof = fire_closed_loop(f"intent_demo_{i}_{int(time.time())}", data)
    print(f"✅ Merkle proof: {proof[:16]}... | Loop closed")
    time.sleep(0.3)

print("\n🎯 ALL FEATURES ADDED:")
print("   • Execution captured at T+0")
print("   • TruthLayer updated")
print("   • Trust Consensus updated")
print("   • PPO reward signal")
print("   • Immutable LORk + Replay + Merkle chain")
print("\n✅ Ready for next call!")
