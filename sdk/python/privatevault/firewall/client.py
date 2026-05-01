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
