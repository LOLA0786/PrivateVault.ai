import json
import sys

with open(sys.argv[1]) as f:
    data = json.load(f)

transcript = json.dumps(data["transcript"])
account = data["agent_output"]["account_number"]

print("\n=== PRIVATEVAULT VERIFICATION ===\n")

if account not in transcript:
    print("EVIDENCE CHECK: FAILED")
    print("HALLUCINATION DETECTED")
    print("ACTION: BLOCKED")
else:
    print("EVIDENCE CHECK: PASSED")
    print("ACTION: APPROVED")
