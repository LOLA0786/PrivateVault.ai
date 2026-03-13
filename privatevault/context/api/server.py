from fastapi import FastAPI

from privatevault.context.vault import signing, store
from privatevault.context.audit import logger
from privatevault.context.engine.policies import PolicyEngine

from privatevault.context.approvals import store as approval_store
from privatevault.context.crypto import approver
from privatevault.context.approvals.regions import REGIONS

import time


app = FastAPI()
engine = PolicyEngine()


# -------------------------
# CONTEXT INGEST
# -------------------------

@app.post("/context")
def ingest(ctx: dict):

    sig = signing.sign_context(ctx)
    ctx["signature"] = sig

    store.save_context(ctx)

    h = logger.snapshot(ctx)

    return {
        "id": ctx["id"],
        "hash": h,
        "signature": sig
    }


# -------------------------
# APPROVAL
# -------------------------

@app.post("/approve")
def approve(req: dict):

    expires = time.time() + req.get("ttl", 3600)

    payload = f'{req["context_id"]}:{req["role"]}:{expires}'

    sig = approver.sign(req["role"], payload)

    approval = {
        "context_id": req["context_id"],
        "role": req["role"],
        "user": req["user"],
        "region": req.get("region", "GLOBAL"),

        "expires_at": expires,
        "signature": sig
    }

    approval_store.add(approval)

    return {
        "status": "approved",
        "expires_at": expires,
        "signature": sig
    }


# -------------------------
# AUTHORIZE
# -------------------------

@app.post("/authorize")
def authorize(req: dict):

    ctx = store.get_context(req["context_id"])

    if not ctx:
        return {"allowed": False, "reason": "no_context"}

    if not signing.verify_context(ctx, ctx["signature"]):
        return {"allowed": False, "reason": "invalid_signature"}

    # ---- Region Rules ----

    region = req.get("region", "GLOBAL")

    required = REGIONS.get(region, ["CRO", "LEGAL"])

    for r in required:
        if not approval_store.get(req["context_id"], r):
            return {
                "allowed": False,
                "reason": "missing_region_approval",
                "role": r
            }

    # ---- Dual Approval ----

    cro = approval_store.get(req["context_id"], "CRO")
    legal = approval_store.get(req["context_id"], "LEGAL")

    if not cro or not legal:
        return {"allowed": False, "reason": "missing_or_expired"}

    # ---- Verify Signatures ----

    cro_payload = f'{cro["context_id"]}:{cro["role"]}:{cro["expires_at"]}'
    legal_payload = f'{legal["context_id"]}:{legal["role"]}:{legal["expires_at"]}'

    if not approver.verify("CRO", cro_payload, cro["signature"]):
        return {"allowed": False, "reason": "invalid_cro_sig"}

    if not approver.verify("LEGAL", legal_payload, legal["signature"]):
        return {"allowed": False, "reason": "invalid_legal_sig"}

    # ---- Policy ----

    ok = engine.evaluate(req["action"], ctx)

    return {"allowed": ok}
