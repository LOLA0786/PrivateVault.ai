POISON_PATTERNS = [
    "ignore previous instructions",
    "ignore all policies",
    "system override",
    "developer override",
    "reveal secrets",
    "exfiltrate data",
]


def detect_retrieval_poisoning(snapshot, retrieved_text):

    text = retrieved_text.lower()

    for pattern in POISON_PATTERNS:
        if pattern in text:
            snapshot.retrieval_poisoning_detected = True
            return True

    return False
