import json
import os

DB_PATH = "data/context_vault.json"

os.makedirs("data", exist_ok=True)


def _load():
    if not os.path.exists(DB_PATH):
        return []
    return json.load(open(DB_PATH))


def _save(data):
    json.dump(data, open(DB_PATH, "w"), indent=2)


def save_context(ctx: dict):
    db = _load()
    db.append(ctx)
    _save(db)


def get_context(ctx_id: str):
    db = _load()
    return next((c for c in db if c["id"] == ctx_id), None)


def query(filters: dict):
    db = _load()

    def match(c):
        return all(c.get(k) == v for k, v in filters.items())

    return list(filter(match, db))
