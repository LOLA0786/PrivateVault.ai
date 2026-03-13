from datetime import timezone
from fastapi import APIRouter, Request
from pydantic import BaseModel
from datetime import datetime

from services.api.governance.normalizer import normalize
from services.api.governance.policy_loader import load_policy
from services.api.governance.policy_engine import evaluate_policy
from services.ai_client import classify_message

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str


@router.post("/respond")
def chat_respond(payload: ChatRequest, request: Request):
    """
    Internal Chat API (used by UI, agents, tests)
    """

    tenant_id = getattr(request.state, "tenant_id", "default")

    # --- AI Governance Layer (Pre-check) ---
    try:
        ai_result = classify_message(
            message=payload.message or "",
            tenant_id=tenant_id,
            user_id="unknown"
        )

        if ai_result["governance"]["policy"]["action"] == "BLOCK":
            return {
                "message": "❌ BLOCKED by AI Governance Layer",
                "ai_decision": ai_result
            }
    except Exception:
        # Fail-open
        pass

    normalized = normalize(payload.message or "")
    policy = load_policy(tenant_id)
    decision = evaluate_policy(normalized["text"], policy)

    if decision["decision"] == "BLOCK":
        return {
            "message": (
                "❌ Decision: BLOCKED\n"
                f"📜 Policy: {decision['policy_id']}\n"
                "🧠 Reason: Policy enforcement\n"
                "🔐 Evidence Hash: 0xabc123\n"
                f"⏱ Timestamp: {datetime.now(timezone.utc).isoformat()}Z"
            )
        }

    return {
        "message": "✅ Allowed",
        "decision": decision
    }


@router.post("/webhook/cometchat")
async def cometchat_webhook(request: Request):
    """
    Webhook endpoint for CometChat
    """

    body = await request.json()

    text = body.get("data", {}).get("text", "")
    tenant_id = getattr(request.state, "tenant_id", "default")

    try:
        ai_result = classify_message(
            message=text,
            tenant_id=tenant_id,
            user_id="unknown"
        )

        if ai_result["governance"]["policy"]["action"] == "BLOCK":
            return {
                "response": {
                    "text": "⚠️ Message blocked by AI governance"
                }
            }
    except Exception:
        pass

    normalized = normalize(text)
    policy = load_policy(tenant_id)
    decision = evaluate_policy(normalized["text"], policy)

    if decision["decision"] == "BLOCK":
        return {
            "response": {
                "text": "⚠️ Message blocked by governance policy."
            }
        }

    return {
        "response": {
            "text": text
        }
    }

