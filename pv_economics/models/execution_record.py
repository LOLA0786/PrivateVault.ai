from dataclasses import dataclass
from typing import Optional


@dataclass
class ExecutionRecord:
    agent: str
    workflow: str
    task: str

    model: str

    input_tokens: int
    output_tokens: int

    latency_ms: float

    retries: int

    cost_usd: float

    success: bool

    customer_id: Optional[str] = None
