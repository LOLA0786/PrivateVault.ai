from pv_runtime.entrypoint import execute_action

try:
    from show_audit import build_audit
except:
    build_audit = None


def evaluate(query, hydra_res):
    intent = {
        "action": "risk_assess",
        "recipient": "user",
        "metadata": hydra_res
    }

    decision = {"status": "ALLOW"}

    result = execute_action(intent, decision)

    if build_audit:
        audit = build_audit(query, hydra_res, result)
        return {
            "result": result,
            "audit_id": audit.get("audit_id"),
            "hash": audit.get("hash")
        }

    return {
        "result": result
    }
