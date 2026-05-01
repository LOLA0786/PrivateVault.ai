"""
PrivateVault Sandbox — local mock enforcement server
Run: python sandbox/sandbox_server.py
Port: 8765
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import hashlib, json, time, uvicorn

app = FastAPI(title="PrivateVault Sandbox", version="0.1.0")

# Default sandbox policy — edit freely
SANDBOX_POLICIES = {
    "block_patterns": ["delete_all", "drop_table", "sudo", "rm -rf"],
    "review_patterns": ["transfer", "send_email", "publish"],
}

LEDGER = []

@app.post("/v1/enforce")
async def enforce(request: Request):
    body = await request.json()
    tool = body.get("tool", "")
    args = body.get("args", {})
    agent_id = body.get("agent_id", "unknown")

    # Decision logic
    decision = "ALLOW"
    reason = "Policy passed"
    args_str = json.dumps(args).lower()

    for pattern in SANDBOX_POLICIES["block_patterns"]:
        if pattern in tool.lower() or pattern in args_str:
            decision = "BLOCK"
            reason = f"Matched block pattern: {pattern}"
            break

    if decision == "ALLOW":
        for pattern in SANDBOX_POLICIES["review_patterns"]:
            if pattern in tool.lower() or pattern in args_str:
                decision = "REVIEW"
                reason = f"Requires human review: {pattern}"
                break

    # Fake Merkle-style proof
    record = {"ts": time.time(), "agent": agent_id, "tool": tool, "decision": decision}
    prev_hash = LEDGER[-1]["proof_hash"] if LEDGER else "0" * 64
    proof_hash = hashlib.sha256(f"{prev_hash}{json.dumps(record)}".encode()).hexdigest()
    record["proof_hash"] = proof_hash
    LEDGER.append(record)

    return JSONResponse({"decision": decision, "reason": reason, "proof_hash": proof_hash, "sandbox": True})

@app.get("/v1/ledger")
def get_ledger():
    return {"entries": LEDGER, "count": len(LEDGER)}

@app.get("/health")
def health():
    return {"status": "ok", "mode": "sandbox", "entries": len(LEDGER)}

if __name__ == "__main__":
    print("🟡 PrivateVault SANDBOX running on http://localhost:8765")
    print("   Policies:", SANDBOX_POLICIES)
    uvicorn.run(app, host="0.0.0.0", port=8765)
