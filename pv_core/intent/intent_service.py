"""
SAFE INTENT NORMALIZATION LAYER
"""

import uuid
import datetime


REQUIRED_FIELDS = ["action"]


def normalize(raw_intent, agent_id):
    if not isinstance(raw_intent, dict):
        raise ValueError("Intent must be dict")

    intent = dict(raw_intent)

    # enforce required fields
    for field in REQUIRED_FIELDS:
        if field not in intent:
            raise ValueError(f"Missing required field: {field}")

    # enrich intent
    intent["_meta"] = {
        "intent_id": str(uuid.uuid4()),
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "agent_id": agent_id,
        "version": "v1"
    }

    return intent


if __name__ == "__main__":
    print(normalize({"action": "test"}, "agent_1"))
