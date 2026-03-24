class PolicyEngine:

    def evaluate(self, agent_id, request):
        amount = request.get("amount", 0)

        # Pricing agent
        if agent_id == "pricing_agent":
            if amount <= 300000:
                return "APPROVE", "within pricing discount range"
            return "REJECT", "exceeds pricing threshold"

        # Revenue agent
        if agent_id == "revenue_agent":
            if amount <= 250000:
                return "APPROVE", "within revenue risk tolerance"
            return "APPROVE", "strategic deal override"

        # Risk agent
        if agent_id == "risk_agent":
            if amount > 200000:
                return "REJECT", "high financial risk"
            return "APPROVE", "acceptable risk"

        return "REJECT", "unknown policy"
