class CostAttributionEngine:

    def calculate(self, execution):

        return {
            "agent": execution.agent,
            "workflow": execution.workflow,
            "task": execution.task,
            "cost": execution.cost_usd
        }
