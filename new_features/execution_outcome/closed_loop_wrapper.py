import sys
sys.path.insert(0, "/home/galanichandan/LORk")
sys.path.insert(0, "/home/galanichandan/LORk/lork")
from execution_outcome import record_execution_outcome

def fire_closed_loop(intent_hash: str, outcome_data: dict):
    """ONE LINE INTEGRATION - full closed loop"""
    return record_execution_outcome(intent_hash, outcome_data)
