from pv_economics.engines.roi_engine import ROIEngine
from pv_economics.engines.trust_engine import TrustEngine
from pv_economics.engines.success_engine import SuccessEngine
from pv_economics.engines.waste_engine import WasteEngine


class EconomicsRegistry:

    def __init__(self):

        self.roi = ROIEngine()

        self.trust = TrustEngine()

        self.success = SuccessEngine()

        self.waste = WasteEngine()
