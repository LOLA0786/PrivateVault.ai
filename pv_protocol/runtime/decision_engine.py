import hashlib
import uuid
from datetime import UTC, datetime

from pv_protocol.models.decision_receipt import (
    Capability,
    DecisionReceipt,
    Evidence,
    LoopSnapshot,
)

from pv_protocol.runtime.adapters.privatevault_adapter import (
    PrivateVaultAdapter,
)


class DecisionEngine:

    def __init__(self, adapter=None):
        self.adapter = adapter or PrivateVaultAdapter()

    def evaluate(self, request):

        policy = self.adapter.evaluate_policy(request)

        self.adapter.evaluate_intent(request)

        economics = self.adapter.collect_economics(request)

        health = self.adapter.compute_health(request)

        capability = self.adapter.issue_capability(request)

        request_hash = hashlib.sha256(
            str(request.to_dict()).encode()
        ).hexdigest()

        decision_hash = hashlib.sha256(
            (
                policy["status"] +
                request_hash
            ).encode()
        ).hexdigest()

        receipt_hash = hashlib.sha256(
            (
                decision_hash +
                request_hash
            ).encode()
        ).hexdigest()

        merkle_root = self.adapter.record_evidence(
            request,
            {
                "request_hash": request_hash,
                "decision_hash": decision_hash,
                "receipt_hash": receipt_hash,
            },
        )

        return DecisionReceipt(
            protocol_version=request.protocol_version,

            request_id=request.request_id,

            decision_id=str(uuid.uuid4()),

            status=policy["status"],

            reason_code=policy["reason_code"],

            capability=Capability(
                jwt=capability["jwt"],
                expires_at=datetime.now(UTC).isoformat(),
                constraints=capability["constraints"],
            ),

            loop_snapshot=LoopSnapshot(
                loop_id=request.loop.loop_id,
                iteration=request.loop.iteration,
                economics=economics,
                health=health,
            ),

            evidence=Evidence(
                request_hash=request_hash,
                decision_hash=decision_hash,
                prior_receipt_hash=request.loop.prior_receipt_hash or "",
                merkle_root=merkle_root,
                receipt_hash=receipt_hash,
            ),
        )
