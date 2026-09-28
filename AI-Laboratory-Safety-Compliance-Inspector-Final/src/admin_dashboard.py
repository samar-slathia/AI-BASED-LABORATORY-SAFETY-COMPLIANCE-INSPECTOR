import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

st.set_page_config(page_title="AI Lab Safety Admin Dashboard", layout="wide")
CSV_FILE = "data/lab_ppe_log.csv"

# ----------------- SESSION STATE SETUP -----------------
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if "rerun_flag" not in st.session_state:
    st.session_state.rerun_flag = False  # For rerun-safe refresh

# ----------------- ADMIN LOGIN -----------------
if not st.session_state.admin_logged_in:
    st.subheader("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.admin_logged_in = True
            st.success("Login Successful!")
            # Rerun-safe refresh using st.query_params
            st.query_params = {"rerun": str(not st.session_state.rerun_flag)}
            st.session_state.rerun_flag = not st.session_state.rerun_flag
        else:
            st.error("Invalid credentials")
    st.stop()  # Stop until login

# ----------------- LOAD DATA -----------------
def load_data():
    if not os.path.exists(CSV_FILE):
        return pd.DataFrame(columns=["time","roll_no","camera","ppe_status","decision"])
    try:
        df = pd.read_csv(CSV_FILE, on_bad_lines='skip')
        for col in ["time","roll_no","camera","ppe_status","decision"]:
            if col not in df.columns:
                df[col] = ""
        df["time"] = pd.to_datetime(df["time"], errors="coerce")
        df["hour"] = df["time"].dt.hour
        return df
    except:
        return pd.DataFrame(columns=["time","roll_no","camera","ppe_status","decision"])

# ----------------- PDF EXPORT -----------------
def generate_pdf(df, filename="PPE_Report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0,10,"AI Lab Safety Compliance Report", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", size=10)
    pdf.cell(0,8,f"Total Checks: {len(df)}", ln=True)
    pdf.cell(0,8,f"Allowed: {len(df[df['decision']=='ALLOWED'])}", ln=True)
    pdf.cell(0,8,f"Denied: {len(df[df['decision']=='DENIED'])}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial","B",10)
    pdf.cell(0,8,"Recent Alerts (DENIED):", ln=True)
    pdf.set_font("Arial", size=9)
    for _, row in df[df["decision"]=="DENIED"].tail(10).iterrows():
        pdf.cell(0,6,f"{row['time']} | {row['roll_no']} | {row['ppe_status']}", ln=True)
    pdf.output(filename)

# ----------------- DASHBOARD -----------------
df = load_data()

st.subheader("Metrics")
total_checks = len(df)
allowed = len(df[df["decision"]=="ALLOWED"])
denied = len(df[df["decision"]=="DENIED"])
col1, col2, col3 = st.columns(3)
col1.metric("Total Checks", total_checks)
col2.metric("Allowed", allowed)
col3.metric("Denied", denied)

st.divider()

# ----------------- CHARTS -----------------
left, right = st.columns(2)
with left:
    st.subheader("Decision Performance")
    fig1, ax1 = plt.subplots(figsize=(4,3))
    ax1.bar(["Allowed","Denied"], [allowed, denied], color=["green","red"])
    ax1.set_ylabel("Count")
    st.pyplot(fig1)

with right:
    st.subheader("Activity Over Time")
    activity = df.groupby("hour").size().reindex(range(0,24), fill_value=0)
    fig2, ax2 = plt.subplots(figsize=(4,3))
    ax2.plot(activity.index, activity.values, marker='o')
    ax2.set_xlabel("Hour of Day")
    ax2.set_ylabel("Checks")
    st.pyplot(fig2)

st.divider()

# ----------------- ALERT LOGS -----------------
st.subheader("🚨 PPE Violations")
alert_df = df[df["decision"]=="DENIED"]
if alert_df.empty:
    st.success("No violations detected 🎉")
else:
    st.dataframe(alert_df.sort_values("time", ascending=False).head(20), use_container_width=True)

# ----------------- EXPORT -----------------
st.subheader("📤 Export Reports")
col_csv, col_pdf = st.columns(2)
with col_csv:
    st.download_button(
        label="⬇ Download CSV",
        data=df.to_csv(index=False),
        file_name="lab_ppe_report.csv",
        mime="text/csv",
        key="csv_download_btn"
    )
with col_pdf:
    if st.button("📄 Generate PDF", key="pdf_generate_btn"):
        generate_pdf(df)
        st.success("PDF generated")

st.divider()

# ----------------- GRANT / DENY ACCESS -----------------
st.subheader("🎯 Grant/Deny Access")
for idx, row in alert_df.iterrows():
    st.write(f"Student: {row['roll_no']} | PPE Status: {row['ppe_status']} | Decision: {row['decision']}")
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"Grant Access {row['roll_no']}", key=f"grant_{idx}"):
            df.loc[idx, "decision"] = "ALLOWED"
            df.to_csv(CSV_FILE, index=False)
            st.success(f"Access granted to {row['roll_no']}")
            # Refresh safely using query params
            st.query_params = {"rerun": str(not st.session_state.rerun_flag)}
            st.session_state.rerun_flag = not st.session_state.rerun_flag
    with col2:
        if st.button(f"Deny Access {row['roll_no']}", key=f"deny_{idx}"):
            df.loc[idx, "decision"] = "DENIED"
            df.to_csv(CSV_FILE, index=False)
            st.warning(f"Access denied to {row['roll_no']}")
            # Refresh safely using query params
            st.query_params = {"rerun": str(not st.session_state.rerun_flag)}
            st.session_state.rerun_flag = not st.session_state.rerun_flag

st.divider()

# ----------------- RECENT LOGS -----------------
st.subheader("Recent Activity Logs")
st.dataframe(df.sort_values("time", ascending=False).head(15), use_container_width=True)

