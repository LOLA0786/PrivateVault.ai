from pv_runtime.loop.manager import LoopManager
from pv_runtime.loop.evidence import record_iteration

from pv_runtime.models.runtime_context import RuntimeContext

runtime = RuntimeContext(
    agent_id="agent"
)

manager = LoopManager()

loop = manager.start(
    goal="Test",
    runtime_context=runtime,
)

loop = record_iteration(loop)

print(loop.evidence)

assert loop.evidence.current_hash != ""

loop = manager.next_iteration(
    loop,
    runtime,
)

loop = record_iteration(loop)

print(loop.evidence)

assert loop.evidence.previous_hash != ""

print("PASS")
