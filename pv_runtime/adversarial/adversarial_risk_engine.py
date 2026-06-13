from pv_runtime.adversarial.detectors.collusion_detector import CollusionDetector
from pv_runtime.adversarial.detectors.context_stitching_detector import ContextStitchingDetector

class AdversarialRiskEngine:

    def __init__(self):
        self.collusion = CollusionDetector()
        self.context = ContextStitchingDetector()

    def evaluate(
        self,
        history,
        agent_chain
    ):

        collusion_score = self.collusion.score(
            agent_chain
        )

        context_score = self.context.score(
            history
        )

        total = min(
            collusion_score +
            context_score,
            100
        )

        return {
            "total_score": total,
            "collusion_score": collusion_score,
            "context_score": context_score
        }
