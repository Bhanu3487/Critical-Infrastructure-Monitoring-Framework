import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os

# ---------- CONFIGURATION ----------

# Set your local file path here
LOG_FILE_PATH = "logs/monitor_ims.log"  # <- change this to your file path

# ---------- Helper Functions ----------

def parse_log_line(line):
    try:
        if line.startswith('"DNS Resolution"'):
            line = '{"check": "dns", "result": ' + line.split(',', 1)[1]
        data = json.loads(line)
        return {
            "timestamp": data.get("timestamp"),
            "check": data.get("check"),
            "url": data["result"].get("url"),
            "domain": data["result"].get("domain"),
            "resolved_ip": data["result"].get("resolved_ip"),
            "status": data["result"].get("status"),
            "code": data["result"].get("code"),
            "response_time": data["result"].get("response_time"),
            "avg_latency_ms": data["result"].get("avg_latency_ms"),
            "packet_loss_percent": data["result"].get("packet_loss_percent"),
        }
    except Exception:
        return None

def load_log_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        parsed_data = [parse_log_line(line.strip()) for line in lines]
        df = pd.DataFrame([entry for entry in parsed_data if entry is not None])
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
        return df.dropna(subset=["timestamp"])
    except Exception as e:
        st.error(f"Error reading log file: {e}")
        return pd.DataFrame()

# ---------- Streamlit UI ----------

st.set_page_config(page_title="Network & Service Log Monitor", layout="wide")
st.title("🛡 Network & Service Log Monitor (Local File Access)")

if not os.path.exists(LOG_FILE_PATH):
    st.error(f"❌ File not found at path: {LOG_FILE_PATH}")
else:
    df = load_log_file(LOG_FILE_PATH)

    if df.empty:
        st.warning("No valid entries in the log file.")
    else:
        urls = df["url"].dropna().unique()
        selected_url = st.selectbox("🌐 Filter by URL", options=urls)

        min_time = df["timestamp"].min().to_pydatetime()
        max_time = df["timestamp"].max().to_pydatetime()
        time_range = st.slider(
            "🕒 Select Time Range",
            min_value=min_time,
            max_value=max_time,
            value=(min_time, max_time),
            format="YYYY-MM-DD HH:mm:ss"
        )

        filtered = df[
            (df["url"] == selected_url) &
            (df["timestamp"] >= time_range[0]) &
            (df["timestamp"] <= time_range[1])
        ]

        # Summary
        st.subheader("📊 Summary Metrics")
        col1, col2, col3 = st.columns(3)
        col1.metric("✅ Uptime", filtered[filtered["status"] == "UP"].shape[0])
        col2.metric("❌ Error", filtered[filtered["status"] == "ERROR"].shape[0])
        col3.metric("⚠ Failed", filtered[filtered["status"] == "FAILED"].shape[0])

        # Graphs
        # Response Time
        st.subheader("⏱ Response Time (seconds)")
        rt_data = filtered[filtered["response_time"].notnull()]
        if not rt_data.empty:
            st.line_chart(rt_data.set_index("timestamp")["response_time"])
        else:
            st.info("No response time data.")

        # Latency
        st.subheader("📶 Latency Over Time (ms)")
        latency_data = filtered[filtered["avg_latency_ms"].notnull()]
        if not latency_data.empty:
            st.line_chart(latency_data.set_index("timestamp")["avg_latency_ms"])
        else:
            st.info("No latency data.")

        # Packet Loss
        st.subheader("📉 Packet Loss Over Time (%)")
        loss_data = filtered[filtered["packet_loss_percent"].notnull()]
        if not loss_data.empty:
            st.line_chart(loss_data.set_index("timestamp")["packet_loss_percent"])
        else:
            st.info("No packet loss data.")