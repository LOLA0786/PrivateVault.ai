import os

def pii_runtime_enabled():
    return (
        os.getenv(
            "PV_ENABLE_PII_RUNTIME",
            "false"
        ).lower() == "true"
    )
