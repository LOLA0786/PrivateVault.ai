# Decision Runtime Protocol (DRP)

Status: Draft v0.1

## Purpose

Decision Runtime Protocol (DRP) defines a transport-independent interface
between an AI orchestrator and a Decision Authority.

The orchestrator proposes an action before execution.

The Decision Authority evaluates the proposal and returns an authorization
decision together with execution capability and verifiable evidence.

The protocol is framework agnostic.

It is intended to work with orchestrators such as:

- ArkSim
- LangGraph
- CrewAI
- OpenAI Agents SDK
- AutoGen
- Google ADK
- Model Context Protocol (MCP)

---

# ActionRequest

Sent from the orchestrator to the Decision Authority.

## Fields

| Field | Description |
|-------|-------------|
| request_id | Unique request identifier |
| timestamp | UTC timestamp |
| principal | Agent or user initiating the request |
| loop | Loop execution context |
| goal | Stable loop-level objective |
| proposed_action | Action proposed for execution |
| intent | Natural-language intent and optional trace |
| graph_ref | Workflow graph metadata |
| limits | Cost, time and iteration constraints |

Example

{
  "protocol_version": "0.1",
  "request_id": "...",
  "timestamp": "...",
  "principal": {},
  "loop": {},
  "goal": {},
  "proposed_action": {},
  "intent": {},
  "graph_ref": {},
  "limits": {}
}

---

# DecisionReceipt

Returned by the Decision Authority.

## Fields

| Field | Description |
|-------|-------------|
| request_id | Original request |
| decision_id | Decision identifier |
| status | approved / denied / needs_approval |
| reason_code | Machine-readable decision reason |
| capability | Execution capability or null |
| loop_snapshot | Loop economics and health |
| evidence | Cryptographic evidence |

Example

{
  "protocol_version": "0.1",
  "request_id": "...",
  "decision_id": "...",
  "status": "approved",
  "reason_code": "POLICY_OK",
  "capability": {},
  "loop_snapshot": {},
  "evidence": {}
}

---

# Execution Flow

Orchestrator

↓

ActionRequest

↓

Decision Authority

↓

DecisionReceipt

↓

Executor

---

# Goals

- Framework agnostic
- Transport agnostic
- Replayable
- Capability based
- Cryptographically verifiable
- Suitable for autonomous agent runtimes


---

# Decision Authority

A Decision Authority is any runtime component responsible for evaluating
proposed actions before execution and returning an authorization decision.

The Decision Authority may enforce policy, validate intent, issue execution
capabilities, record cryptographic evidence, and maintain execution context.

The protocol intentionally does not require a specific implementation.

PrivateVault is the reference implementation accompanying this draft, but
any framework, runtime, or vendor may implement the protocol.

---

# Non-Goals

Decision Runtime Protocol intentionally does not define:

- Network transport (HTTP, gRPC, WebSocket, MQ, etc.)
- Authentication or identity providers
- Policy languages or rule engines
- Workflow orchestration
- Execution engines
- Storage formats
- Ledger implementations
- Cryptographic algorithms
- Runtime-specific economics models
- Runtime-specific health calculations

These concerns belong to individual implementations rather than the protocol
itself.

---

# Reference Implementation

This repository includes a reference implementation of the protocol within
PrivateVault.

The reference implementation demonstrates one possible Decision Authority,
including:

- Policy evaluation
- Capability issuance
- Cryptographic evidence generation
- Decision receipts
- Runtime integration

The protocol specification remains independent of any implementation and is
intended to support interoperability across agent runtimes and orchestration
frameworks.

