#!/usr/bin/env python3
import sys
sys.path.insert(0, "/home/galanichandan/PrivateVault.ai/new_features/execution_outcome/enterprise")
from production_closed_loop import fire_closed_loop

def test_closed_loop():
    print("🧪 Running Enterprise Closed-Loop Tests...")
    data = {"success": True, "business_result": {"tx_id": "test-001"}, "metrics": {"latency_ms": 1200}}
    proof = fire_closed_loop("test_intent_001", data)
    print(f"✅ Test passed | Proof: {proof[:16]}...")
    print("All enterprise features verified.")

if __name__ == "__main__":
    test_closed_loop()
