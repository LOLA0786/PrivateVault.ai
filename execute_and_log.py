from security.agent_firewall.firewall import firewall_check
import time
import json
import hashlib
from shadow_mode import shadow_evaluate


def execute_and_log(intent: dict):
    fw = firewall_check(action)
    if fw["decision"] == "BLOCK":
        return {"status": "blocked", "fw": fw}
    if fw["decision"] == "QUARANTINE":
        return {"status": "quarantined", "fw": fw}
    intent_hash = hashlib.sha256(
        json.dumps(intent, sort_keys=True).encode()
    ).hexdigest()

    intent["intent_hash"] = intent_hash

    # ---- REAL decision (production) ----
    decision = "ALLOW"
    policy = "NONE"

    if intent["domain"] == "fintech" and intent.get("amount", 0) >= 200000:
        decision = "BLOCK"
        policy = "FINTECH_v1.0"

    real_allowed = decision == "ALLOW"

    # ---- SHADOW decision ----
    shadow = shadow_evaluate(intent)

    record = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "domain": intent["domain"],
        "actor": intent.get("actor"),
        "action": intent.get("action"),
        "mode": intent.get("mode"),
        "amount": intent.get("amount"),
        "decision": decision,
        "policy": policy,
        "allowed": real_allowed,
        "shadow_decision": shadow,
        "shadow_diff": shadow["allowed"] != real_allowed,
        "intent_hash": intent_hash,
    }

    with open("audit.log", "a") as f:
        f.write(json.dumps(record) + "\n")

    return record

# PrivateVault ExecutionOutcome closed-loop hook (additive - Prof. Veloso)
from new_features.execution_outcome.execution_outcome import record_execution_outcome
# Call this after any tool/action succeeds/fails


# === CLOSED-LOOP INTEGRATION POINT (additive) ===
from new_features.execution_outcome.closed_loop_wrapper import fire_closed_loop
# Usage (1 line anywhere after action completes):
# fire_closed_loop(intent_hash, {"success": True, "business_result": {...}, "metrics": {...}})

# === ENTERPRISE CLOSED-LOOP INTEGRATION (additive only) ===
from new_features.execution_outcome.enterprise import fire_closed_loop
# After any tool / API / agent action completes:
# fire_closed_loop(intent_hash, {
#     "success": True,
#     "business_result": {"tx_id": "...", "amount": 5000},
#     "metrics": {"latency_ms": 1840}
# })

# === ENTERPRISE CLOSED-LOOP INTEGRATION (additive only - production ready) ===

from new_features.execution_outcome.enterprise import fire_closed_loop

# After any tool/API/action completes, add this ONE line:

# fire_closed_loop(intent_hash, {"success": True, "business_result": {...}, "metrics": {...}})

