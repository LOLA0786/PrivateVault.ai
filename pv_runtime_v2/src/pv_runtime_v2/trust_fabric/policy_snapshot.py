from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class PolicySnapshot:

    version: str

    policy_hash: str

    signed_by: str

    created_at: datetime
