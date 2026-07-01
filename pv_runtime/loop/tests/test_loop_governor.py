from pv_runtime.loop.manager import LoopManager
from pv_runtime.loop.economics import LoopEconomicsEngine
from pv_runtime.loop.governor import LoopGovernor

from pv_runtime.models.runtime_context import RuntimeContext

runtime = RuntimeContext(
    agent_id="agent"
)

manager = LoopManager()

loop = manager.start(
    goal="Governor",
    runtime_context=runtime,
)

engine = LoopEconomicsEngine()

loop = engine.update(
    loop,
    outcome={
        "success": True,
        "business_value": 50,
    },
    cost_usd=1,
    latency_ms=500,
    input_tokens=1000,
    used_tokens=100,
    total_tool_calls=4,
    useful_tool_calls=4,
)

decision = LoopGovernor().evaluate(loop)

print(decision)

assert decision.action == "PAUSE"

print("PASS")
