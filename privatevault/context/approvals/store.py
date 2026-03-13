import json
import os
import time

DB = "data/approvals.json"

os.makedirs("data", exist_ok=True)


def _load():
    if not os.path.exists(DB):
        return []
    return json.load(open(DB))


def _save(data):
    json.dump(data, open(DB, "w"), indent=2)


def add(approval: dict):

    db = _load()
    db.append(approval)
    _save(db)


def get(context_id: str, role: str):

    db = _load()
    now = time.time()

    for a in db:

        if (
            a["context_id"] == context_id and
            a["role"] == role and
            a["expires_at"] > now
        ):
            return a

    return None
