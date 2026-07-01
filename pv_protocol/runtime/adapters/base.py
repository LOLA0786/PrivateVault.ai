from abc import ABC, abstractmethod


class RuntimeAdapter(ABC):

    @abstractmethod
    def evaluate_policy(self, request):
        pass

    @abstractmethod
    def evaluate_intent(self, request):
        pass

    @abstractmethod
    def issue_capability(self, request):
        pass

    @abstractmethod
    def collect_economics(self, request):
        pass

    @abstractmethod
    def compute_health(self, request):
        pass

    @abstractmethod
    def record_evidence(self, request, decision):
        pass
