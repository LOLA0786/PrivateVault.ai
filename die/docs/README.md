# Decision Integrity Engine (DIE)

Pre-execution decision correctness layer for PrivateVault.

## Position in the stack

```
User Intent
    ↓
Intent Parser
    ↓
⚡ DIE  ← this module
    ↓
ai_firewall_core.py   (existing — untouched)
    ↓
policy_engine.py      (existing — untouched)
    ↓
Execution
```

## What it does

Validates whether a decision is **structurally sound** before an agent
is allowed to execute it.

Not safety. Not compliance. **Decision correctness under context variability.**

## Pipeline

```
DecisionObject
    → AssumptionExtractor   surfaces implicit logic as explicit assumptions
    → StressTester          simulates context variations (fraud, edge values)
    → StabilityScorer       scores fragility (0.0 – 1.0)
    → ExecutionGate         emits PASS / RESTRICTED / BLOCKED
```

## Output

```json
{
  "status": "RESTRICTED",
  "reason": "decision holds only under specific conditions",
  "required_conditions": ["cart_value = 120", "user_type = new_customer"],
  "decision_score": 0.62,
  "decision_type": "conditional",
  "failure_modes": ["decision unsafe under high fraud risk"],
  "assumption_flags": []
}
```

## Integration

```python
from die import DecisionIntegrityEngine, DecisionObject

engine = DecisionIntegrityEngine()

decision = DecisionObject(
    action="offer_discount",
    goal="increase_conversion",
    context={"user_type": "new_customer", "cart_value": 120},
    constraints={"max_discount": 20, "margin_floor": 15},
)

result = engine.evaluate(decision)

if result.status == "BLOCKED":
    return {"allowed": False, "reason": result.reason}
```

## Files

```
die/
├── __init__.py                    public API
├── core/
│   ├── __init__.py
│   ├── decision_object.py         input contract
│   ├── assumption_extractor.py    component 1
│   ├── stress_tester.py           component 2
│   ├── stability_scorer.py        component 3
│   ├── execution_gate.py          component 4 + DIEResult
│   └── engine.py                  orchestrator (single entry point)
├── tests/
│   ├── __init__.py
│   └── test_die.py                unit tests
└── docs/
    └── README.md                  this file
```

## Status

Phase 1 — rule-based (current)
Phase 2 — LLM-backed assumption extraction + adversarial stress scenarios
Phase 3 — feedback loop from blocked decisions → pattern library
