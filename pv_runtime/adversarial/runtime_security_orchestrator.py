from pv_runtime.adversarial.runtime_hook import (
    evaluate_adversarial_risk
)

from pv_runtime.adversarial.storage.graph_recorder import (
    record_intent
)

from pv_runtime.adversarial.runtime_escalation import (
    escalation_decision
)

try:
    from pv_economics.engines.adversarial_waste import (
        AdversarialWaste
    )
except Exception:
    AdversarialWaste = None


class RuntimeSecurityOrchestrator:

    def process(
        self,
        principal,
        action,
        text="",
        history=None,
        agent_chain=None
    ):

        history = history or []
        agent_chain = agent_chain or [principal]

        adversarial = evaluate_adversarial_risk(
            history=history,
            agent_chain=agent_chain,
            text=text
        )

        try:
            record_intent(
                principal=principal,
                action=action,
                normalized=text,
                risk=adversarial
            )
        except Exception:
            pass

        escalation = escalation_decision(
            adversarial.get(
                "total_score",
                0
            )
        )

        economics = {}

        try:
            if AdversarialWaste:

                economics = (
                    AdversarialWaste()
                    .evaluate(
                        adversarial.get(
                            "total_score",
                            0
                        )
                    )
                )

        except Exception:
            pass

        return {
            "adversarial": adversarial,
            "escalation": escalation,
            "economics": economics
        }
