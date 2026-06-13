from pv_runtime.adversarial.detectors.collusion_detector import CollusionDetector
from pv_runtime.adversarial.detectors.context_stitching_detector import ContextStitchingDetector
from pv_runtime.adversarial.detectors.confusable_detector import ConfusableDetector
from pv_runtime.adversarial.detectors.script_mixing_detector import ScriptMixingDetector

class AdversarialRiskEngine:

    def __init__(self):
        self.collusion = CollusionDetector()
        self.context = ContextStitchingDetector()
        self.confusable = ConfusableDetector()
        self.script_mixing = ScriptMixingDetector()

    def evaluate(
        self,
        history,
        agent_chain,
        text=""
    ):

        collusion_score = self.collusion.score(agent_chain)

        context_score = self.context.score(history)

        confusable_score = self.confusable.score(text)

        script_score = self.script_mixing.score(text)

        total = min(
            collusion_score +
            context_score +
            confusable_score +
            script_score,
            100
        )

        return {
            "total_score": total,
            "collusion_score": collusion_score,
            "context_score": context_score,
            "confusable_score": confusable_score,
            "script_score": script_score
        }
