SAFE_PATTERNS = [
    "get",
    "fetch",
    "read",
    "list",
    "view",
    "query"
]

def is_safe_action(action: str):
    action = action.lower()
    return any(action.startswith(p) for p in SAFE_PATTERNS)
