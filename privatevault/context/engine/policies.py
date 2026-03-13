import yaml


class PolicyEngine:

    def __init__(self, path="policies.yaml"):
        self.policies = yaml.safe_load(open(path))


    def evaluate(self, action: str, ctx: dict):

        for p in self.policies:

            if p["action"] != action:
                continue

            cond = p["allowed_if"]

            for k, v in cond.items():

                if isinstance(v, dict):
                    if not eval(str(ctx["data"].get(k)) + v["op"] + str(v["value"])):
                        return False
                else:
                    if ctx["data"].get(k) != v:
                        return False

            return True

        return False
