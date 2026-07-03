import statistics
import time
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path.home() / "UAAL"))

from eav.engine import EnterpriseActionVerifier

ACTION = {
    "actor": "finance-agent",
    "verb": "process_payment",
    "object": {
        "id": "vendor-a",
        "type": "vendor",
    },
    "parameters": {
        "amount": 500,
        "currency": "USD",
    },
    "capability": "payments.transfer",
    "evidence": {
        "user_request": {
            "canonical": "vendor-a",
            "amount": 500,
        },
        "planner_output": {
            "canonical": "vendor-a",
            "amount": 500,
        },
        "tool_parameters": {
            "canonical": "vendor-a",
            "amount": 500,
        },
        "enterprise_state": {
            "canonical": "vendor-a",
            "invoice_open": True,
            "target_verified": True,
        },
        "approval": {
            "canonical": "vendor-a",
        },
        "capability": {
            "canonical": "vendor-a",
        },
    },
}

RUNS = 10000

eav = EnterpriseActionVerifier()

times = []

for _ in range(RUNS):
    t0 = time.perf_counter_ns()
    eav.verify(ACTION)
    t1 = time.perf_counter_ns()
    times.append((t1 - t0) / 1_000_000)

times.sort()

avg = statistics.mean(times)
p50 = times[int(RUNS * 0.50)]
p95 = times[int(RUNS * 0.95)]
p99 = times[int(RUNS * 0.99)]

print()
print("=" * 40)
print("UAAL ENTERPRISE ACTION VERIFIER")
print("=" * 40)
print(f"Runs : {RUNS}")
print(f"Average : {avg:.3f} ms")
print(f"P50 : {p50:.3f} ms")
print(f"P95 : {p95:.3f} ms")
print(f"P99 : {p99:.3f} ms")
print(f"Max : {max(times):.3f} ms")
print("=" * 40)
