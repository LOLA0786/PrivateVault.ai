from pv_runtime.adversarial.adversarial_risk_engine import (
    AdversarialRiskEngine
)

from pv_runtime.adversarial.storage.graph_recorder import (
    record_intent
)

_engine = AdversarialRiskEngine()

def evaluate_adversarial_risk(
    principal=None,
    action=None,
    history=None,
    agent_chain=None,
    text=""
):

    history = history or []
    agent_chain = agent_chain or []

    result = _engine.evaluate(
        history=history,
        agent_chain=agent_chain,
        text=text
    )

    try:
        record_intent(
            principal=principal,
            action=action,
            normalized=text,
            risk=result
        )
    except Exception:
        pass

    return result
