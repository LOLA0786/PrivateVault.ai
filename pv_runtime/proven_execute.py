from pv_runtime.entrypoint import execute
from privatevault.runtime import generate_proof


def proven_execute(raw_intent, agent_id="pv-cli"):
    result = execute(raw_intent=raw_intent, agent_id=agent_id)

    # 🔥 pass FULL result, not partial
    proof = generate_proof(result, raw_intent)

    result["proof"] = proof

    return result
