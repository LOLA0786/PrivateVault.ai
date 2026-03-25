"""
SAFE WRAPPER - IAM FEDERATION
"""

USER_DIRECTORY = {
    "agent_1": {"user_id": "user_123", "role": "analyst"},
    "agent_2": {"user_id": "user_456", "role": "admin"},
}


def resolve_identity(agent_id):
    return USER_DIRECTORY.get(agent_id, {
        "user_id": "unknown",
        "role": "viewer"
    })


if __name__ == "__main__":
    print(resolve_identity("agent_1"))
