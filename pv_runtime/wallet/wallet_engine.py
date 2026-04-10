from typing import Dict

class WalletEngine:
    def reset(self):
        self.budgets = {}
        self.usage = {}


    def __init__(self):
        self.budgets = {}
        self.usage = {}

    def set_budget(self, agent_id: str, amount: float):
        self.budgets[agent_id] = amount
        self.usage[agent_id] = 0

    def is_within_budget(self, agent_id: str, action: Dict) -> bool:
        cost = self._estimate_cost(action)

        if agent_id not in self.budgets:
            return True

        if self.usage[agent_id] + cost > self.budgets[agent_id]:
            return False

        self.usage[agent_id] += cost
        return True

    def _estimate_cost(self, action: Dict) -> float:
        return float(action.get("amount", 1))
