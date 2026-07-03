# Receipt Schema v1

Version: 1.0
Status: FROZEN

## Purpose

A Runtime Receipt is the immutable cryptographically-verifiable record
of every authorization decision.

Every decision MUST emit exactly one receipt.

---

## Required Fields

| Field | Type |
|--------|------|
| schema_version | string |
| receipt_hash | string |
| previous_receipt_hash | string |
| timestamp | number |
| decision | string |
| reason | string/null |
| decision_id | string/null |
| jti | string/null |
| canonical_action | object/null |
| semantic_convergence | object/null |
| enterprise_state | object/null |
| constraints | array/null |
| invariants | array/null |
| sha256 | string |
| signature | object |

---

## Canonical Serialization

Receipts MUST be serialized using

json.dumps(
    receipt,
    sort_keys=True,
    separators=(",", ":"),
    default=str,
)

---

## Signature

Algorithm: Ed25519

signature = Sign(
    SHA256(canonical_receipt)
)

---

## Hash Chain

receipt.previous_receipt_hash

MUST equal

previous.receipt_hash

GENESIS is used for the first receipt.

---

## Compatibility

Fields may only be ADDED.

Fields may NEVER

- disappear
- change names
- change meaning
- change type

Version 1.x is backward compatible.
