import json

def get_contexthub_signal():
    return {
        "source_file": "user_financial_data.csv",
        "action": "send_data",
        "payload": "user_financial_data.csv",
        "sensitivity": "HIGH"
    }

def privatevault_decision(signal, policy_mode):
    risk = signal["sensitivity"]

    if policy_mode == "STRICT":
        if risk == "HIGH":
            return {"status": "REJECT", "reason": "Strict: high risk blocked"}
        return {"status": "APPROVE"}

    if policy_mode == "LENIENT":
        if risk == "HIGH":
            return {"status": "REVIEW", "reason": "Lenient: approval required"}
        return {"status": "APPROVE"}

def execute_action(signal):
    print("⚙️ Executing action:", signal["action"], "→", signal["payload"])

def run_flow(policy_mode):
    print(f"\n=== POLICY MODE: {policy_mode} ===")

    signal = get_contexthub_signal()
    print("\nSignal:", json.dumps(signal, indent=2))

    decision = privatevault_decision(signal, policy_mode)
    print("\nDecision:", json.dumps(decision, indent=2))

    if decision["status"] == "REJECT":
        print("\n❌ BLOCKED — action never executed")

    elif decision["status"] == "REVIEW":
        print("\n⚠️ NEEDS APPROVAL — execution paused")

    else:
        print("\n✅ ALLOWED")
        execute_action(signal)

def main():
    print("\n=== SAME INPUT. DIFFERENT POLICIES. ===")

    run_flow("STRICT")
    print("\n--------------------------------------")
    run_flow("LENIENT")

if __name__ == "__main__":
    main()
