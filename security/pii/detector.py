import re

PATTERNS = {
    "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "phone": r"\b\d{10}\b",
    "aadhaar": r"\b\d{4}\s?\d{4}\s?\d{4}\b",
    "pan": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"
}

def detect(text):
    findings = []

    for name, pattern in PATTERNS.items():
        matches = re.findall(pattern, text)

        for match in matches:
            findings.append({
                "type": name,
                "value": match
            })

    return findings
