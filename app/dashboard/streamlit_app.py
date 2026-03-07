import streamlit as st
import subprocess
import json
import pandas as pd
from pathlib import Path
from PIL import Image
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components

# st_autorefresh(interval=5000, key="monitor_refresh")

# control refresh behaviour
if "pause_refresh" not in st.session_state:
    st.session_state.pause_refresh = False

if not st.session_state.pause_refresh:
    st_autorefresh(interval=5000, key="monitor_refresh")

LOG_FILE = "logs/incidents.json"

st.set_page_config(layout="wide")

st.markdown("""
<style>
            
/* Remove extra top space */
.block-container {
    padding-top: 0rem !important;
}

/* -------- Glass System Cards -------- */

.glass-card {
    background: rgba(0,255,150,0.05);
    border: 1px solid #8fdfff;
    backdrop-filter: blur(10px);
    border-radius: 12px;
    padding: 18px;
    text-align: center;
    font-weight: 600;
    font-size: 17px;
}

/* -------- Alert Panel -------- */

.alert-panel {
    width: 45%;
    margin: auto;
    border-radius: 12px;
    padding: 22px;
    border: 2px solid #00ffa6;
    background: rgba(0,255,150,0.08);
    backdrop-filter: blur(10px);
    text-align: center;
}

/* -------- Blinking Animation -------- */

@keyframes blinkGlow {
    0% { box-shadow: 0 0 8px rgba(0,255,150,0.3); }
    50% { box-shadow: 0 0 22px rgba(0,255,150,0.9); }
    100% { box-shadow: 0 0 8px rgba(0,255,150,0.3); }
}

.alert-panel {
    animation: blinkGlow 1.6s infinite;
}

/* -------- Alert Text -------- */

.alert-title {
    font-size: 22px;
    font-weight: 800;
    letter-spacing: 1px;
}

.alert-info {
    font-size: 15px;
    margin-top: 6px;
}

/* -------- Control Buttons -------- */

.control-btn {
    background: rgba(0,255,150,0.08);
    border: 1px solid #00ffa6;
    padding: 10px 18px;
    border-radius: 8px;
    text-align: center;
    font-weight: 600;
}
            
/* -------- Status Bar -------- */

.status-bar {
    width: 40%;
    margin: 12px auto;
    border-radius: 8px;
    padding: 6px;
    text-align: center;
    font-weight: 600;
    font-size: 14px;
    background: rgba(255,80,80,0.15);
    border: 1px solid rgba(255,80,80,0.4);
}

</style>
""", unsafe_allow_html=True)

st.title("🚨 AI Safety Monitoring Control Panel")

# -----------------------------
# SYSTEM PROCESS CONTROL
# -----------------------------

if "process" not in st.session_state:
    st.session_state.process = None


def start_monitoring():
    if st.session_state.process is None:
        st.session_state.process = subprocess.Popen(
            ["python", "app/main.py"]
        )


def stop_monitoring():
    if st.session_state.process:
        st.session_state.process.terminate()
        st.session_state.process = None


# -----------------------------
# LOAD INCIDENT DATA
# -----------------------------

def load_incidents():
    try:
        with open(LOG_FILE) as f:
            data = json.load(f)
            return data[::-1]
    except:
        return []


incidents = load_incidents()


# -----------------------------
# popup
# -----------------------------

@st.dialog("Incident Investigation Panel")
def show_incident_details(inc):

    st.subheader("Incident Snapshot")

    if Path(inc["image_path"]).exists():
        st.image(inc["image_path"], use_container_width=True)

    st.divider()

    col1, col2 = st.columns(2)

    # INCIDENT INFO
    with col1:
        st.subheader("Incident Information")

        st.write(f"**Incident ID:** {inc['incident_id']}")
        st.write(f"**Camera:** {inc['camera_id']}")
        st.write(f"**Detection Time:** {inc['detection_start_time']}")
        st.write(f"**Risk Escalation Time:** {inc['risk_escalation_time']}")

    # DETECTION DETAILS
    with col2:
        st.subheader("Detection Details")

        st.write(f"**People Detected:** {inc['people_count']}")
        st.write(f"**Lighting Condition:** {inc['lighting']}")
        st.write(f"**Confidence Score:** {inc['confidence']}")

    st.divider()

    # RISK ASSESSMENT
    st.subheader("Risk Assessment")

    if inc["risk_level"] == "HIGH":
        st.error(f"Risk Level: {inc['risk_level']}")
    elif inc["risk_level"] == "MEDIUM":
        st.warning(f"Risk Level: {inc['risk_level']}")
    else:
        st.success(f"Risk Level: {inc['risk_level']}")

    st.write(f"**AI Reasoning:** {inc['rag_reasoning']}")

    st.divider()

    # ALERT INFO
    st.subheader("Alert Information")

    col3, col4 = st.columns(2)

    with col3:
        st.write(f"**Alert Sent:** {inc['alert_sent']}")
        st.write(f"**Alert Method:** {inc['alert_method']}")

    with col4:
        st.write(f"**Alert Trigger Time:** {inc['alert_trigger_time']}")
        st.write(f"**Response Time:** {inc['response_time_sec']} sec")

    if st.button("Close"):
        st.session_state.pause_refresh = False
        st.rerun()

# -----------------------------
# TABS
# -----------------------------

tab1, tab2, tab3 = st.tabs(
    ["Live Monitoring", "Alerts", "Incident History"]
)

# -----------------------------
# TAB 1 — LIVE MONITORING
# -----------------------------

with tab1:

    st.markdown("### System Control")

    control_col1, control_col2, control_col3 = st.columns([1,2,1])

    with control_col2:

        colA, colB = st.columns(2)

        with colA:
            if st.button("▶ START", use_container_width=True):
                start_monitoring()

        with colB:
            if st.button("■ STOP", use_container_width=True):
                stop_monitoring()

    if st.session_state.process:
        st.markdown(
            "<div class='status-bar' style='background:rgba(0,255,120,0.15); border-color:#00ffa6;'>SYSTEM STATUS : RUNNING</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<div class='status-bar'>SYSTEM STATUS : STOPPED</div>",
            unsafe_allow_html=True
        )

    st.divider()

    # -----------------------------
    # system health indicators 
    # -----------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            '<div class="glass-card">Camera<br><span>● ONLINE</span></div>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            '<div class="glass-card">Detection<br><span>● RUNNING</span></div>',
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            '<div class="glass-card">RAG Engine<br><span>● ACTIVE</span></div>',
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            '<div class="glass-card">Alerts<br><span>● ENABLED</span></div>',
            unsafe_allow_html=True
        )
        
    st.divider()
        
        # -----------------------------
    st.subheader("Recent Incidents")

    if incidents:

        recent_incidents = incidents[:5]

        if "selected_incident" not in st.session_state:
            st.session_state.selected_incident = None

        for inc in recent_incidents:

            col1, col2 = st.columns([1.5,4])


            if Path(inc["image_path"]).exists():
                img = Image.open(inc["image_path"])
                col1.image(img, use_container_width=True)

            # compact info
            col2.markdown(
                f"""
                **{inc['incident_id']}**

                **Risk:** {inc['risk_level']}  
                **People:** {inc['people_count']}  
                **Time:** {inc['detection_start_time']}  
                **Reason:** {inc['rag_reasoning'][:50]}...
                """
            )

            # if col2.button("View Details", key=inc["incident_id"]):
            #     show_incident_details(inc)
            if col2.button("View Details", key=inc["incident_id"]):
                st.session_state.pause_refresh = True
                show_incident_details(inc)

            st.divider()

        if st.session_state.selected_incident:

            inc = st.session_state.selected_incident

            st.subheader("Incident Details")

            col1, col2 = st.columns([1,4])

            if Path(inc["image_path"]).exists():
                col1.image(inc["image_path"])

            col2.write(f"**Incident ID:** {inc['incident_id']}")
            col2.write(f"**Time:** {inc['detection_start_time']}")
            col2.write(f"**Risk Level:** {inc['risk_level']}")
            col2.write(f"**People Detected:** {inc['people_count']}")
            col2.write(f"**Lighting:** {inc['lighting']}")
            col2.write(f"**Confidence:** {inc['confidence']}")
            col2.write(f"**Reasoning:** {inc['rag_reasoning']}")
            col2.write(f"**Alert Sent:** {inc['alert_sent']}")


# -----------------------------
# TAB 2 — ALERTS
# -----------------------------

with tab2:

    st.subheader("Alert Feed")

    if incidents:

        for inc in incidents:

            col1, col2 = st.columns([1.5,4])

            # small preview image
            if Path(inc["image_path"]).exists():
                col1.image(inc["image_path"], use_container_width=True)

            # alert summary
            col2.markdown(
                f"""
                **{inc['incident_id']}**

                **Risk:** {inc['risk_level']}  
                **People:** {inc['people_count']}  
                **Time:** {inc['detection_start_time']}  
                **Reason:** {inc['rag_reasoning'][:60]}...
                """
            )

            if col2.button("View Details", key=f"alert_{inc['incident_id']}"):
                show_incident_details(inc)

            st.divider()

    else:
        st.info("No alerts recorded yet.")

# -----------------------------
# TAB 3 — HISTORY
# -----------------------------

with tab3:

    st.subheader("Incident History")

    if incidents:

        df = pd.DataFrame(incidents)

        # -----------------------------
        # Select Relevant Columns
        # -----------------------------

        cols = [
            "incident_id",
            "risk_level",
            "people_count",
            "lighting",
            "detection_start_time",
            "risk_escalation_time",
            "camera_id",
            "alert_sent",
            "alert_method",
            "alert_trigger_time",
            "response_time_sec"
        ]

        df = df[cols]

        # -----------------------------
        # Metrics
        # -----------------------------

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Incidents", len(df))
        col2.metric("High Risk", len(df[df["risk_level"] == "HIGH"]))
        col3.metric("Alerts Sent", df["alert_sent"].sum())
        col4.metric("Avg Response Time", round(df["response_time_sec"].mean(), 2))

        st.divider()

        # -----------------------------
        # Filters
        # -----------------------------

        filter_col1, filter_col2 = st.columns(2)

        risk_filter = filter_col1.selectbox(
            "Filter by Risk Level",
            ["ALL", "HIGH", "MEDIUM", "LOW"]
        )

        search_id = filter_col2.text_input("Search Incident ID")

        if risk_filter != "ALL":
            df = df[df["risk_level"] == risk_filter]

        if search_id:
            df = df[df["incident_id"].str.contains(search_id)]

        st.divider()

        # -----------------------------
        # Add Serial Number
        # -----------------------------

        df = df.reset_index(drop=True)
        df.insert(0, "S.No", range(1, len(df) + 1))

        st.divider()

        # -----------------------------
        # Risk Coloring
        # -----------------------------

        def color_risk(val):
            if val == "HIGH":
                return "color: red; font-weight: bold;"
            elif val == "MEDIUM":
                return "color: orange; font-weight: bold;"
            else:
                return "color: green; font-weight: bold;"

        styled_df = df.style.applymap(color_risk, subset=["risk_level"])

        # -----------------------------
        # Display Table
        # -----------------------------

        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No incidents recorded yet.")

