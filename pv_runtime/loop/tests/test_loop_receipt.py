from pv_runtime.loop.manager import LoopManager
from pv_runtime.loop.evidence import record_iteration
from pv_runtime.loop.receipt import generate_receipt

from pv_runtime.models.runtime_context import RuntimeContext

runtime = RuntimeContext(
    agent_id="agent"
)

manager = LoopManager()

loop = manager.start(
    goal="Receipt",
    runtime_context=runtime,
)

loop = record_iteration(loop)

receipt = generate_receipt(loop)

print(receipt)

assert "receipt_hash" in receipt

print("PASS")
