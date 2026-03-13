class DistributedExecutor:
    """
    Sends agent tasks to distributed workers.
    """

    def __init__(self, bus):
        self.bus = bus

    def execute(self, action):
        self.bus.publish("agent_tasks", action)
