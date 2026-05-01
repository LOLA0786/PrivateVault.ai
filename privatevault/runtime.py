import json
import time

import merkle


def _to_bytes(obj):
    return json.dumps(obj, sort_keys=True).encode()


def generate_proof(input_data, model="unknown", temperature=0):
    timestamp = int(time.time())

    # 🔥 simulate output for now (replace later with real model call)
    output_data = {
        "result": "processed",
        "echo": input_data
    }

    config = {
        "model": model,
        "temperature": temperature
    }

    # 🔥 multi-leaf Merkle
    leaves = [
        _to_bytes(input_data),
        _to_bytes(output_data),
        _to_bytes(config),
        _to_bytes({"timestamp": timestamp})
    ]

    root_bytes = merkle.merkle_root(leaves)
    root = root_bytes.hex()

    return {
        "proof_id": root,
        "timestamp": timestamp,
        "input_hash": merkle.hash_leaf(leaves[0]).hex(),
        "output_hash": merkle.hash_leaf(leaves[1]).hex(),
        "config_hash": merkle.hash_leaf(leaves[2]).hex()
    }


def verify_proof(proof):
    # recompute root from provided components
    leaves = [
        bytes.fromhex(proof["input_hash"]),
        bytes.fromhex(proof["output_hash"]),
        bytes.fromhex(proof["config_hash"]),
    ]

    root_bytes = merkle.merkle_root(leaves)
    recomputed = root_bytes.hex()

    return {
        "valid": recomputed == proof["proof_id"],
        "recomputed": recomputed
    }
