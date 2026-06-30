def evaluate(query, hydra_res):
    """
    Compatibility wrapper for legacy callers.

    NOTE:
    The canonical runtime entrypoint is pv_runtime.entrypoint.execute().
    This wrapper only adapts older code.
    """

    from pv_core.connectors.connector_service import execute_action

    try:
        from show_audit import build_audit
    except Exception:
        build_audit = None

    intent = {
        "action": "risk_assess",
        "recipient": "user",
        "metadata": hydra_res,
    }

    # Canonical decision schema
    decision = {
        "allowed": True,
        "reason": "legacy_wrapper",
    }

    result = execute_action(intent, decision)

    if build_audit:
        audit = build_audit(query, hydra_res, result)
        return {
            "result": result,
            "audit_id": audit.get("audit_id"),
            "hash": audit.get("hash"),
        }

    return {
        "result": result,
    }
