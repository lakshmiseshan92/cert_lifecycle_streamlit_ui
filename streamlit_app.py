
import streamlit as st
import json
import os
import time
from datetime import datetime

st.set_page_config(page_title="Auto-Refresh Certificate Renewal Tracker (ICA-driven)")

st.title("🔄 Auto-Refresh Certificate Renewal Tracker (ICA-driven)")
st.info("This UI auto-refreshes every 5 seconds to reflect new renewal events.")

domain = "demo.smartcert.io"
log_file = "renew_log.json"

last_renewed = "N/A"
if os.path.exists(log_file):
    try:
        with open(log_file, "r") as f:
            logs = json.load(f)
            if logs.get("domain") == domain:
                last_renewed = logs.get("timestamp", "N/A")
    except Exception as e:
        st.warning(f"⚠️ Log read error: {e}")

st.markdown(f"🔐 **Domain:** `{domain}`")
st.markdown(f"🕒 **Last Renewed:** `{last_renewed}`")

if st.button("🔁 Trigger ICA Renewal"):
    st.info("📡 Waiting for ICA to renew and update log...")

st.divider()
st.markdown("📘 **Renewal History** (mocked)")
st.empty()

time.sleep(5)
st.rerun()

