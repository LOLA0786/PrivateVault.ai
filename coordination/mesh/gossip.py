import random

class GossipProtocol:

    def __init__(self, mesh):
        self.mesh = mesh

    def broadcast(self, message):
        peers = list(self.mesh.agents.keys())
        selected = random.sample(peers, min(3, len(peers)))

        for peer in selected:
            self.deliver(peer, message)

    def deliver(self, peer, message):
        # simulate peer receiving message
        pass
