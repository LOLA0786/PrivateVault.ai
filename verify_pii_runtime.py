from decision_ledger import DecisionLedger

ledger = DecisionLedger(
    log_file="pii_runtime_ledger.jsonl",
    auto_load=True
)

print("EVENTS:", len(ledger.chain))
print("INTEGRITY:", ledger.verify_chain_integrity())
