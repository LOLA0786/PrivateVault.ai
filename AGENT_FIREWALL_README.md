# Agent Firewall (PrivateVault)

## What this does
A runtime firewall for AI agents that:
- detects unsafe actions
- blocks execution before tools run
- enforces tool-level authorization

## Demo
- weather → allowed
- scraping → quarantined
- payment → blocked
- db delete → blocked

## Enterprise Mode (default)
- runs fully locally
- no raw data leaves environment
- telemetry OFF by default

## Optional Signal Sharing
- only anonymized signals
- no prompts / no user data
- fully opt-in

## Why this matters
Prevents real-world damage from agent hallucinations and unsafe execution.

## Architecture
Agent → Firewall → Authorization → Execution
