import json
import hashlib
import time

LOG = "data/audit.log"


def snapshot(context: dict):

    blob = json.dumps(context, sort_keys=True)

    h = hashlib.sha256(blob.encode()).hexdigest()

    record = {
        "hash": h,
        "time": time.time(),
        "context_id": context["id"]
    }

    with open(LOG, "a") as f:
        f.write(json.dumps(record) + "\n")

    return h
