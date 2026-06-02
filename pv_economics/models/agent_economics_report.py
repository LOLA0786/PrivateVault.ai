from dataclasses import dataclass


@dataclass
class AgentEconomicsReport:

    agent: str

    cost_usd: float

    success_score: float

    trust_score: float

    roi_score: float

    context_waste: float

    retrieval_waste: float

    tool_waste: float

    savings_opportunity: float
