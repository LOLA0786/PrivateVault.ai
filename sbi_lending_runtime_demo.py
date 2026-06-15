#!/usr/bin/env python3
"""PrivateVault - SBI Lending Runtime Control Plane (Enhanced Demo)
Regulatory thresholds/values are ILLUSTRATIVE. Verify vs current SBI credit
policy + RBI Master Directions before any live banker/customer demo."""
import hashlib, json, uuid, sys
from datetime import datetime, timezone

class C:
    R="\033[91m";G="\033[92m";Y="\033[93m";B="\033[94m";M="\033[95m";CY="\033[96m";BOLD="\033[1m";DIM="\033[2m";END="\033[0m"
def hr():print(C.DIM+"-"*66+C.END)
def stage(t):print(f"\n{C.B}{C.BOLD}[PRIVATEVAULT] {t}{C.END}")
def kv(k,v,color=C.END):print(f"  {C.DIM}{k:<30}{C.END}{color}{v}{C.END}")
def block(r):print(f"\n{C.R}{C.BOLD}  [X] DECISION: BLOCKED{C.END}\n  {C.R}{r}{C.END}")
def escalate(r):print(f"\n{C.Y}{C.BOLD}  [!] DECISION: ESCALATE -> maker-checker queue{C.END}\n  {C.Y}{r}{C.END}")
def approve():print(f"\n{C.G}{C.BOLD}  [OK] DECISION: APPROVED -> forward to SBI LOS{C.END}")
def h(o):return hashlib.sha256(json.dumps(o,sort_keys=True,default=str).encode()).hexdigest()
def merkle_root(leaves):
    layer=[hashlib.sha256(x.encode()).hexdigest() for x in sorted(leaves)]
    if not layer:return hashlib.sha256(b"").hexdigest()
    while len(layer)>1:
        if len(layer)%2:layer.append(layer[-1])
        layer=[hashlib.sha256((layer[i]+layer[i+1]).encode()).hexdigest() for i in range(0,len(layer),2)]
    return layer[0]
def audit_packet(d,ev):
    return {"decision_id":str(uuid.uuid4()),"timestamp":datetime.now(timezone.utc).isoformat(),
            "policy_version":POLICY["version"],"intent_hash":h(d),"evidence_hash":h(sorted(ev)),"merkle_root":merkle_root(ev)}
def show_audit(p):
    stage("Cryptographic Audit Package (tamper-evident)")
    kv("Decision ID",p["decision_id"],C.CY);kv("Timestamp (UTC)",p["timestamp"])
    kv("Policy Version",p["policy_version"]);kv("Intent Hash",p["intent_hash"][:40]+"...")
    kv("Evidence Hash",p["evidence_hash"][:40]+"...");kv("Merkle Root",p["merkle_root"],C.M)
def emi(p,rate,m):
    r=rate/12/100
    return p/m if r==0 else p*r*(1+r)**m/((1+r)**m-1)
def foir_pct(obl,e,nmi):return round((obl+e)/nmi*100,1)
def inr(n):
    x=str(int(n))
    if len(x)<=3:return "Rs "+x
    last3=x[-3:];rest=x[:-3];parts=[]
    while len(rest)>2:parts.insert(0,rest[-2:]);rest=rest[:-2]
    if rest:parts.insert(0,rest)
    return "Rs "+",".join(parts)+","+last3
POLICY={"version":"SBI-RETAIL-CREDIT-v2026.2 (demo)","max_foir_pct":55.0,"min_cibil":700,
        "max_ltv_pct":75.0,"interest_waiver_authority":False,"single_borrower_limit":50_00_000,"group_exposure_limit":1_00_00_000}

def s1_income_hallucination():
    stage("Loan Application Received  |  Channel: YONO Business")
    app={"borrower":"ABC Industries (Prop: R. Sharma)","pan":"AABCA1234F","product":"Business Term Loan","requested_loan":50_00_000,"tenor_months":240,"roi_pct":9.5}
    for k,v in app.items():kv(k,inr(v) if isinstance(v,int) and v>1000 else v)
    stage("Evidence on File (account aggregator + bureau pull)")
    vi=12_00_000;obl=25_000;cibil=762
    kv("Verified Annual Income (ITR/26AS)",inr(vi),C.G);kv("Existing EMI obligations/mo",inr(obl))
    kv("CIBIL Score",f"{cibil}",C.G if cibil>=POLICY["min_cibil"] else C.R)
    stage("AI Underwriter Recommendation")
    ai=21_00_000;kv("AI-asserted Annual Income",inr(ai),C.R);kv("AI Recommendation","APPROVE",C.R)
    e=emi(app["requested_loan"],app["roi_pct"],app["tenor_months"])
    stage("Runtime Control: Evidence Binding + FOIR Recompute")
    kv("Computed EMI",inr(round(e))+"/mo")
    kv("FOIR @ AI income",f"{foir_pct(obl,e,ai/12)}%  (PASS <= {POLICY['max_foir_pct']}%)",C.Y)
    kv("FOIR @ verified income",f"{foir_pct(obl,e,vi/12)}%  (BREACH)",C.R)
    kv("Income source binding","NO SOURCE DOC HASH -> INCOME_DRIFT",C.R)
    kv("Drift magnitude",f"+{round((ai-vi)/vi*100)}% over evidence",C.R)
    block("Underwriter income unsupported by filed evidence. FOIR on verified income breaches policy. Typology: INCOME INFLATION.")
    show_audit(audit_packet({"action":"loan_approval","pan":app["pan"],"verdict":"BLOCK"},["ITR_FY25:"+h({"inc":vi}),"Form26AS:"+h({"t":1}),"CIBIL:"+h({"s":cibil})]))

def s2_credit_memo_fabrication():
    stage("Relationship Manager Upload  |  SME Working Capital")
    kv("Borrower","Meridian Textiles Pvt Ltd");kv("Docs uploaded","GSTR-1, GSTR-3B, Bank Stmt (6mo), Financials")
    stage("AI Credit Memo");kv("Recommendation","APPROVE",C.R);kv("Stated basis","'Strong cashflow; DSCR 1.8x; collateral cover 1.4x'",C.R)
    stage("Runtime Control: Memo Citation Traceability")
    for c,s in [("DSCR 1.8x","NOT FOUND in uploaded financials"),("Collateral cover 1.4x","No valuation report on file"),("Strong cashflow","GSTR-3B shows 3 nil-filing months")]:kv(c,s,C.R)
    kv("Memo -> evidence hash match","FAILED (0/3 claims grounded)",C.R)
    block("Memo asserts metrics with no traceable source. Typology: CREDIT MEMO FABRICATION (ungrounded LLM justification).")
    show_audit(audit_packet({"action":"memo_approval","verdict":"BLOCK"},["GSTR3B:"+h({"nil":3}),"BankStmt:"+h({"bal":84000})]))

def s3_synthetic_identity_fraud():
    stage("Document Verification  |  Personal Loan (digital STP)")
    kv("Applicant","S. Verma  |  PAN: BXZPV9912K");kv("Docs","PAN, Salary Slip, Bank Statement (uploaded)")
    stage("AI Decision");kv("AI Risk","LOW",C.R);kv("AI Recommendation","APPROVE",C.R)
    stage("Runtime Control: Multi-Source Cross-Validation")
    for k,v in [("Employer (EPFO vs slip)","MISMATCH - employer not in EPFO"),("Salary (slip vs bank credit)","MISMATCH - no matching credit"),("Bank credits (AA vs stmt)","MISMATCH - statement edited"),("CIBIL profile","THIN FILE - 2 enquiries in 7 days (velocity)")]:kv(k,v,C.R)
    kv("Composite Trust Score","41%",C.R)
    escalate("Identity and income fail cross-source corroboration. Typology: SYNTHETIC IDENTITY / STATEMENT TAMPERING. Routed to fraud-control unit, not auto-rejected.")
    show_audit(audit_packet({"action":"loan_approval","verdict":"ESCALATE","trust":41},["EPFO:"+h({"f":False}),"AA:"+h({"edit":True})]))

def s4_policy_violation():
    stage("Collections Agent Action  |  NPA Bucket 2")
    kv("Borrower","K. Nair  |  Loan A/c xxxx-4471");kv("Outstanding",inr(4_50_000));kv("AI Recommendation","Offer 100% interest waiver to close",C.R)
    stage("Runtime Control: Policy + Authority Matrix")
    kv("Current policy","NO INTEREST WAIVER (recovery policy v2026.1)",C.G);kv("Agent authority","Collections agent - NO waiver authority",C.R)
    kv("Attempted action","INTEREST WAIVER (100%)",C.R);kv("Authority check","DENIED - exceeds delegated powers",C.R)
    block("Action violates recovery policy and exceeds agent's delegated authority. Typology: POLICY OVERRIDE / UNAUTHORIZED CONCESSION.")
    show_audit(audit_packet({"action":"interest_waiver","verdict":"BLOCK"},["Policy:"+h({"w":False}),"Role:"+h({"auth":False})]))

def s5_clean_approval():
    stage("Loan Application  |  Home Loan")
    app={"borrower":"A. Iyer","pan":"CKPPI4456L","requested_loan":50_00_000,"property_value":70_00_000,"tenor_months":240,"roi_pct":8.7}
    vi=25_00_000;obl=18_000;cibil=791;e=emi(app["requested_loan"],app["roi_pct"],app["tenor_months"])
    foir=foir_pct(obl,e,vi/12);ltv=round(app["requested_loan"]/app["property_value"]*100,1)
    for k,v in app.items():kv(k,inr(v) if isinstance(v,int) and v>1000 else v)
    stage("Runtime Verification (all controls)")
    kv("Verified Income (ITR/26AS)",inr(vi),C.G);kv("CIBIL Score",f"{cibil}  (>= {POLICY['min_cibil']})",C.G)
    kv("Computed EMI",inr(round(e))+"/mo");kv("FOIR",f"{foir}%  (<= {POLICY['max_foir_pct']}%)",C.G)
    kv("LTV",f"{ltv}%  (<= {POLICY['max_ltv_pct']}%)",C.G);kv("GST / Cashflow / Fraud","VERIFIED / VERIFIED / PASSED",C.G)
    kv("Single-borrower limit","within limit",C.G)
    approve()
    show_audit(audit_packet({"action":"loan_approval","verdict":"APPROVE","foir":foir,"ltv":ltv,"cibil":cibil,"risk":12},["ITR:"+h({"inc":vi}),"Val:"+h({"v":app["property_value"]}),"CIBIL:"+h({"s":cibil}),"GST:"+h({"ok":True})]))

def s6_group_exposure_breach():
    stage("Sanction Request  |  Connected-Party / Group Exposure")
    kv("New facility","Zenith Logistics Pvt Ltd  ->  "+inr(40_00_000))
    kv("Single-borrower limit",inr(POLICY["single_borrower_limit"])+"  (PASS individually)",C.G)
    stage("Runtime Control: Aggregate Group-Exposure Check")
    related=[("Zenith Logistics (this)",40_00_000),("Zenith Warehousing (same UBO)",35_00_000),("Zenith Transport LLP (same UBO)",40_00_000)]
    total=sum(v for _,v in related)
    for n,a in related:kv(n,inr(a))
    kv("Aggregate group exposure",inr(total),C.R);kv("Group exposure limit",inr(POLICY["group_exposure_limit"]),C.Y)
    kv("Status","BREACH - each loan passes alone; sum exceeds limit",C.R)
    block("Connected entities individually within limit, aggregate breaches group exposure cap. Typology: EXPOSURE SPLITTING / DECOMPOSITION. This is the attack single-call enforcement misses.")
    show_audit(audit_packet({"action":"sanction","verdict":"BLOCK","total":total},["UBO:"+h({"linked":3}),"Exp:"+h({"t":total})]))

SCENARIOS={"1":("Income Hallucination",s1_income_hallucination),"2":("Credit Memo Fabrication",s2_credit_memo_fabrication),"3":("Synthetic Identity / Forgery",s3_synthetic_identity_fraud),"4":("Policy Violation (Collections)",s4_policy_violation),"5":("Clean Approval (straight-through)",s5_clean_approval),"6":("Group Exposure Breach (aggregate)",s6_group_exposure_breach)}

def banner():
    print(C.CY+C.BOLD+"\n  PRIVATEVAULT  |  SBI LENDING RUNTIME CONTROL PLANE\n  pre-execution governance for AI underwriting\n"+C.END)
def menu():
    banner()
    while True:
        hr()
        for k,(n,_) in SCENARIOS.items():print(f"  {C.BOLD}{k}{C.END}. {n}")
        print(f"  {C.BOLD}0{C.END}. Run ALL   |   {C.BOLD}q{C.END}. Exit");hr()
        ch=input(f"{C.CY}Select Scenario: {C.END}").strip().lower()
        if ch in ("q","exit"):break
        elif ch=="0":
            for _,fn in SCENARIOS.values():fn();print()
        elif ch in SCENARIOS:SCENARIOS[ch][1]();print()
        else:print(C.R+"Invalid selection."+C.END)
if __name__=="__main__":
    if "--selftest" in sys.argv:
        for _,fn in SCENARIOS.values():fn();print()
    else:menu()
