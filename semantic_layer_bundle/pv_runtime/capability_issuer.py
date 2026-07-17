"""
PrivateVault Capability Issuer.

Issues runtime execution capabilities using the canonical JWT capability
implementation.
"""

import time
import uuid

from jwt_capability import issue_jwt_cap

from pv_runtime.models.capability import Capability


def issue_capability(
    *,
    principal: str,
    action: str,
    ttl_seconds: int = 300,
):
    """
    Issue a runtime execution capability.

    The runtime model remains stable while the underlying token format
    is delegated to jwt_capability.py.
    """

    issued = int(time.time())

    decision_id = str(uuid.uuid4())

    token = issue_jwt_cap(
        decision_id=decision_id,
        action=action,
        principal=principal,
    )

    return Capability(
        token=token,
        capability_id=decision_id,
        principal=principal,
        action=action,
        issued_at=issued,
        expires_at=issued + ttl_seconds,
        single_use=True,
    )
