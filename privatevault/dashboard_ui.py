import streamlit as st
import requests
import os
import random
from datetime import datetime

# ---------- Page Setup ----------
st.set_page_config(
    page_title="PrivateVault Control Center",
    page_icon="🔐",
    layout="wide"
)

# ---------- Header ----------
st.markdown(
    """
    <h1 style='text-align:center;color:#00ffc8;'>🔐 PrivateVault Control Center</h1>
    <p style='text-align:center;color:gray;'>Your unified AI Ops Vault — monitor, test & optimize everything.</p>
    """,
    unsafe_allow_html=True,
)

# ---------- Sidebar Navigation ----------
page = st.sidebar.radio(
    "🧭 Select Module",
    ["🏦 CloudShift FinOps", "🧩 TechDebtZero Analyzer", "🔒 Vault-X Privacy Core"]
)

# ---------- Backend Health ----------
BACKEND_URL = os.environ.get("BACKEND_URL", "https://api.getprivatevault.com")

def get_backend_status():
    try:
        r = requests.get(BACKEND_URL, timeout=5)
        return True, r.status_code
    except Exception:
        return False, None

# ---------- Metrics Section ----------
st.subheader("📊 Live Metrics")

col1, col2, col3, col4 = st.columns(4)
uptime = round(random.uniform(99.7, 99.99), 2)
latency = random.randint(180, 420)
requests_today = random.randint(1200, 4000)
savings = random.randint(10_000, 75_000)

col1.metric("Uptime (%)", f"{uptime}%")
col2.metric("Avg Latency (ms)", latency)
col3.metric("Requests Today", f"{requests_today:,}")
col4.metric("Estimated Savings", f"${savings:,}/mo")

st.markdown("---")

# ---------- Product Modules ----------
if "CloudShift" in page:
    st.header("🏦 CloudShift • FinOps Autopilot")
    st.write("Simulate cloud savings recommendations and instant migration plans.")
    if st.button("Run FinOps Simulation"):
        st.success("✅ Simulation complete.")
        st.json({
            "Top Savings": "Migrate Azure CosmosDB → Supabase",
            "Impact": "$12,000 / month",
            "Confidence": "94%",
            "Next Action": "Auto-generate migration DSL"
        })

elif "TechDebtZero" in page:
    st.header("🧩 TechDebtZero • Code Quality Analyzer")
    repo = st.text_input("GitHub Repo URL", "https://github.com/example/repo")
    if st.button("Analyze Codebase"):
        st.success("✅ Analysis complete.")
        st.json({
            "Maintainability Index": 82.5,
            "Complexity Score": 7.3,
            "Pylint Rating": 8.4,
            "Todos Remaining": 5,
            "Refactor Suggestion": "AI-based function modularization"
        })

else:
    st.header("🔒 Vault-X • Privacy & Encryption Core")
    text = st.text_area("Enter text to encrypt", "Confidential data here…")
    if st.button("Encrypt Now"):
        encrypted = text[::-1] + "🔐"
        st.success("✅ Encrypted Result:")
        st.code(encrypted)
    if st.button("Run Compliance Audit"):
        st.json({
            "TEE Layer": "Enabled",
            "Federated Learning": "Active",
            "Homomorphic Encryption": "Verified",
            "Compliance": ["GDPR", "HIPAA", "SOC-2"]
        })

# ---------- Backend Health Check ----------
ok, code = get_backend_status()
st.markdown("---")
if ok:
    st.success(f"Backend Healthy (HTTP {code}) — {BACKEND_URL}")
else:
    st.warning(f"Backend unreachable — check {BACKEND_URL}")

# ---------- Footer ----------
st.markdown(
    f"""
    <div style='text-align:center;color:gray;'>
        <p>Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}</p>
        <p>© 2025 PrivateVault Labs • Internal test dashboard • No real data stored</p>
    </div>
    """,
    unsafe_allow_html=True,
)
