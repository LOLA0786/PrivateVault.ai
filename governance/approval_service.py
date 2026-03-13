from datetime import datetime, timedelta
from governance.override_token import OverrideToken

def issue_override(
    decision_type,
    approvers,
    justification,
    mode="standard",
    ttl_minutes=30
):
    return OverrideToken(
        decision_type=decision_type,
        approvers=approvers,
        justification=justification,
        mode=mode,
        issued_at=datetime.now(timezone.utc),
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=ttl_minutes)
    )
