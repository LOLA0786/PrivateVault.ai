# Decision Runtime Protocol (DRP)

Status: Draft v0.1

Decision Runtime Protocol defines the interface between an AI
orchestrator and a Decision Authority such as PrivateVault.

Objectives

- Framework agnostic
- Transport agnostic
- Cryptographically verifiable
- Replayable
- Capability based
- Event sourced

Core Objects

1. ActionRequest
2. DecisionReceipt
3. Capability
4. ExecutionEvidence

Flow

Planner
↓

ActionRequest

↓

Decision Authority

↓

DecisionReceipt

↓

Executor

↓

Execution Evidence

↓

Ledger

