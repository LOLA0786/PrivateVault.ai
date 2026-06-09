# PrivateVault Decision Security Control Plane

## Core Thesis

Traditional AI systems secure:

- Prompts
- Models
- Responses

PrivateVault secures:

- Decisions

---

## Decision Lifecycle

Intent
→ Policy Validation
→ Context Integrity
→ Capability Authorization
→ Trust Evaluation
→ Decision Integrity
→ Execution Authorization

---

## Core Objects

### Decision Integrity Snapshot

Captures:

- Intent
- Policy
- Trust
- Context
- Authorization
- Outcome

before execution occurs.

### Decision Contract

Cryptographic authorization artifact proving:

- what was requested
- what was authorized
- under which policy
- with which capabilities

### Decision Integrity Score

Measures trustworthiness of a decision.

100 = fully trusted

0 = blocked

---

## Context Security

### Context Integrity

Tracks:

- source
- trust
- provenance
- hashes

### Retrieval Poisoning Detection

Blocks:

- instruction injection
- hidden override attempts
- malicious retrieved content

### Policy Context Conflict

Detects:

- policy violations
- context-policy mismatches

before execution.

---

## Outcomes

AUTHORIZED

or

BLOCKED

No execution occurs without authorization.

