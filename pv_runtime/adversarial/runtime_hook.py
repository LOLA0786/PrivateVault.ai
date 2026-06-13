from pv_runtime.adversarial.adversarial_risk_engine import (
    AdversarialRiskEngine
)

_engine = AdversarialRiskEngine()

def evaluate_adversarial_risk(
    history=None,
    agent_chain=None
):
    history = history or []
    agent_chain = agent_chain or []

    return _engine.evaluate(
        history=history,
        agent_chain=agent_chain
    )
