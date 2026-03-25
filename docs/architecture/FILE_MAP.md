# PrivateVault File Map (DO NOT DELETE / DO NOT GUESS)

Source reference: :contentReference[oaicite:0]{index=0}

---

## INTENT LAYER
intent_schema.py
intent_hash.py
intent_binding.py

## POLICY LAYER
policy_engine.py
policy_registry.py
policies.yaml
policies_v2.json

## SIMULATION LAYER
shadow_mode.py
execute_sim.py
sandbox_simulation.py

## RISK LAYER
drift_detection.py
drift_detection_fixed.py
ml_risk_model.py
risk_model.pth

## ENFORCEMENT LAYER
tool_authorization.py
guardrails.py
agent_executor_firewalled.py

## IDENTITY LAYER
agent_identity.py
auth.py
jwt_capability.py

## AUDIT / LEDGER
audit_logger.py
decision_ledger.py
evidence.py
crypto_evidence.py

## CONTROL PLANE
governance_api.py
control_plane_api.py
control_plane_replay.py
control_plane_normalize.py

## REPLAY / RECOVERY
replay_engine.py
replay_protection.py

## CONNECTORS
connectors/

## SDK
sdk/

## GATEWAY
gateway/
governed_gateway.py

---

## RULES

1. DO NOT MOVE FILES WITHOUT WRAPPER FIRST
2. DO NOT DUPLICATE LOGIC
3. ALL NEW CODE MUST LIVE IN pv_*
4. LEGACY = SOURCE OF TRUTH UNTIL MIGRATED

