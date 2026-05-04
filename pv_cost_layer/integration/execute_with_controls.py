from typing import Dict, Any, Callable
import hashlib
import json

from pv_core.safety.execution_gate import allow_execution
from pv_cost_layer.router.scoring import PROFILES, score
from pv_cost_layer.router.learning import record
from pv_cost_layer.audit.decision_ledger import append as audit_append
from pv_cost_layer.policies.execution_policy import allowed_providers


def _rid(context: Dict[str, Any]) -> str:
    s = json.dumps(context, sort_keys=True)
    return hashlib.md5(s.encode()).hexdigest()


def _score_snapshot():
    return {p: score(p) for p in PROFILES}


def execute_with_controls(execute_fn: Callable[[Dict[str, Any]], Dict[str, Any]],
                          context: Dict[str, Any]) -> Dict[str, Any]:

    request_id = _rid(context)
    action = context.get("action", context)

    if not allow_execution(action):
        audit = audit_append({
            "request_id": request_id,
            "decision": "block",
            "reason": "rate_limited",
            "context": context,
        })
        return {
            "executed": False,
            "blocked": True,
            "reason": "rate_limited",
            "audit": audit,
        }

    scores = _score_snapshot()

    # 🔥 HARD POLICY FIRST
    allowed = allowed_providers()

    # 🔥 SOFT OPTIMIZATION SECOND
    provider = max(allowed, key=lambda p: scores[p])

    new_context = dict(context)
    new_context["provider"] = provider

    result = execute_fn(new_context)

    record(provider, result.get("success", False))

    audit = audit_append({
        "request_id": request_id,
        "decision": "execute",
        "selected_provider": provider,
        "allowed_providers": allowed,
        "scores": scores,
        "context": context,
        "result": result,
    })

    result["request_id"] = request_id
    result["audit"] = audit
    result["selected_provider"] = provider
    result["provider_profile"] = PROFILES.get(provider, {})
    result["decision_scores"] = scores
    result["allowed_providers"] = allowed

    return result
