class ContextAnalyzer:

    def __init__(self, graph):
        self.graph = graph

    def get_context(self, agent_id):
        data = self.graph.query(agent_id)

        failures = 0
        successes = 0

        for item in data:
            if item.get("type") == "outcome":
                result = item.get("result", {})
                if result.get("executed"):
                    successes += 1
                else:
                    failures += 1

        return {
            "recent_failures": failures,
            "recent_success": successes,
            "total_actions": len(data)
        }
