import streamlit as st
import requests
import pandas as pd
import datetime
import time
import os
import json

API_URL = "https://cert-lifecycle-flask-api.onrender.com"  # Replace with your Render Flask URL

# Optional: Path from env or default
LOG_FILE = os.environ.get("RENEW_LOG_PATH", os.path.join(os.getcwd(), "renew_log.json"))

def get_last_renewed():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            try:
                data = json.load(f)
                return data.get("last_renewed", "")
            except:
                return ""
    return ""

# Trigger auto-refresh only when new ICA renewal happens
current_log_time = get_last_renewed()
if "last_seen_renew_time" not in st.session_state:
    st.session_state.last_seen_renew_time = current_log_time
elif current_log_time != st.session_state.last_seen_renew_time:
    st.session_state.last_seen_renew_time = current_log_time
    st.experimental_rerun()  # ⛓️ rerun only once per renewal

# UI setup
st.set_page_config(page_title="SmartCert Manager", layout="wide")
st.title("🔐 Smart Certificate Lifecycle Manager – Demo Mode")

tab1, tab2, tab3 = st.tabs(["📋 Certificate Status", "📚 Renewal Logs", "📤 Export Report"])

with tab1:
    st.subheader("📋 Demo Certificate Status (Auto-Updates via ICA)")
    expires_on = datetime.datetime.now() + datetime.timedelta(seconds=60)
    st.markdown(f"**Domain:** `demo.smartcert.io`")
    st.markdown(f"**Expires In:** `~60 seconds`")  # Static text unless you want real countdown
    st.markdown(f"**Expires On:** `{expires_on.strftime('%Y-%m-%d %H:%M:%S')}`")
    st.success(f"✅ Last Renewed (from ICA): `{current_log_time or 'N/A'}`")
    

    if st.button("🔁 Renew Certificate"):
        try:
            renew_resp = requests.post(f"{API_URL}/renew", json={"domain": "demo.smartcert.io"})
            st.success("Renewal Triggered")
            st.json(renew_resp.json())
        except Exception as e:
            st.error(f"Failed to renew: {e}")

with tab2:
    st.subheader("📚 Renewal Logs")
    try:
        logs = requests.get(f"{API_URL}/log").json()
        if logs:
            df = pd.DataFrame(logs)
            st.dataframe(df)
        else:
            st.info("No logs yet.")
    except:
        st.error("Error fetching logs.")

with tab3:
    st.subheader("📤 Export Renewal Report")
    if st.button("Generate PDF Report"):
        try:
            pdf_resp = requests.get(f"{API_URL}/export/pdf")
            st.success(f"PDF Generated: {pdf_resp.json().get('path')}")
        except:
            st.error("Failed to generate PDF")
