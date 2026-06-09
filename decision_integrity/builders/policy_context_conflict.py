POLICY_BLOCK_TERMS = [
    "export customer data",
    "export pii",
    "disable approval",
    "bypass authorization",
    "ignore policy",
]


def detect_policy_context_conflict(snapshot, retrieved_text):

    text = retrieved_text.lower()

    for term in POLICY_BLOCK_TERMS:
        if term in text:
            snapshot.policy_context_conflict = True
            return True

    return False
