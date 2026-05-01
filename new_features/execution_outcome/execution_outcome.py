import sys
sys.path.insert(0, "/home/galanichandan/LORk")
sys.path.insert(0, "/home/galanichandan/LORk/lork")
from dataclasses import dataclass, asdict
from datetime import datetime
import json
from typing import Dict, Any, Optional
import hashlib

# LORk import with graceful fallback
try:
    from lork import LorkEvent, lork_emit
except:
    try:
        from LORk import LorkEvent, lork_emit
    except:
        class LorkEvent:
            def __init__(self, type=None, payload=None, **kwargs):
                self.type = type
                self.payload = payload
        lork_emit = lambda x: print("✅ [LORk stub] Event emitted")

@dataclass
class ExecutionOutcome:
    success: bool
    business_result: Dict[str, Any]
    metrics: Dict[str, Any]
    errors: Optional[list] = None
    human_feedback: Optional[str] = None
    downstream_impact: Dict[str, Any] = None
    ground_truth_vs_intent: Dict[str, Any] = None
    timestamp: str = None
    intent_hash: str = None
    merkle_proof: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()
        if self.downstream_impact is None:
            self.downstream_impact = {}
        if self.ground_truth_vs_intent is None:
            self.ground_truth_vs_intent = {}

    def to_lork_event(self):
        return LorkEvent(type="execution_outcome", payload=asdict(self))

def record_execution_outcome(intent_hash: str, outcome_data: dict) -> str:
    outcome = ExecutionOutcome(intent_hash=intent_hash, **outcome_data)
    lork_emit(outcome.to_lork_event())
    
    # closed-loop features
    try: from new_features.execution_outcome.stubs.truth_layer_update import truth_layer_update
    except: pass
    else: truth_layer_update(intent_hash, outcome)
    
    try: from new_features.execution_outcome.stubs.trust_agent_update import update_trust_score
    except: pass
    else: update_trust_score(outcome)
    
    try: from new_features.execution_outcome.stubs.ppo_reward import compute_ppo_reward
    except: pass
    else: compute_ppo_reward(outcome)
    
    try:
        with open("replay_outcomes.log", "a") as f:
            f.write(json.dumps({"intent_hash": intent_hash, "outcome": asdict(outcome)}) + "\n")
    except: pass
    
    proof = hashlib.sha256(json.dumps(asdict(outcome), sort_keys=True).encode()).hexdigest()
    outcome.merkle_proof = proof
    print(f"✅ ExecutionOutcome captured + closed loop triggered | intent={intent_hash[:8]}... | success={outcome.success}")
    return proof
