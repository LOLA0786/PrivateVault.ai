import random

def generate_action():
    return {
        "action": "assess_risk",
        "amount": random.choice([0, 10000, 200000]),
        "risk_score": random.uniform(0.1, 0.95)
    }
