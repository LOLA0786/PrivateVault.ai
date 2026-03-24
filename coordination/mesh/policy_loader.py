import yaml

class PolicyLoader:

    def __init__(self, path):
        with open(path) as f:
            self.policy = yaml.safe_load(f)

    def get(self):
        return self.policy
