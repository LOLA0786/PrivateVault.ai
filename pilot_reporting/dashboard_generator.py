import json

def build_dashboard(findings):

    return {
        "pilot_name": "SBI Lending Runtime Pilot",
        "decisions_reviewed": findings["total_decisions"],
        "approved": findings["approved"],
        "blocked": findings["blocked"],
        "escalated": findings["escalated"],
        "average_risk_score": findings["average_risk_score"],

        "income_drift_cases":
            findings["violations"].get("INCOME_DRIFT", 0),

        "credit_memo_fabrication_cases":
            findings["violations"].get(
                "CREDIT_MEMO_FABRICATION", 0
            ),

        "synthetic_identity_cases":
            findings["violations"].get(
                "SYNTHETIC_IDENTITY", 0
            ),

        "policy_violation_cases":
            findings["violations"].get(
                "POLICY_VIOLATION", 0
            ),

        "group_exposure_breach_cases":
            findings["violations"].get(
                "GROUP_EXPOSURE_BREACH", 0
            )
    }

def save_dashboard(data,
                   path="pilot_output/executive_dashboard.json"):

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

