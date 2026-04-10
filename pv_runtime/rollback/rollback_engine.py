from typing import Dict, Any

class RollbackEngine:

    def __init__(self):
        self.rollback_map = {}

    def register(self, action_type: str, rollback_fn):
        self.rollback_map[action_type] = rollback_fn

    def rollback(self, action: Dict[str, Any]):
        action_type = action.get("action")

        if action_type not in self.rollback_map:
            return {"status": "NO_ROLLBACK_DEFINED"}

        try:
            return self.rollback_map[action_type](action)
        except Exception as e:
            return {"status": "ROLLBACK_FAILED", "error": str(e)}
