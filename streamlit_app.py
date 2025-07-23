import streamlit as st
import requests
import pandas as pd
import datetime
import time

API_URL = "http://localhost:5000"  # Replace with your Render Flask URL

st.set_page_config(page_title="SmartCert Manager", layout="wide")
st.title("🔐 Smart Certificate Lifecycle Manager – Demo Mode")

tab1, tab2, tab3 = st.tabs(["📋 Certificate Status", "📚 Renewal Logs", "📤 Export Report"])

with tab1:
    st.subheader("📋 Demo Certificate Status (Auto-Refresh)")
    cert_placeholder = st.empty()
    demo_start = time.time()

    for i in range(3):  # Refresh for 3 intervals (5s each)
        elapsed = time.time() - demo_start
        seconds_left = max(0, 60 - int(elapsed % 60))
        expires_on = datetime.datetime.now() + datetime.timedelta(seconds=seconds_left)

        with cert_placeholder.container():
            st.markdown(f"**Domain:** `demo.smartcert.io`")
            st.markdown(f"**Expires In:** `{seconds_left} seconds`")
            st.markdown(f"**Expires On:** `{expires_on.strftime('%Y-%m-%d %H:%M:%S')}`")
        time.sleep(5)

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