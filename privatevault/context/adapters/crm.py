import uuid

def pull_crm(customer):

    return {
        "customer_ltv": customer["ltv"],
        "open_tickets": customer["tickets"],
        "deal_stage": customer["stage"],
        "manager_approved": customer["approved"]
    }


def build_context(user, crm_data):

    return {
        "id": str(uuid.uuid4()),
        "source": "crm",
        "user_id": user,
        "data": crm_data,
        "human_overrides": {},
        "policy_version": "v1.0",
        "risk_profile": "medium"
    }
