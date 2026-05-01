import json
import merkle


def _b(obj):
    return json.dumps(obj, sort_keys=True).encode()


def verify_proof(data):
    try:
        # 🔥 reconstruct EXACT same leaves as runtime
        input_data = data.get("intent", {})
        receipt = data.get("receipt", {})
        decision = data.get("decision", {})
        trace = data.get("trace", {})
        enforcement = data.get("enforcement", {})

        leaves = [
            _b(input_data),
            _b(receipt),
            _b(decision),
            _b(trace),
            _b(enforcement)
        ]

        recomputed = merkle.merkle_root(leaves).hex()
        proof_id = data.get("proof", {}).get("proof_id")

        return {
            "valid": recomputed == proof_id,
            "recomputed": recomputed,
            "expected": proof_id
        }

    except Exception as e:
        return {
            "valid": False,
            "error": str(e)
        }
