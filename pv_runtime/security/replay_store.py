"""
Replay Store.

Abstracts replay protection away from JWT verification.
"""

from abc import ABC, abstractmethod


class ReplayStore(ABC):

    @abstractmethod
    def exists(self, key: str) -> bool:
        ...

    @abstractmethod
    def put(self, key: str, ttl: int):
        ...
