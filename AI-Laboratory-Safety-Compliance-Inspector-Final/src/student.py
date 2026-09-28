import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Student Lab Safety Dashboard",
    layout="wide"
)

CSV_FILE = "data/lab_ppe_log.csv"

# ---------------- SESSION STATE ----------------
if "student_logged_in" not in st.session_state:
    st.session_state.student_logged_in = False

# ---------------- STUDENT LOGIN ----------------
if not st.session_state.student_logged_in:
    st.title("🎓 Student Login – Lab Safety System")

    roll_no = st.text_input("Roll Number", placeholder="e.g. 2022a1r155")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Demo credentials (as discussed)
        if roll_no == "2022a1r155" and password == "password":
            st.session_state.student_logged_in = True
            st.session_state.roll_no = roll_no
            st.success("Login successful!")
            st.query_params = {"login": "success"}
        else:
            st.error("Invalid roll number or password")

    st.stop()

# ---------------- LOAD DATA ----------------
def load_data():
    if not os.path.exists(CSV_FILE):
        return pd.DataFrame(
            columns=["time", "roll_no", "camera", "ppe_status", "decision"]
        )

    df = pd.read_csv(CSV_FILE, on_bad_lines="skip")
    df["time"] = pd.to_datetime(df["time"], errors="coerce")
    return df

df = load_data()

student_df = df[df["roll_no"] == st.session_state.roll_no]

# ---------------- DASHBOARD ----------------
st.title("🧪 Student Lab Safety Dashboard")

# -------- METRICS --------
total_visits = len(student_df)
violations = len(student_df[student_df["decision"] == "DENIED"])
allowed = len(student_df[student_df["decision"] == "ALLOWED"])

attendance_percentage = (
    (allowed / total_visits) * 100 if total_visits > 0 else 0
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Lab Entries", total_visits)
col2.metric("Allowed Entries", allowed)
col3.metric("Violations", violations)
col4.metric("Attendance %", f"{attendance_percentage:.2f}%")

st.divider()

# -------- WARNINGS STATUS --------
st.subheader("⚠️ Warning Status")

warnings = min(violations, 3)

if warnings == 0:
    st.success("No warnings. You are compliant ✅")
elif warnings < 3:
    st.warning(f"Warnings issued: {warnings} / 3")
else:
    st.error("Maximum warnings reached ❌ Access denied")

st.divider()

# -------- RECENT VIOLATIONS --------
st.subheader("🚨 PPE Violation History")

violations_df = student_df[student_df["decision"] == "DENIED"]

if violations_df.empty:
    st.success("No PPE violations detected 🎉")
else:
    st.dataframe(
        violations_df.sort_values("time", ascending=False),
        use_container_width=True
    )

st.divider()

# -------- FULL ACTIVITY LOG --------
st.subheader("📋 Complete Lab Activity Log")

if student_df.empty:
    st.info("No lab activity recorded yet.")
else:
    st.dataframe(
        student_df.sort_values("time", ascending=False),
        use_container_width=True
    )

st.divider()

# -------- INFO PANEL --------
st.info(
    """
📌 **Important Rules**
- Helmet, mask, and gloves are mandatory.
- 3 PPE violations = automatic access denial.
- Administrator is notified after 3 warnings.
- Attendance is affected by PPE violations.
"""
)

# -------- LOGOUT --------
if st.button("Logout"):
    st.session_state.student_logged_in = False
    st.query_params = {"logout": "true"}

