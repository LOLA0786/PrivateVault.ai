import json
import os

HISTORY_FILE = "logs/firewall/history.json"

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history[-1000:], f)

def anomaly_score(action: str):
    history = load_history()

    if action not in history:
        return 0.4

    return 0.05

def update_history(action: str):
    history = load_history()
    history.append(action)
    save_history(history)
