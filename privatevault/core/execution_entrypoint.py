class ExecutionEntrypoint:
    """
    Unified entrypoint for all AI agent actions.
    Ensures governance, routing, and evidence are always applied.
    """

    def __init__(self, execution_fabric):
        self.execution_fabric = execution_fabric

    def run(self, action):
        return self.execution_fabric.execute(action)
