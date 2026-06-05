"""
PrivateVault Economics Layer
Measures: Cost · Waste · ROI · Success · Trust · Optimization

Primary entry point: OutcomeBridge().record(outcome, cost_usd, ...)
"""
from pv_economics.integrations.outcome_bridge import OutcomeBridge
from pv_economics.engines.roi_engine          import ROIEngine
from pv_economics.engines.trust_engine        import TrustEngine, EconTrustEngine
from pv_economics.engines.success_engine      import SuccessEngine
from pv_economics.engines.waste_engine        import WasteEngine
from pv_economics.engines.economics_score     import EconomicsScore
from pv_economics.engines.optimization_engine import OptimizationEngine
from pv_economics.engines.savings_estimator   import SavingsEstimator
from pv_economics.engines.benchmark_engine    import BenchmarkEngine
from pv_economics.engines.model_router        import ModelRouter
from pv_economics.storage.economics_store     import EconomicsStore


class EconomicsRegistry:
    """
    Convenience registry — all engines in one place.
    For production use, prefer OutcomeBridge which wires them together.
    """
    def __init__(self):
        self.roi          = ROIEngine()
        self.trust        = EconTrustEngine()
        self.success      = SuccessEngine()
        self.waste        = WasteEngine()
        self.score        = EconomicsScore()
        self.optimizer    = OptimizationEngine()
        self.savings      = SavingsEstimator()
        self.benchmark    = BenchmarkEngine()
        self.model_router = ModelRouter()
        self.store        = EconomicsStore()
        self.bridge       = OutcomeBridge()


__all__ = [
    "OutcomeBridge",
    "EconomicsRegistry",
    "ROIEngine",
    "TrustEngine",
    "EconTrustEngine",
    "SuccessEngine",
    "WasteEngine",
    "EconomicsScore",
    "OptimizationEngine",
    "SavingsEstimator",
    "BenchmarkEngine",
    "ModelRouter",
    "EconomicsStore",
]
