import json
import time
import uuid

class PolicyVersioning:

    def __init__(self, file_path="pv_policies.log"):
        self.file_path = file_path

    def create_version(self, policy):
        version = {
            "id": str(uuid.uuid4()),
            "policy": policy,
            "timestamp": time.time()
        }

        with open(self.file_path, "a") as f:
            f.write(json.dumps(version) + "\n")

        return version["id"]

    def get_latest(self):
        try:
            with open(self.file_path, "r") as f:
                lines = f.readlines()
                if not lines:
                    return None
                return json.loads(lines[-1])
        except FileNotFoundError:
            return None

    def get_version(self, version_id):
        try:
            with open(self.file_path, "r") as f:
                for line in f:
                    v = json.loads(line)
                    if v["id"] == version_id:
                        return v
        except FileNotFoundError:
            pass
        return None
