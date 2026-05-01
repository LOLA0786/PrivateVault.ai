class DecisionEngine:

    def evaluate(self, agent_id, action, context):
        score = 0

        # 💰 High value actions get priority
        if action.get("amount", 0) > 50:
            score += 2

        # 🔁 Penalize retries
        score -= action.get("retries", 0)

        # ⚠️ Penalize agents with recent failures
        if context.get("recent_failures", 0) > 5:
            score -= 2

        # ✅ Reward successful history
        if context.get("recent_success", 0) > 10:
            score += 1

        decision = "EXECUTE" if score >= 0 else "DEFER"

        return {
            "decision": decision,
            "priority": score
        }
