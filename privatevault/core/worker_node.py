class WorkerNode:
    """
    Worker node that executes agent tasks from the distributed bus.
    """

    def __init__(self, bus, execution_fabric):
        self.bus = bus
        self.execution_fabric = execution_fabric

    def start(self, topic="agent_tasks"):

        def handler(action):
            result = self.execution_fabric.execute(action)
            self.bus.publish("agent_results", result)

        self.bus.subscribe(topic, handler)
