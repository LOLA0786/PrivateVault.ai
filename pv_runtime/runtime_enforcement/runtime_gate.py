
import sys
from pathlib import Path

UAAL_ROOT = Path.home() / "UAAL"

if str(UAAL_ROOT) not in sys.path:
    sys.path.insert(0, str(UAAL_ROOT))

from intent_binding import assert_intent_binding
from approval_binding import assert_approval_binding
from jwt_capability import verify_jwt_cap

from eav.engine import EnterpriseActionVerifier
from pv_runtime.evidence.runtime_receipt import (
    create_runtime_receipt,
)


def authorize_execution(
    declared_intent,
    executed_intent,
    evidence,
    approval,
    capability_token,
    action,
    principal,
):

    eav_action = {
        "actor": principal,
        "verb": action,
        "object": {
            "id": (
                executed_intent.get("target")
                or executed_intent.get("recipient")
                or executed_intent.get("vendor")
                or executed_intent.get("object")
                or "UNKNOWN"
            ),
            "type": executed_intent.get(
                "target_type",
                "resource",
            ),
        },
        "parameters": executed_intent,
        "capability": action,
        "evidence": evidence,
    }

    try:
        jwt_payload = verify_jwt_cap(
            capability_token,
            action,
            principal,
        )

        result = EnterpriseActionVerifier().verify(
            eav_action
        )

        if not result["passed"]:
            runtime_receipt = create_runtime_receipt(
                result,
                decision="REJECT",
                reason="EAV_VERIFICATION_FAILED",
                decision_id=jwt_payload["decision_id"],
                jti=jwt_payload["jti"],
            )
            return {
                "authorized": False,
                "runtime_receipt": runtime_receipt,
                "error": f"EAV_VERIFICATION_FAILED: {result}",
            }

        assert_intent_binding(
            declared_intent,
            executed_intent,
        )

        assert_approval_binding(
            declared_intent,
            approval,
        )

    except Exception as e:

        runtime_receipt = create_runtime_receipt(
            locals().get("result", {"passed": False}),
            decision="REJECT",
            reason=str(e),
            decision_id=locals().get("jwt_payload", {}).get("decision_id"),
            jti=locals().get("jwt_payload", {}).get("jti"),
        )

        return {
            "authorized": False,
            "runtime_receipt": runtime_receipt,
            "error": str(e),
        }

    runtime_receipt = create_runtime_receipt(
        result,
        decision="ALLOW",
        decision_id=jwt_payload["decision_id"],
        jti=jwt_payload["jti"],
    )

    return {
        "authorized": True,
        "runtime_receipt": runtime_receipt,
    }

