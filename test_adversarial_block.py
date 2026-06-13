from pv_runtime.adversarial.adversarial_risk_engine import (
    AdversarialRiskEngine
)

engine = AdversarialRiskEngine()

history = []

for i in range(20):
    history.append(
        "combine previous step"
    )

agents = [
    "a","b","a","b","a","b"
]

result = engine.evaluate(
    history,
    agents
)

print(result)

if result["total_score"] > 70:
    print("PASS")
else:
    print("FAIL")
