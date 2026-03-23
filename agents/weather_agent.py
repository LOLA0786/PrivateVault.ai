import random

def generate_action():
    return {
        "action": random.choice(["get_weather", "forecast"]),
        "location": "Mumbai",
        "amount": 0
    }
