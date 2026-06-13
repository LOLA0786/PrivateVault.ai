from pv_runtime.adversarial.runtime_enforcement_extension import (
    enforce_adversarial_risk
)

payload = {
    "adversarial": {
        "total_score": 90
    }
}

try:

    enforce_adversarial_risk(
        payload
    )

    print("FAIL")

except Exception as e:

    print("PASS")
    print(str(e))

