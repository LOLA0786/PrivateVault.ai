"""
SAFE CONTEXT AGGREGATION LAYER
"""

def build_context(intent):
    # minimal safe context (no assumption)
    context = {
        "history": [],
        "policies": {},
        "signals": {},
        "meta": intent.get("_meta", {})
    }

    return context


if __name__ == "__main__":
    print(build_context({"_meta": {"test": True}}))
