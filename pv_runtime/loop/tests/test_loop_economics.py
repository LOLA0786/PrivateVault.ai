from pv_runtime.loop.manager import LoopManager
from pv_runtime.loop.economics import LoopEconomicsEngine

from pv_runtime.models.runtime_context import RuntimeContext

runtime = RuntimeContext(
    agent_id="agent"
)

manager = LoopManager()

loop = manager.start(
    goal="Economics",
    runtime_context=runtime,
)

engine = LoopEconomicsEngine()

loop = engine.update(
    loop,
    outcome={
        "success": True,
        "business_value": 250,
    },
    cost_usd=2.5,
    latency_ms=800,
    input_tokens=1000,
    used_tokens=350,
    total_tool_calls=10,
    useful_tool_calls=8,
)

print(loop.economics)
print(loop.metadata)

assert loop.economics.total_cost == 2.5
assert "economics_score" in loop.metadata

print("PASS")
