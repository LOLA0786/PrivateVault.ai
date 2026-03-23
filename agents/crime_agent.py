import random

def generate_action():
    return {
        "action": random.choice(["query_criminal_db", "flag_suspect"]),
        "suspect_id": random.randint(1000, 9999),
        "risk_level": random.choice(["low", "high"]),
        "amount": 0
    }
