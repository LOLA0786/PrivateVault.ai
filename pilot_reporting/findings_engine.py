import json
from collections import Counter


class FindingsEngine:

    def analyze(self, records):

        findings = {
            "total_decisions": len(records),
            "approved": 0,
            "blocked": 0,
            "escalated": 0,
            "violations": Counter(),
            "risk_scores": [],
        }

        for r in records:

            verdict = r.get("verdict")

            if verdict == "APPROVE":
                findings["approved"] += 1

            elif verdict == "BLOCK":
                findings["blocked"] += 1

            elif verdict == "ESCALATE":
                findings["escalated"] += 1

            violation = r.get("violation_type")

            if violation:
                findings["violations"][violation] += 1

            score = r.get("risk_score")

            if score is not None:
                findings["risk_scores"].append(score)

        findings["average_risk_score"] = (
            round(sum(findings["risk_scores"]) / len(findings["risk_scores"]), 2)
            if findings["risk_scores"]
            else 0
        )

        findings["violations"] = dict(findings["violations"])

        return findings


def save_findings(findings, path):

    with open(path, "w") as f:
        json.dump(findings, f, indent=2)
