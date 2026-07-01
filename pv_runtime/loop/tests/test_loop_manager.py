from pv_runtime.loop.manager import LoopManager

from pv_runtime.models.runtime_context import RuntimeContext

manager = LoopManager()

runtime = RuntimeContext(
    agent_id="agent-1"
)

loop = manager.start(
    goal="Write secure code",
    runtime_context=runtime,
    max_iterations=5,
)

assert loop.iteration == 0

loop = manager.next_iteration(
    loop,
    runtime,
)

assert loop.iteration == 1

print(loop)

print("PASS")
