from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeRequest:

    request_id: str

    agent_id: str

    capability: str

    payload_hash: str
