class ToolRegistry:
    """
    Registry of all tools agents are allowed to call.
    """

    def __init__(self):
        self.tools = {}

    def register(self, name, func):
        self.tools[name] = func

    def get(self, name):
        if name not in self.tools:
            raise Exception(f"Tool not registered: {name}")
        return self.tools[name]
