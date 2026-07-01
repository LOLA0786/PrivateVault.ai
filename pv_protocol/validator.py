from pv_protocol.models.action_request import ActionRequest
from pv_protocol.models.decision_receipt import DecisionReceipt


VALID_STATUSES = {
    "approved",
    "denied",
    "needs_approval"
}


def validate_action_request(req: ActionRequest):

    assert req.protocol_version

    assert req.request_id

    assert req.timestamp

    assert req.loop.iteration >= 0

    assert req.limits.deadline_ms > 0

    assert req.limits.max_iterations > 0

    return True


def validate_decision_receipt(receipt: DecisionReceipt):

    assert receipt.protocol_version

    assert receipt.request_id

    assert receipt.decision_id

    assert receipt.status in VALID_STATUSES

    return True
