"""
SAFE WRAPPER - USING authorize_intent (DETECTED)
"""

import inspect
from policy_engine import authorize_intent


def evaluate(intent, context):
    return authorize_intent(intent, context)


if __name__ == "__main__":
    print("[CHECK] policy_service loaded")
    print("[CHECK] using authorize_intent")
    print(inspect.getsource(authorize_intent))
