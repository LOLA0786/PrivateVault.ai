def truth_layer_update(intent_hash: str, outcome):
    print(f"🔄 TruthLayer updated | intent={intent_hash[:8]}... | success={getattr(outcome,'success',True)}")
