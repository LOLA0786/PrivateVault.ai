def quick_score(intent):
    amount = intent.get("amount", 0)

    if amount > 50000:
        return {"risk_score": 0.9, "risk_level": "high"}
    elif amount > 10000:
        return {"risk_score": 0.6, "risk_level": "medium"}
    else:
        return {"risk_score": 0.1, "risk_level": "low"}
