import streamlit as st
import requests
import pandas as pd
import datetime
import time
import os
import json

API_URL = "https://cert-lifecycle-flask-api.onrender.com"

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

# UI config
st.set_page_config(page_title="SmartCert Manager", layout="wide")
st.title("🔐 Smart Certificate Lifecycle Manager – Demo Mode")

tab1, tab2, tab3 = st.tabs(["📋 Certificate Status", "📚 Renewal Logs", "📤 Export Report"])

# TAB 1: CERT STATUS (Auto-Refresh every 5s)
with tab1:
    # 🔁 Auto-refresh this tab every 5 seconds
    st.markdown("<meta http-equiv='refresh' content='5'>", unsafe_allow_html=True)

    st.subheader("📋 Demo Certificate Status (Auto-Updates via ICA)")
    expires_on = datetime.datetime.now() + datetime.timedelta(seconds=60)
    st.markdown(f"**Domain:** `demo.smartcert.io`")
    st.markdown(f"**Expires In:** `~60 seconds`")
    st.markdown(f"**Expires On:** `{expires_on.strftime('%Y-%m-%d %H:%M:%S')}`")

    # ICA-triggered renewal check
    current_log_time = get_last_renewed()
    if "last_seen_renew_time" not in st.session_state:
        st.session_state.last_seen_renew_time = current_log_time
    elif current_log_time != st.session_state.last_seen_renew_time:
        st.session_state.last_seen_renew_time = current_log_time
        st.experimental_rerun()

    st.success(f"✅ Last Renewed (from ICA): `{current_log_time or 'N/A'}`")

    if st.button("🔁 Renew Certificate"):
        try:
            renew_resp = requests.post(f"{API_URL}/renew", json={"domain": "demo.smartcert.io"})
            st.success("Renewal Triggered")
            st.json(renew_resp.json())
        except Exception as e:
            st.error(f"Failed to renew: {e}")

# TAB 2: LOGS
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

# TAB 3: PDF Export
with tab3:
    st.subheader("📤 Export Renewal Report")
    if st.button("Generate PDF Report"):
        try:
            pdf_resp = requests.get(f"{API_URL}/export/pdf")
            st.success(f"PDF Generated: {pdf_resp.json().get('path')}")
        except:
            st.error("Failed to generate PDF")
