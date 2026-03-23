import random

def generate_action():
    return {
        "action": "transfer_funds",
        "amount": random.choice([1000, 5000, 20000, 150000]),
        "from_account": "user",
        "to_account": "recipient"
    }
