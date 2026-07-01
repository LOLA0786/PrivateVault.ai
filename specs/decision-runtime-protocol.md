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

