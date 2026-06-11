from security.pii.redactor import redact

def enforce(openai_response):

    try:
        content = (
            openai_response["choices"][0]
            ["message"]["content"]
        )

        cleaned, findings = redact(content)

        openai_response["choices"][0] \
            ["message"]["content"] = cleaned

        return {
            "response": openai_response,
            "findings": findings,
            "count": len(findings)
        }

    except Exception:
        return {
            "response": openai_response,
            "findings": [],
            "count": 0
        }
