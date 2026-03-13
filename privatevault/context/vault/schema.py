from pydantic import BaseModel
from typing import Dict, Optional
import time


class Context(BaseModel):
    id: str
    source: str
    user_id: str

    data: Dict
    human_overrides: Dict

    policy_version: str
    risk_profile: str

    created_at: float = time.time()
    signature: Optional[str] = None
