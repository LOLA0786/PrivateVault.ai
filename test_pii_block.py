from security.pii.runtime_filter import enforce

sample = {
    "choices": [
        {
            "message": {
                "content": """
Email a@gmail.com
Email b@gmail.com
Email c@gmail.com
Email d@gmail.com
Email e@gmail.com
Email f@gmail.com
"""
            }
        }
    ]
}

result = enforce(sample)

if result["count"] > 5:
    print("DECISION: DENY")
else:
    print("DECISION: ALLOW")
