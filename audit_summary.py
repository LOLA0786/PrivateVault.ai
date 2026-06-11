import json
from collections import Counter

with open("proof.json") as f:
    data = json.load(f)

analyses = data.get("analyses", [])

drift = 0
critical = 0
deny = 0
rules = Counter()

for a in analyses:
    if a.get("intentDrift"):
        drift += 1

    if a.get("riskLevel") == "CRITICAL":
        critical += 1

    if a.get("policyDecision") == "DENY":
        deny += 1

    for r in a.get("violatedRules", []):
        rules[r.get("name", "unknown")] += 1

print("PrivateVault Governance Audit")
print()
print(f"Total Actions : {len(analyses)}")
print(f"Intent Drift  : {drift}")
print(f"Critical Risk : {critical}")
print(f"Denied Actions: {deny}")
print()

print("Top Violations:")
for name, count in rules.most_common(5):
    print(f" - {name}: {count}")
