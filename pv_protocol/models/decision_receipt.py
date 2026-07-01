from dataclasses import dataclass, field, asdict
from typing import Dict, Any


@dataclass
class Capability:
    jwt: str
    expires_at: str
    constraints: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LoopSnapshot:
    loop_id: str
    iteration: int
    economics: Dict[str, Any] = field(default_factory=dict)
    health: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Evidence:
    request_hash: str
    decision_hash: str
    prior_receipt_hash: str
    merkle_root: str
    receipt_hash: str


@dataclass
class DecisionReceipt:
    protocol_version: str

    request_id: str
    decision_id: str

    status: str
    reason_code: str

    capability: Capability
    loop_snapshot: LoopSnapshot
    evidence: Evidence

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(
            protocol_version=data["protocol_version"],
            request_id=data["request_id"],
            decision_id=data["decision_id"],
            status=data["status"],
            reason_code=data["reason_code"],
            capability=Capability(**data["capability"]),
            loop_snapshot=LoopSnapshot(**data["loop_snapshot"]),
            evidence=Evidence(**data["evidence"])
        )
