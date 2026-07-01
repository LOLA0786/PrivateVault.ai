from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional


@dataclass
class Principal:
    tenant_id: str
    actor_id: str
    actor_type: str


@dataclass
class Loop:
    loop_id: str
    iteration: int
    prior_receipt_hash: Optional[str] = None


@dataclass
class Goal:
    goal_id: str
    description: str
    goal_hash: str


@dataclass
class ProposedAction:
    action_type: str
    target: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    resource_scope: str = ""


@dataclass
class Intent:
    description: str
    intent_hash: str = ""
    model_trace_ref: str = ""


@dataclass
class GraphRef:
    graph_id: str
    version: str
    from_node: str
    to_node: str
    edge_id: str


@dataclass
class Limits:
    max_cost_usd: float
    deadline_ms: int
    max_iterations: int


@dataclass
class ActionRequest:
    protocol_version: str
    request_id: str
    timestamp: str

    principal: Principal
    loop: Loop
    goal: Goal
    proposed_action: ProposedAction
    intent: Intent
    graph_ref: GraphRef
    limits: Limits

    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(
            protocol_version=data["protocol_version"],
            request_id=data["request_id"],
            timestamp=data["timestamp"],
            principal=Principal(**data["principal"]),
            loop=Loop(**data["loop"]),
            goal=Goal(**data["goal"]),
            proposed_action=ProposedAction(**data["proposed_action"]),
            intent=Intent(**data["intent"]),
            graph_ref=GraphRef(**data["graph_ref"]),
            limits=Limits(**data["limits"]),
            metadata=data.get("metadata", {})
        )
