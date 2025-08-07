import streamlit as st
import uuid
import requests

API = "http://127.0.0.1:8000"  # Adjust to your FastAPI endpoint

# -------------------------------
# User Credentials (Hardcoded)
# -------------------------------
USERS = {
    "admin_user": {"password": "admin123", "role": "admin"},
    "teacher_user": {"password": "teach123", "role": "teacher"},
    "student_user": {"password": "stud123", "role": "student"},
    "parent_user": {"password": "parent123", "role": "parent"},
}

# -------------------------------
# Session Initialization
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = None
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------------
# Login Form
# -------------------------------
def login_screen():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            response = requests.post(f"{API}/login", json={
                "username": username,
                "password": password
            })

            if response.status_code == 200:
                data = response.json()
                st.session_state.logged_in = True
                st.session_state.username = data["username"]
                st.session_state.role = data["role"]

                # Optionally fetch chat history
                try:
                    res = requests.get(f"{API}/chat/history/", params={"session_id": st.session_state["session_id"]})
                    if res.ok:
                        st.session_state.chat_history = [(item["user"], item["bot"]) for item in res.json()]
                except:
                    st.session_state.chat_history = []

                st.success(f"Welcome, {data['username']}!")
                st.rerun()
            else:
                st.error("Login failed. Invalid credentials.")

        except Exception as e:
            st.error(f"Error connecting to backend: {e}")
# -------------------------------
# Main App UI After Login
# -------------------------------
def main_app():
    st.title("LangGraph Chatbot (FastAPI-backed)")

    # Initialize session state for inputs
    for key in ["id", "name", "email", "action", "mode", "send"]:
        if key not in st.session_state:
            st.session_state[key] = ""

    # Sidebar role display
    with st.sidebar:
        st.markdown(f"**Logged in as:** `{st.session_state.username}`")
        st.markdown(f"**Role:** `{st.session_state.role}`")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.role = None
            st.session_state.chat_history = []
            st.rerun()

    role = st.session_state.role

    # Role-based options
    role_options = {
        "admin": ["None", "Info Related", "Performance"],
        "teacher": ["None", "Mark Posting", "Performance"],
        "student": ["None", "Performance"],
        "parent": ["None", "Performance"]
    }

    st.session_state["mode"] = st.sidebar.selectbox("Select Option", role_options.get(role, []))

    st.markdown(f"**Current Role:** `{role}`")
    st.markdown("### 💬 Chat History")
    for user_msg, bot_reply in st.session_state.chat_history:
        st.markdown(f"**You:** {user_msg}")
        st.markdown(f"**Bot:** {bot_reply}")

    def is_operation_allowed(msg, role):
        if role in ["admin", "teacher"]:
            return True
        if any(word in msg.lower() for word in ["create", "update", "delete"]):
            return False
        return True

    role_endpoints = {
        "admin": "admin",
        "teacher": "teacher",
        "student": "performance",
        "parent": "performance"
    }

    if st.session_state["mode"] == "Performance":
        msg = st.text_input("Ask your question")
        if not is_operation_allowed(msg, role):
            st.error(f"As a `{role}`, you are not allowed to perform this operation.")
        elif st.button("Get Performance"):
            try:
                res = requests.post(
                    f"{API}/chat/performance",
                    params={
                        "session_id": st.session_state["session_id"],
                        "message": msg
                    }
                )
                data = res.json()
                st.markdown(data.get("reply", "(No reply found)"))
            except Exception as e:
                st.error(f"Error: {e}")

    elif st.session_state["mode"] in ["Mark Posting", "Info Related"]:        
        
        if st.session_state["mode"] == "Info Related":
         

         st.session_state["action"] = st.text_input("What is your request?", st.session_state["action"])

        st.session_state["action"] = st.session_state["action"].lower()

        if any(word in st.session_state["action"] for word in ["create", "add"]):
            st.session_state["name"] = st.text_input("name", st.session_state["name"])
            st.session_state["email"] = st.text_input("email", st.session_state["email"])

        elif any(word in st.session_state["action"] for word in ["update", "modify", "change"]):
            st.session_state["id"] = st.text_input("id", st.session_state["id"])
            st.session_state["name"] = st.text_input("name", st.session_state["name"])
            st.session_state["email"] = st.text_input("email", st.session_state["email"])

        elif any(word in st.session_state["action"] for word in ["delete"]):
            st.session_state["id"] = st.text_input("id", st.session_state["id"])

        msg = f"{st.session_state['action']} : {st.session_state['id']} name: {st.session_state['name']} email:{st.session_state['email']}"

        if st.button("Send", st.session_state['send']):
            try:
                endpoint = role_endpoints[role]
                res = requests.post(
                    f"{API}/chat/{endpoint}",
                    params={
                        "session_id": st.session_state["session_id"],
                        "message": msg
                    }
                )
                data = res.json()
                if res.status_code == 200:
                    st.success("Message sent successfully.")
                    st.markdown(f"**Bot:** {data.get('reply', '(No reply found)')}")

                    # Reset session state and restart from beginning
                    if st.button("Reset"):
                        for key in ["id", "name", "email", "action", "mode", "send"]:
                            st.session_state[key] = ""
                        st.rerun()
                    st.session_state["action"] = "how can i help you"
                    st.session_state["name"] = ""
                    st.session_state["email"] = ""
                    st.session_state["id"] = ""
                else:
                    st.error(f"Failed with status code: {res.status_code}")

            except Exception as e:
                st.error(f"Error: {e}")

# -------------------------------
# App Controller
# -------------------------------
if not st.session_state.logged_in:
    login_screen()
else:
    main_app()