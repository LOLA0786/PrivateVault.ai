# Runtime Receipt Schema v1

Fields

- timestamp
- decision
- reason
- decision_id
- jti
- canonical_action
- semantic_convergence
- enterprise_state
- constraints
- invariants
- sha256
- signature
- previous_receipt_hash
- receipt_hash

Rules

- receipt_hash algorithm is immutable
- signature algorithm is immutable
- chain algorithm is immutable
- fields may only be added
- existing fields may never be renamed or removed
