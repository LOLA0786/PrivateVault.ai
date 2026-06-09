from dataclasses import dataclass
from typing import FrozenSet
from datetime import datetime


@dataclass(frozen=True, slots=True)
class CapabilityToken:

    token_id: str

    agent_id: str

    capabilities: FrozenSet[str]

    issued_at: datetime

    expires_at: datetime

    signature: str
