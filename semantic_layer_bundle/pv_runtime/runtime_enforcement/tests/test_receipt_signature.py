from pv_runtime.evidence.runtime_receipt import create_runtime_receipt
from pv_runtime.evidence.receipt_signer import verify_receipt

def test_receipt_signature_detects_tampering():

    receipt = create_runtime_receipt(
        {
            "passed": True,
            "canonical_action": {
                "actor":"agent",
                "verb":"pay",
                "amount":100,
            }
        }
    )

    assert verify_receipt(receipt)

    receipt["canonical_action"]["amount"] = 999999

    assert not verify_receipt(receipt)
