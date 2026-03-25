from coordination.trust.trust_engine import TrustEngine

trust_engine = TrustEngine()


def get_trust_snapshot():
    return {
        "trust_state_hash": trust_engine.snapshot_hash(),
        "timestamp": trust_engine._load_state()
    }
