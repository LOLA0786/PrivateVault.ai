from security.pii.detector import detect

def redact(text):

    findings = detect(text)

    for finding in findings:

        value = finding["value"]

        if finding["type"] == "email":
            replacement = value[:2] + "***@***"

        elif finding["type"] == "phone":
            replacement = "******" + value[-4:]

        elif finding["type"] == "aadhaar":
            replacement = "********" + value[-4:]

        elif finding["type"] == "pan":
            replacement = "******" + value[-3:]

        else:
            replacement = "[REDACTED]"

        text = text.replace(value, replacement)

    return text, findings
