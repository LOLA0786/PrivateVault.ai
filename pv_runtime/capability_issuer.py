"""
PrivateVault Capability Issuer.

Responsible for issuing short-lived execution capabilities.

This module DOES NOT execute anything.
It only creates execution capabilities.
"""

import time
import uuid

from pv_runtime.models.capability import Capability


def issue_capability(
    *,
    principal: str,
    action: str,
    ttl_seconds: int = 300,
):
    """
    Issue a runtime execution capability.

    Future versions will replace the random token with a
    cryptographically signed JWT capability.
    """

    issued = int(time.time())

    return Capability(
        token=str(uuid.uuid4()),
        capability_id=str(uuid.uuid4()),
        principal=principal,
        action=action,
        issued_at=issued,
        expires_at=issued + ttl_seconds,
        single_use=True,
    )
