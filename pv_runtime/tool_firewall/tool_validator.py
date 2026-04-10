from typing import Dict, Any

class ToolValidator:

    def validate(self, action: Dict[str, Any]) -> Dict[str, Any]:

        if "action" not in action:
            return {"valid": False, "reason": "Missing action"}

        if action.get("action") == "transfer":
            if "amount" not in action:
                return {"valid": False, "reason": "Missing amount"}

            if action["amount"] <= 0:
                return {"valid": False, "reason": "Invalid amount"}

        return {"valid": True}
