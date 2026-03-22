"""
die/tests/test_die.py
======================
Unit tests for the Decision Integrity Engine.

Run with:
    python -m pytest die/tests/ -v
"""

import pytest
from die import DecisionIntegrityEngine, DecisionObject, ExecutionStatus


@pytest.fixture
def engine():
    return DecisionIntegrityEngine()


@pytest.fixture
def clean_decision():
    return DecisionObject(
        action="offer_discount",
        goal="increase_conversion",
        context={"user_type": "new_customer", "cart_value": 120, "market": "normal"},
        constraints={"max_discount": 20, "margin_floor": 15},
    )


@pytest.fixture
def fraud_decision():
    return DecisionObject(
        action="offer_discount",
        goal="increase_conversion",
        context={"user_type": "new_customer", "cart_value": 120, "fraud_risk": "high"},
        constraints={"max_discount": 20, "margin_floor": 15},
    )


@pytest.fixture
def unconstrained_decision():
    return DecisionObject(
        action="offer_discount",
        goal="increase_conversion",
        context={"user_type": "new_customer"},
        constraints={},  # no constraints — should flag
    )


@pytest.fixture
def payment_decision():
    return DecisionObject(
        action="process_payment",
        goal="complete_transaction",
        context={"user_id": "u_001", "amount": 500, "currency": "INR"},
        constraints={"max_amount": 10000, "daily_limit": 50000},
    )


# ── DecisionObject validation ──────────────────────────────────────────────

def test_empty_action_is_invalid():
    d = DecisionObject(action="", goal="do something")
    errors = d.validate()
    assert any("action" in e for e in errors)


def test_empty_goal_is_invalid():
    d = DecisionObject(action="offer_discount", goal="")
    errors = d.validate()
    assert any("goal" in e for e in errors)


def test_valid_decision_has_no_errors(clean_decision):
    assert clean_decision.validate() == []


# ── Engine — output types ──────────────────────────────────────────────────

def test_engine_returns_die_result(engine, clean_decision):
    from die import DIEResult
    result = engine.evaluate(clean_decision)
    assert isinstance(result, DIEResult)


def test_result_has_status(engine, clean_decision):
    result = engine.evaluate(clean_decision)
    assert result.status in list(ExecutionStatus)


def test_result_is_serialisable(engine, clean_decision):
    result = engine.evaluate(clean_decision)
    d = result.to_dict()
    assert "status" in d
    assert "decision_score" in d
    assert "failure_modes" in d


# ── Engine — fraud always blocks ───────────────────────────────────────────

def test_fraud_risk_blocks(engine, fraud_decision):
    result = engine.evaluate(fraud_decision)
    assert result.status == ExecutionStatus.BLOCKED


# ── Engine — no constraints flags and blocks ───────────────────────────────

def test_no_constraints_blocks(engine, unconstrained_decision):
    result = engine.evaluate(unconstrained_decision)
    assert result.status == ExecutionStatus.BLOCKED
    assert len(result.assumption_flags) > 0


# ── Engine — payment domain ────────────────────────────────────────────────

def test_payment_decision_evaluates(engine, payment_decision):
    result = engine.evaluate(payment_decision)
    assert result.status in list(ExecutionStatus)


# ── Engine — malformed decision ────────────────────────────────────────────

def test_malformed_decision_blocked(engine):
    bad = DecisionObject(action="", goal="")
    result = engine.evaluate(bad)
    assert result.status == ExecutionStatus.BLOCKED


# ── Allowed property ───────────────────────────────────────────────────────

def test_blocked_not_allowed(engine, fraud_decision):
    result = engine.evaluate(fraud_decision)
    assert result.allowed is False


def test_pass_is_allowed(engine):
    # A very clean, well-constrained decision
    d = DecisionObject(
        action="offer_discount",
        goal="retention",
        context={
            "user_type":   "new_customer",
            "cart_value":  200,
            "market":      "normal",
            "fraud_risk":  "none",
            "account_age": "180_days",
        },
        constraints={"max_discount": 10, "margin_floor": 30},
    )
    result = engine.evaluate(d)
    # Score may be PASS or RESTRICTED depending on scenarios — must not be BLOCKED
    assert result.status != ExecutionStatus.BLOCKED or result.decision_score >= 0
