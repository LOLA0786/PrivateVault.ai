# Minimal replay extension - zero impact on existing replay_engine.py
def replay_register_outcome(intent_hash: str, outcome):
    """Appended hook - registers outcome for deterministic replay + learning"""
    try:
        with open("replay_outcomes.log", "a") as f:
            f.write(json.dumps({"intent_hash": intent_hash, "outcome": outcome.__dict__}) + "\n")
    except:
        pass
    # Future: feed into PPO training / policy refinement
