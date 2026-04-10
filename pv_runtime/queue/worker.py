import threading
import time

class Worker:
    def __init__(self, controller, queue, metrics):
        self.controller = controller
        self.queue = queue
        self.metrics = metrics
        self.running = True

    def start(self):
        t = threading.Thread(target=self.run)
        t.daemon = True
        t.start()

    def run(self):
        while self.running:
            item = self.queue.pop()

            if item:
                agent_id, action = item

                result = self.controller.execute(agent_id, action)

                # ✅ SAFE retry handling
                if result["status"] == "FAILED":
                    retries = action.get("retries", 0)

                    if retries < 3:
                        action["retries"] = retries + 1
                        self.queue.push((agent_id, action))
                    else:
                        self.metrics.record(result)
                else:
                    self.metrics.record(result)

            else:
                time.sleep(0.001)
