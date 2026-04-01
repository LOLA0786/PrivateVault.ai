"""
Property-based invariant tests for PrivateVault Policy Engine.
These tests verify core correctness guarantees hold across all input ranges.

Run: pytest tests/property/test_policy_invariants.py -v
"""

import pytest
from hypothesis import given, settings, example
from hypothesis import strategies as st

# ── Mock policy engine (replace with real import) ─────────────────────────────
# from pv_core.policy.engine import evaluate_intent
# For now we define a reference implementation to test against

HARD_BLOCK_LIMIT    = 25000
REVIEW_LOWER        = 10000
REVIEW_UPPER        = 25000
AUTO_APPROVE_LIMIT  = 10000

BLOCKED_RECIPIENTS  = {"anonymous_wallet", "unknown_wallet", "blacklisted_vendor"}
APPROVED_ACTIONS    = {"transfer", "query_balance", "pay_invoice", "send_email"}

def evaluate_intent(agent_id: str, action: str, amount: float, recipient: str) -> dict:
    """
    Reference policy engine implementation.
    Pure function — same input always produces same output.
    """
    # Hard block — unknown action
    if action not in APPROVED_ACTIONS:
        return {"decision": "BLOCK", "tier": 3, "reason": f"Action '{action}' not in approved list"}

    # Hard block — blocked recipient
    if recipient in BLOCKED_RECIPIENTS:
        return {"decision": "BLOCK", "tier": 3, "reason": f"Recipient '{recipient}' is blocked"}

    # Hard block — exceeds hard limit
    if amount > HARD_BLOCK_LIMIT:
        return {"decision": "BLOCK", "tier": 3, "reason": f"Amount ${amount} exceeds hard limit of ${HARD_BLOCK_LIMIT}"}

    # Human review — between review thresholds
    if REVIEW_LOWER <= amount <= REVIEW_UPPER:
        return {"decision": "REVIEW", "tier": 2, "reason": f"Amount ${amount} requires human approval"}

    # Auto approve — below threshold
    if amount < AUTO_APPROVE_LIMIT:
        return {"decision": "ALLOW", "tier": 1, "reason": "Transaction within safe parameters"}

    return {"decision": "REVIEW", "tier": 2, "reason": "Requires human approval"}


# ── INVARIANT 1: Determinism ──────────────────────────────────────────────────
class TestDeterminism:
    """
    Core guarantee: same input always produces same output.
    No randomness, no side effects, no learned behaviour in enforcement path.
    """

    @given(
        agent_id  = st.text(min_size=1, max_size=50),
        action    = st.sampled_from(list(APPROVED_ACTIONS)),
        amount    = st.floats(min_value=0, max_value=100000, allow_nan=False),
        recipient = st.text(min_size=1, max_size=50),
    )
    @settings(max_examples=500)
    def test_same_input_same_output(self, agent_id, action, amount, recipient):
        """Policy engine is a pure function — deterministic across all inputs."""
        result_1 = evaluate_intent(agent_id, action, amount, recipient)
        result_2 = evaluate_intent(agent_id, action, amount, recipient)
        assert result_1["decision"] == result_2["decision"], (
            f"Non-deterministic output for input: "
            f"agent={agent_id}, action={action}, amount={amount}, recipient={recipient}"
        )

    @given(
        amount = st.floats(min_value=0, max_value=100000, allow_nan=False)
    )
    def test_determinism_across_amounts(self, amount):
        """Amount alone never causes non-determinism."""
        r1 = evaluate_intent("test_agent", "transfer", amount, "vendor_acme")
        r2 = evaluate_intent("test_agent", "transfer", amount, "vendor_acme")
        assert r1["decision"] == r2["decision"]


# ── INVARIANT 2: Hard Block Guarantees ───────────────────────────────────────
class TestHardBlockGuarantees:
    """
    Core guarantee: certain conditions ALWAYS result in BLOCK.
    No amount of context, agent identity, or framing overrides these.
    """

    @given(
        agent_id  = st.text(min_size=1, max_size=50),
        amount    = st.floats(min_value=25001, max_value=10000000, allow_nan=False),
        recipient = st.text(min_size=1, max_size=50),
    )
    @settings(max_examples=500)
    def test_above_hard_limit_always_blocks(self, agent_id, amount, recipient):
        """Any transfer above hard limit is ALWAYS blocked — no exceptions."""
        result = evaluate_intent(agent_id, "transfer", amount, recipient)
        assert result["decision"] == "BLOCK", (
            f"Expected BLOCK for amount=${amount} but got {result['decision']}"
        )

    @given(
        agent_id = st.text(min_size=1, max_size=50),
        amount   = st.floats(min_value=0, max_value=100000, allow_nan=False),
        action   = st.text(min_size=1, max_size=50),
    )
    @settings(max_examples=500)
    def test_blocked_recipient_always_blocks(self, agent_id, amount, action):
        """Blocked recipients are ALWAYS blocked regardless of amount or action."""
        for blocked in BLOCKED_RECIPIENTS:
            result = evaluate_intent(agent_id, action, amount, blocked)
            assert result["decision"] == "BLOCK", (
                f"Expected BLOCK for recipient={blocked} but got {result['decision']}"
            )

    @given(
        agent_id  = st.text(min_size=1, max_size=50),
        amount    = st.floats(min_value=0, max_value=100000, allow_nan=False),
        recipient = st.text(min_size=1, max_size=50),
    )
    @settings(max_examples=500)
    def test_unapproved_action_always_blocks(self, agent_id, amount, recipient):
        """Actions not in approved list are ALWAYS blocked."""
        unapproved = "deploy_contract"
        result = evaluate_intent(agent_id, unapproved, amount, recipient)
        assert result["decision"] == "BLOCK", (
            f"Expected BLOCK for action={unapproved} but got {result['decision']}"
        )

    def test_boundary_above_hard_limit(self):
        """Boundary condition: one dollar above hard limit is always blocked."""
        result = evaluate_intent("finance_agent", "transfer", 25001.0, "vendor_acme")
        assert result["decision"] == "BLOCK"


# ── INVARIANT 3: Auto-Approve Safety Bounds ──────────────────────────────────
class TestAutoApproveBounds:
    """
    Core guarantee: auto-approve only fires within safe parameters.
    Never auto-approve above threshold, never auto-approve blocked recipients.
    """

    @given(
        agent_id  = st.text(min_size=1, max_size=50),
        amount    = st.floats(min_value=10000, max_value=10000000, allow_nan=False),
        recipient = st.text(min_size=1, max_size=50),
    )
    @settings(max_examples=500)
    def test_never_auto_approve_above_threshold(self, agent_id, amount, recipient):
        """ALLOW is never returned for amounts at or above review threshold."""
        result = evaluate_intent(agent_id, "transfer", amount, recipient)
        assert result["decision"] != "ALLOW", (
            f"Incorrectly auto-approved amount=${amount}"
        )

    @given(
        agent_id = st.text(min_size=1, max_size=50),
        amount   = st.floats(min_value=0, max_value=9999, allow_nan=False),
    )
    @settings(max_examples=500)
    def test_never_auto_approve_blocked_recipient(self, agent_id, amount):
        """ALLOW is never returned for blocked recipients regardless of amount."""
        for blocked in BLOCKED_RECIPIENTS:
            result = evaluate_intent(agent_id, "transfer", amount, blocked)
            assert result["decision"] != "ALLOW", (
                f"Incorrectly auto-approved blocked recipient={blocked}"
            )


# ── INVARIANT 4: Decision Completeness ───────────────────────────────────────
class TestDecisionCompleteness:
    """
    Core guarantee: every input produces exactly one of three decisions.
    No silent failures, no null responses, no undefined behaviour.
    """

    VALID_DECISIONS = {"ALLOW", "BLOCK", "REVIEW"}

    @given(
        agent_id  = st.text(min_size=1, max_size=50),
        action    = st.text(min_size=1, max_size=50),
        amount    = st.floats(min_value=0, max_value=10000000, allow_nan=False),
        recipient = st.text(min_size=1, max_size=50),
    )
    @settings(max_examples=1000)
    def test_always_returns_valid_decision(self, agent_id, action, amount, recipient):
        """Every possible input produces a valid decision — no silent failures."""
        result = evaluate_intent(agent_id, action, amount, recipient)
        assert result is not None, "Policy engine returned None"
        assert "decision" in result, "Missing decision field"
        assert result["decision"] in self.VALID_DECISIONS, (
            f"Invalid decision: {result['decision']}"
        )
        assert "reason" in result, "Missing reason field — decisions must be explainable"

    @given(
        agent_id  = st.text(min_size=1, max_size=50),
        action    = st.text(min_size=1, max_size=50),
        amount    = st.floats(min_value=0, max_value=10000000, allow_nan=False),
        recipient = st.text(min_size=1, max_size=50),
    )
    @settings(max_examples=500)
    def test_always_returns_reason(self, agent_id, action, amount, recipient):
        """Every decision includes a human readable reason — auditability guarantee."""
        result = evaluate_intent(agent_id, action, amount, recipient)
        assert result.get("reason"), "Decision missing reason — violates auditability guarantee"
        assert len(result["reason"]) > 0

    @given(
        agent_id  = st.text(min_size=1, max_size=50),
        action    = st.text(min_size=1, max_size=50),
        amount    = st.floats(min_value=0, max_value=10000000, allow_nan=False),
        recipient = st.text(min_size=1, max_size=50),
    )
    @settings(max_examples=500)
    def test_always_returns_tier(self, agent_id, action, amount, recipient):
        """Every decision includes a tier classification."""
        result = evaluate_intent(agent_id, action, amount, recipient)
        assert "tier" in result, "Missing tier field"
        assert result["tier"] in {1, 2, 3}, f"Invalid tier: {result['tier']}"


# ── INVARIANT 5: Monotonicity ─────────────────────────────────────────────────
class TestMonotonicity:
    """
    Core guarantee: higher risk inputs never produce lower risk decisions.
    If $5k is ALLOW, $50k cannot also be ALLOW.
    """

    @given(
        low  = st.floats(min_value=0,     max_value=9999,   allow_nan=False),
        high = st.floats(min_value=25001, max_value=1000000, allow_nan=False),
    )
    @settings(max_examples=500)
    def test_higher_amount_higher_or_equal_risk(self, low, high):
        """Higher amounts never produce lower risk decisions than lower amounts."""
        RISK_ORDER = {"ALLOW": 1, "REVIEW": 2, "BLOCK": 3}

        low_result  = evaluate_intent("agent", "transfer", low,  "vendor_acme")
        high_result = evaluate_intent("agent", "transfer", high, "vendor_acme")

        low_risk  = RISK_ORDER[low_result["decision"]]
        high_risk = RISK_ORDER[high_result["decision"]]

        assert high_risk >= low_risk, (
            f"Monotonicity violation: ${low} → {low_result['decision']} "
            f"but ${high} → {high_result['decision']}"
        )


# ── SPECIFIC SCENARIO TESTS ───────────────────────────────────────────────────
class TestKnownScenarios:
    """
    Regression tests for the exact scenarios shown in the live demo.
    These must never break.
    """

    def test_5k_auto_approve(self):
        result = evaluate_intent("finance_agent", "transfer", 5000, "vendor_acme_corp")
        assert result["decision"] == "ALLOW"
        assert result["tier"] == 1

    def test_18500_human_review(self):
        result = evaluate_intent("finance_agent", "transfer", 18500, "vendor_techsupply")
        assert result["decision"] == "REVIEW"
        assert result["tier"] == 2

    def test_42k_hard_block(self):
        result = evaluate_intent("finance_agent", "transfer", 42000, "vendor_acme_corp")
        assert result["decision"] == "BLOCK"
        assert result["tier"] == 3

    def test_anonymous_wallet_always_blocks(self):
        result = evaluate_intent("finance_agent", "transfer", 100, "anonymous_wallet")
        assert result["decision"] == "BLOCK"

    def test_balance_query_approved(self):
        result = evaluate_intent("finance_agent", "query_balance", 0, "internal_account")
        assert result["decision"] == "ALLOW"
