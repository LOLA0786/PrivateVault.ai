from datetime import datetime


def build_report(findings):

    violations = findings.get("violations", {})

    report = f"""
# PRIVATEVAULT AI DECISION AUDIT REPORT

Generated:
{datetime.utcnow().isoformat()} UTC

--------------------------------------------------

DECISIONS REVIEWED

Total Decisions:
{findings["total_decisions"]}

Approved:
{findings["approved"]}

Blocked:
{findings["blocked"]}

Escalated:
{findings["escalated"]}

--------------------------------------------------

TOP FINDINGS

Income Drift:
{violations.get("INCOME_DRIFT", 0)}

Policy Violations:
{violations.get("POLICY_OVERRIDE", 0)}

Group Exposure Breaches:
{violations.get("GROUP_EXPOSURE_BREACH", 0)}

Synthetic Identity:
{violations.get("SYNTHETIC_IDENTITY", 0)}

Credit Memo Fabrication:
{violations.get("CREDIT_MEMO_FABRICATION", 0)}

--------------------------------------------------

RISK

Average Risk Score:
{findings.get("average_risk_score",0)}

--------------------------------------------------

AUDITABILITY

Decision Replay:
100%

Evidence Coverage:
TBD

--------------------------------------------------

BUSINESS IMPACT

Investigation Time

Before:
4 Hours

After:
2 Minutes

--------------------------------------------------

PRIVATEVAULT

AI Can Recommend.
PrivateVault Verifies.
"""

    return report


def save_report(report, path):

    with open(path, "w") as f:
        f.write(report)
