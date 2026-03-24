# PrivateVault Decentralized Trust Layer (DTL)

This module implements a decentralized coordination system for AI agents:

- Trust-weighted quorum (N-of-M)
- Drift-aware voting (unstable agents ignored)
- Cryptographic signature verification
- Merkle-ready audit hooks
- Execution bridge into PrivateVault core

## Flow

Agent → Mesh → Consensus → Control Plane → Execution → Proof

## Example

Run:
python coordination/mesh/demo_financial_flow.py
