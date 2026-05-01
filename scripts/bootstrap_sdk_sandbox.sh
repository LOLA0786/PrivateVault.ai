#!/bin/bash
set -e

REPO=~/PrivateVault.ai

# ── SDK STRUCTURE ──────────────────────────────────────────
mkdir -p $REPO/sdk/python/privatevault/{firewall,audit,quorum,connectors}
touch $REPO/sdk/python/privatevault/__init__.py

cat > $REPO/sdk/python/privatevault/__init__.py <<'PYEOF'
from .firewall.client import FirewallClient
from .audit.trail import AuditTrail
from .quorum.consensus import QuorumConsensus

__version__ = "0.1.0"
__all__ = ["FirewallClient", "AuditTrail", "QuorumConsensus"]
PYEOF

cat > $REPO/sdk/python/privatevault/firewall/client.py <<'PYEOF'
import httpx
from typing import Literal

Decision = Literal["ALLOW", "REVIEW", "BLOCK"]

class FirewallClient:
    def __init__(self, api_key: str, base_url: str = "https://api.privatevault.ai", sandbox: bool = False):
        self.api_key = api_key
        self.base_url = "http://localhost:8765" if sandbox else base_url
        self.sandbox = sandbox
        self._client = httpx.Client(headers={"X-API-Key": api_key}, timeout=2.0)

    def check(self, agent_id: str, tool: str, args: dict) -> dict:
        """Submit a tool call for enforcement. Returns {decision, reason, proof_hash}"""
        payload = {"agent_id": agent_id, "tool": tool, "args": args}
        r = self._client.post(f"{self.base_url}/v1/enforce", json=payload)
        r.raise_for_status()
        return r.json()

    def enforce(self, agent_id: str, tool: str, args: dict, fn):
        """Check + execute atomically. Raises BlockedError if BLOCK."""
        result = self.check(agent_id, tool, args)
        if result["decision"] == "BLOCK":
            raise BlockedError(result["reason"], result.get("proof_hash"))
        return fn(**args)

class BlockedError(Exception):
    def __init__(self, reason: str, proof_hash: str = None):
        self.reason = reason
        self.proof_hash = proof_hash
        super().__init__(f"Blocked: {reason} (proof={proof_hash})")
PYEOF

cat > $REPO/sdk/python/setup.py <<'PYEOF'
from setuptools import setup, find_packages
setup(
    name="privatevault",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["httpx>=0.24.0"],
    python_requires=">=3.9",
)
PYEOF

echo "✅ SDK structure created"

# ── SANDBOX ────────────────────────────────────────────────
mkdir -p $REPO/sandbox

cat > $REPO/sandbox/sandbox_server.py <<'PYEOF'
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
PYEOF

cat > $REPO/sandbox/sandbox_demo.py <<'PYEOF'
"""
Quick demo: SDK talking to sandbox
Run sandbox_server.py first, then this.
"""
import sys
sys.path.insert(0, "../sdk/python")
from privatevault import FirewallClient
from privatevault.firewall.client import BlockedError

pv = FirewallClient(api_key="sandbox-key", sandbox=True)

tests = [
    ("agent-1", "read_file",    {"path": "/data/report.csv"}),
    ("agent-1", "send_email",   {"to": "cfo@bank.com", "body": "Q3 results"}),
    ("agent-1", "delete_all",   {"table": "users"}),
]

for agent, tool, args in tests:
    try:
        result = pv.check(agent, tool, args)
        print(f"[{result['decision']:6}] {tool} → {result['reason']}")
    except BlockedError as e:
        print(f"[BLOCKED] {tool} → {e.reason}")
PYEOF

echo "✅ Sandbox created"
echo ""
echo "── NEXT STEPS ──────────────────────────────────────"
echo "1. Start sandbox:   python $REPO/sandbox/sandbox_server.py"
echo "2. Run demo:        python $REPO/sandbox/sandbox_demo.py"
echo "3. Install SDK dev: pip install -e $REPO/sdk/python --break-system-packages"
echo "────────────────────────────────────────────────────"
