import json
import hashlib
from datetime import datetime


AGENT_CONFIG = {
    "default": {
        "MIN_TRUST": 0.3,
        "MAX_TRUST": 2.0,
        "PASSIVE_DECAY": 0.98,
        "REWARD_RATE": 0.08,
        "PENALTY": 0.90,        # softened
        "MILD_PENALTY": 0.96,
        "TARGET_TRUST": 0.7
    },
    "risk_agent": {
        "TARGET_TRUST": 0.85,
        "REWARD_RATE": 0.06
    },
    "pricing_agent": {
        "TARGET_TRUST": 0.7,
        "REWARD_RATE": 0.09
    },
    "revenue_agent": {
        "TARGET_TRUST": 0.65,
        "REWARD_RATE": 0.1
    }
}


class TrustEngine:
    def __init__(self, storage_path="coordination/trust/trust_state.json"):
        self.storage_path = storage_path
        self.state = self._load_state()

    def _get_config(self, agent_id):
        base = AGENT_CONFIG["default"].copy()
        override = AGENT_CONFIG.get(agent_id, {})
        base.update(override)
        return base

    def _load_state(self):
        try:
            with open(self.storage_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_state(self):
        with open(self.storage_path, "w") as f:
            json.dump(self.state, f, indent=2)

    def get_weight(self, agent_id):
        return self.state.get(agent_id, {}).get("weight", 1.0)

    def update_trust(self, agent_id, outcome):
        config = self._get_config(agent_id)

        agent = self.state.setdefault(agent_id, {
            "weight": 1.0,
            "history": []
        })

        agent["history"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "outcome": outcome
        })

        weight = agent["weight"]
        target = config["TARGET_TRUST"]

        # 🔹 1. Passive decay (always)
        weight *= config["PASSIVE_DECAY"]

        # 🔹 2. Active adjustment
        if outcome.get("policy_violation"):
            # 🔥 DAMPED penalty based on distance from target
            distance = abs(weight - target)
            damping = min(distance * 2, 1.0)   # 0 → near target, 1 → far
            penalty = 1 - (1 - config["PENALTY"]) * damping
            weight *= penalty

        elif not outcome.get("correct"):
            weight *= config["MILD_PENALTY"]

        else:
            # pull toward equilibrium
            delta = target - weight
            weight += delta * config["REWARD_RATE"]

        # 🔹 3. Clamp
        weight = max(config["MIN_TRUST"], min(weight, config["MAX_TRUST"]))
        agent["weight"] = round(weight, 4)

        self._save_state()
        return agent["weight"]

    def snapshot_hash(self):
        payload = json.dumps(self.state, sort_keys=True)
        return hashlib.sha256(payload.encode()).hexdigest()
