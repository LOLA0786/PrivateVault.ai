"""
Canonical Approval model.

Represents an immutable approval attached to a runtime decision.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Approval:
    """
    Immutable approval record.
    """

    approved: bool

    approver: str = ""

    intent_hash: str = ""

    approval_hash: str = ""

    approval_id: str = ""

    expires_at: int = 0
