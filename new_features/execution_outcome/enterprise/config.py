# Enterprise configuration - fully additive
import os

ENTERPRISE_CONFIG = {
    "enabled": True,
    "environment": os.getenv("PV_ENV", "production"),
    "log_file": "new_features/execution_outcome/enterprise/logs/closed_loop_events.jsonl",
    "merkle_enabled": True,
    "truth_layer_enabled": True,
    "trust_consensus_enabled": True,
    "ppo_reward_enabled": True,
    "lor_k_enabled": True,
    "max_latency_ms": 50
}
