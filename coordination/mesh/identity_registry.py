class IdentityRegistry:

    def __init__(self):
        self.identities = {}

    def register(self, agent_id, public_key, org):
        self.identities[agent_id] = {
            "public_key": public_key,
            "org": org
        }

    def get(self, agent_id):
        return self.identities.get(agent_id)
