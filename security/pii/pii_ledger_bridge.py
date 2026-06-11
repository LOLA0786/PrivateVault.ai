from decision_ledger import DecisionLedger

ledger = DecisionLedger(
    log_file="pii_runtime_ledger.jsonl",
    auto_load=True
)

def log_pii_decision(result):

    return ledger.log_interaction(
        "pii_runtime_enforcement",
        {
            "decision": result["decision"],
            "reason": result["reason"],
            "pii_count": result["count"]
        }
    )
