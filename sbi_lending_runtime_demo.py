import time
import uuid
import hashlib

class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    END = "\033[0m"

def banner():
    print(f"""{Colors.CYAN}

███████╗██████╗ ██╗
██╔════╝██╔══██╗██║
███████╗██████╔╝██║
╚════██║██╔══██╗██║
███████║██████╔╝██║
╚══════╝╚═════╝ ╚═╝

PRIVATEVAULT
SBI LENDING RUNTIME CONTROL PLANE

{Colors.END}
""")

def step(msg):
    print(f"\n{Colors.BLUE}[PRIVATEVAULT]{Colors.END} {msg}")
    time.sleep(1)

def merkle(payload):
    leaves = []

    for k, v in payload.items():
        h = hashlib.sha256(
            f"{k}:{v}".encode()
        ).hexdigest()

        leaves.append(h)

    root = hashlib.sha256(
        "".join(leaves).encode()
    ).hexdigest()

    return root

# ======================================================
# SCENARIO 1
# INCOME HALLUCINATION
# ======================================================

def income_hallucination():

    docs = {
        "customer":"ABC Industries",
        "annual_income":"1200000",
        "requested_loan":"5000000"
    }

    ai = {
        "annual_income":"2100000",
        "recommendation":"APPROVE",
        "loan":"5000000"
    }

    step("Loan Application Received")

    print(docs)

    step("AI Underwriter Recommendation")

    print(ai)

    step("Evidence Verification")

    failures = []

    if docs["annual_income"] != ai["annual_income"]:
        failures.append("INCOME_DRIFT")

    for f in failures:
        print(f"{Colors.RED}✗ {f}{Colors.END}")

    step("Risk Engine")

    risk = 92

    print(f"Risk Score: {risk}/100")

    step("Decision")

    print(f"""
{Colors.RED}
LOAN APPROVAL BLOCKED

Reason:
Income mismatch

Document Income:
₹12,00,000

AI Income:
₹21,00,000
{Colors.END}
""")

# ======================================================
# SCENARIO 2
# CREDIT MEMO FABRICATION
# ======================================================

def credit_memo_fabrication():

    step("Relationship Manager Upload")

    print("""
GST Returns
Bank Statements
Financial Statements
""")

    step("AI Credit Memo")

    print("""
Recommendation:
APPROVE

Reason:
Strong Cashflow
""")

    step("Evidence Traceability")

    print(f"""
{Colors.RED}
Cashflow Reference:
NOT FOUND

Supporting Evidence:
NOT FOUND

Memo Traceability:
FAILED
{Colors.END}
""")

    print(f"""
{Colors.RED}
STATUS:
BLOCKED
{Colors.END}
""")

# ======================================================
# SCENARIO 3
# FRAUD LENDING
# ======================================================

def fraud_lending():

    step("Document Verification")

    print("""
PAN Uploaded
Salary Slip Uploaded
Bank Statement Uploaded
""")

    step("AI Decision")

    print("""
Risk:
LOW

Recommendation:
APPROVE
""")

    step("PrivateVault Cross Validation")

    print(f"""
Employer:
MISMATCH

Salary:
MISMATCH

Bank Credits:
MISMATCH
""")

    print(f"""
{Colors.RED}
TRUST SCORE:
41%

DECISION:
ESCALATE
{Colors.END}
""")

# ======================================================
# SCENARIO 4
# POLICY VIOLATION
# ======================================================

def policy_violation():

    step("Collections Agent")

    print("""
Outstanding:
₹4,50,000

AI Recommendation:
Interest Waiver
""")

    step("Policy Engine")

    print(f"""
Current Policy:
NO INTEREST WAIVER

Agent Action:
INTEREST WAIVER
""")

    print(f"""
{Colors.RED}
POLICY VIOLATION

STATUS:
BLOCKED
{Colors.END}
""")

# ======================================================
# SCENARIO 5
# APPROVED CASE
# ======================================================

def approved_case():

    step("Loan Application")

    print("""
Income:
₹25,00,000

Loan:
₹50,00,000
""")

    step("Verification")

    print(f"""
{Colors.GREEN}
Income Verified
GST Verified
Cashflow Verified
Policy Passed
Fraud Check Passed
{Colors.END}
""")

    root = merkle({
        "income":"2500000",
        "loan":"5000000",
        "status":"approved"
    })

    step("Audit Package")

    print(f"""
Decision ID:
{uuid.uuid4()}

Merkle Root:
{root}

Risk:
12/100
""")

    print(f"""
{Colors.GREEN}
APPROVED

Forward To SBI LOS
{Colors.END}
""")

# ======================================================
# MENU
# ======================================================

def menu():

    banner()

    while True:

        print("""

1. Income Hallucination
2. Credit Memo Fabrication
3. Fraud Lending
4. Policy Violation
5. Approved Case
6. Exit

""")

        c = input("Select Scenario: ")

        if c == "1":
            income_hallucination()

        elif c == "2":
            credit_memo_fabrication()

        elif c == "3":
            fraud_lending()

        elif c == "4":
            policy_violation()

        elif c == "5":
            approved_case()

        elif c == "6":
            break

if __name__ == "__main__":
    menu()
