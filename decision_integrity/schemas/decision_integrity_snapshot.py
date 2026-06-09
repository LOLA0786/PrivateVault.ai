from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class DecisionIntegritySnapshot:
    decision_id: str
    timestamp: str

    actor_id: str
    agent_id: str

    intent_hash: str
    intent_text: str

    policy_version: str
    policy_hash: str

    capability_tokens: List[str] = field(default_factory=list)

    trust_score: float = 0.0

    tools_requested: List[str] = field(default_factory=list)
    tools_authorized: List[str] = field(default_factory=list)

    approval_chain: List[str] = field(default_factory=list)

    execution_contract_hash: str = ""

    outcome: str = "PENDING"

    evidence_hash: str = ""

    decision_integrity_score: float = 100.0

    metadata: Dict[str, Any] = field(default_factory=dict)

    context_hashes: List[str] = field(default_factory=list)
    context_sources: List[str] = field(default_factory=list)
    context_trust_scores: List[float] = field(default_factory=list)

    policy_context_conflict: bool = False
    retrieval_poisoning_detected: bool = False
    memory_poisoning_detected: bool = False
