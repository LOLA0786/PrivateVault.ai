from dataclasses import dataclass
from typing import Dict
from datetime import datetime


@dataclass
class MemoryRecord:
    memory_id: str
    memory_hash: str

    source: str
    creator: str

    trust_score: float

    snapshot_id: str

    status: str

    created_at: str


class MemoryRegistry:

    def __init__(self):
        self.memories: Dict[str, MemoryRecord] = {}

    def register(
        self,
        record: MemoryRecord
    ):
        self.memories[
            record.memory_id
        ] = record

    def get(
        self,
        memory_id
    ):
        return self.memories.get(memory_id)

    def exists(
        self,
        memory_id
    ):
        return memory_id in self.memories
