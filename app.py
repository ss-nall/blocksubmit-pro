import streamlit as st
import base64
from datetime import datetime

from blockchain import Blockchain
from streak import display_streak_calendar, get_streak_badge

# 🔐 Initialize session state
if "users" not in st.session_state:
    st.session_state.users = {}

# 🌟 UI Header
st.set_page_config(page_title="BlockSubmit Pro", layout="centered")
st.title("🚀 BlockSubmit Pro")

# 👤 Login
username = st.text_input("Enter your name:")
if not username:
    st.stop()

# 🧠 User init
if username not in st.session_state.users:
    st.session_state.users[username] = {
        "projects": {},
        "role": "student"  # default
    }

user_data = st.session_state.users[username]

# 🔁 Role Switch
is_faculty = st.checkbox("👨‍🏫 I am faculty", value=user_data["role"] == "faculty")
user_data["role"] = "faculty" if is_faculty else "student"

# ================================
# STUDENT DASHBOARD
# ================================
if user_data["role"] == "student":
    st.success(f"Welcome, {username}! (Student)")

    # 📁 Create Project
    st.header("📁 Create Project")
    proj_name = st.text_input("New Project Name:")
    if st.button("Create Project"):
        if proj_name in user_data["projects"]:
            st.warning("Project already exists.")
        elif proj_name.strip() == "":
            st.warning("Project name cannot be empty.")
        else:
            user_data["projects"][proj_name] = {
                "start_date": datetime.now().strftime("%Y-%m-%d"),
                "blockchain": Blockchain(),
                "feedback": {}
            }
            st.success(f"Created project: {proj_name}")

    # 📤 Upload Progress
    st.header("📌 Upload Progress")
    if user_data["projects"]:
        selected_proj = st.selectbox("Choose Project", list(user_data["projects"].keys()))
        proj = user_data["projects"][selected_proj]

        st.caption(f"Started on: {proj['start_date']}")
        file = st.file_uploader("Upload file:")
        if file:
            content = base64.b64encode(file.read()).decode()
            data = {"filename": file.name, "content": content}
            proj["blockchain"].add_block(data)
            st.success(f"Uploaded: {file.name}")

        # 📜 Submission History
        st.header("📜 Submission History")
        history = proj["blockchain"].get_history()
        if history:
            for i, item in enumerate(reversed(history), 1):
                st.markdown(f"**{i}.** 📄 `{item['filename']}` — _{item['timestamp']}_")
                file_bytes = base64.b64decode(proj["blockchain"].chain[-i].data["content"])
                st.download_button("⬇️ Download", file_bytes, file_name=item["filename"], key=f"dl_{i}")
                feedback = proj["feedback"].get(item["timestamp"])
                if feedback:
                    st.info(f"💬 Faculty Feedback: {feedback}")
        else:
            st.info("No submissions yet.")

        # 🔥 Streak & Badges
        st.subheader("🔥 Streak Calendar")
        dates = proj["blockchain"].get_submission_dates()
        display_streak_calendar(dates)
        badge = get_streak_badge(dates)
        if badge:
            st.success(f"🏅 You earned a badge: {badge}")
    else:
        st.info("Create a project to begin.")

# ================================
# FACULTY DASHBOARD
# ================================
else:
    st.success(f"Welcome, {username}! (Faculty)")
    st.header("📚 Student Submissions")

    for student, s_data in st.session_state.users.items():
        if s_data["role"] != "student":
            continue
        st.subheader(f"👩‍🎓 {student}")
        for pname, pdata in s_data["projects"].items():
            st.markdown(f"**📁 {pname}** — _Started: {pdata['start_date']}_")
            history = pdata["blockchain"].get_history()
            if not history:
                st.info("No submissions.")
                continue
            for h in history:
                st.markdown(f"- 📄 `{h['filename']}` — _{h['timestamp']}_")
                feedback = st.text_input(
                    f"💬 Feedback for {h['filename']} ({student})",
                    key=f"{student}_{pname}_{h['timestamp']}"
                )
                if feedback.strip():
                    pdata["feedback"][h["timestamp"]] = feedback
