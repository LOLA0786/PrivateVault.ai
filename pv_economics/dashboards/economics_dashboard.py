import json


def build_dashboard(event):

    return {
        "agent":
            event["agent"],

        "cost":
            event["cost_usd"],

        "success":
            event["success"],

        "trust":
            event["trust_score"],

        "roi":
            event["roi_score"],

        "waste":
            event["waste_score"]
    }
