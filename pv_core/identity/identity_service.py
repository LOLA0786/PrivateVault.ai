"""
SAFE WRAPPER - USING authenticate_agent (DETECTED)
"""

import inspect
from agent_identity import authenticate_agent


def resolve(agent_id):
    return authenticate_agent(agent_id)


if __name__ == "__main__":
    print("[CHECK] identity_service loaded")
    print("[CHECK] using authenticate_agent")
    print(inspect.getsource(authenticate_agent))
