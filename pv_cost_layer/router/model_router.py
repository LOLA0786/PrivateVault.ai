from dataclasses import dataclass


@dataclass(frozen=True)
class RoutingDecision:
    model: str
    tier: str


class ModelRouter:
    def route(self, risk_score: float) -> RoutingDecision:
        if risk_score < 0.2:
            return RoutingDecision(model="gpt-4o-mini", tier="cheap")
        elif risk_score < 0.5:
            return RoutingDecision(model="gpt-4o", tier="standard")
        return RoutingDecision(model="gpt-4.1", tier="expensive")
