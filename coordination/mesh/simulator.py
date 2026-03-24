class Simulator:

    def __init__(self, adapter):
        self.adapter = adapter

    def run(self, action_id, request):
        result = self.adapter.verify(action_id, request)

        return {
            "simulated": True,
            "result": result
        }
