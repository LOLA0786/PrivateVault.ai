"""
SAFE WRAPPER - MULTI-TENANCY
"""

TENANT_MAP = {
    "user_123": {"tenant_id": "finance", "policy_scope": "strict"},
    "user_456": {"tenant_id": "ops", "policy_scope": "relaxed"},
}


def resolve_tenant(identity):
    user_id = identity.get("user_id")

    return TENANT_MAP.get(user_id, {
        "tenant_id": "default",
        "policy_scope": "standard"
    })


if __name__ == "__main__":
    print(resolve_tenant({"user_id": "user_123"}))
