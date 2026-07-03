
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

    result = EnterpriseActionVerifier().verify(
        eav_action
    )

    if not result["passed"]:
        raise Exception(
            f"EAV_VERIFICATION_FAILED: {result}"
        )

    runtime_receipt = create_runtime_receipt(
        result
    )

    assert_intent_binding(
        declared_intent,
        executed_intent,
    )

    assert_approval_binding(
        declared_intent,
        approval,
    )

    verify_jwt_cap(
        capability_token,
        action,
        principal,
    )

    return {
        "authorized": True,
        "runtime_receipt": runtime_receipt,
    }
