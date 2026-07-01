"""
Decision Runtime Protocol.

Every agent framework interacts with PrivateVault through this interface.
"""

from abc import ABC, abstractmethod

from pv_protocol.action_request import ActionRequest
from pv_protocol.action_response import ActionResponse


class DecisionRuntime(ABC):
    """
    Canonical Decision Runtime interface.
    """

    @abstractmethod
    def evaluate(
        self,
        request: ActionRequest,
    ) -> ActionResponse:
        """
        Evaluate one proposed action.

        The runtime is responsible for:

        • intent binding
        • policy evaluation
        • approval
        • capability issuance
        • authorization
        • execution
        • economics
        • cryptographic evidence
        • immutable receipt
        """
        raise NotImplementedError
