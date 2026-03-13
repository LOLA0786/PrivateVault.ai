from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class AgentAction:
    """
    Universal Agent Action Language (UAAL)
    """

    agent_id: str
    intent: str
    tool: str
    parameters: Dict[str, Any]
    risk_level: str
    timestamp: float
