import threading
import random
import time

from pv_runtime.execution_controller.controller import ExecutionController
from pv_runtime.rollback.financial_rollback import rollback_transfer
from pv_runtime.queue.simple_queue import SimpleQueue
from pv_runtime.queue.worker import Worker
from pv_runtime.queue.metrics import Metrics

controller = ExecutionController()
controller.rollback_engine.register("transfer", rollback_transfer)

controller.idempotency.reset()
controller.wallet.reset()
controller.graph.reset()

queue = SimpleQueue()
metrics = Metrics()

workers = []
for _ in range(5):
    w = Worker(controller, queue, metrics)
    w.start()
    workers.append(w)

def simulate(agent_id):
    for _ in range(200):
        action = {
            "idempotency_key": str(random.random()),
            "action": "transfer",
            "amount": 10,
            "recipient": "vendor_x"
        }
        queue.push((agent_id, action))

threads = []
start = time.time()

for i in range(10):
    t = threading.Thread(target=simulate, args=(f"agent_{i}",))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# ✅ WAIT UNTIL QUEUE EMPTY
while queue.size() > 0:
    time.sleep(0.1)

end = time.time()

print("\n=== FINAL QUEUE RESULTS ===")
print("Metrics:", metrics.report())
print("Total Time:", end - start)
