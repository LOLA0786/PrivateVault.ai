import streamlit as st
from tee_enclave import ask_grok_blind

st.title("Vault-X PrivateML.ai — Demo 🐉")
st.caption("Local demo (no external keys).")

q = st.text_input("Ask the blind engine:", "Should we approve Rinky's loan?")
if st.button("Run demo"):
    st.json(ask_grok_blind(q))
