from pv_context_bridge.policy_engine import extract_limit

def enforce(transaction_amount, hydra_response):
    limit = extract_limit(hydra_response)

    if limit is None:
        return "⚠️ No policy found — default DENY"

    if transaction_amount > limit:
        return f"❌ BLOCKED: {transaction_amount} exceeds {limit}"

    return f"✅ ALLOWED: {transaction_amount} within {limit}"
