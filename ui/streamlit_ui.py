import streamlit as st
import uuid
import requests

API = "http://127.0.0.1:8000"  # Adjust to your FastAPI endpoint

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())
if "role" not in st.session_state:
    st.session_state["role"] = None
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

st.title("LangGraph Chatbot (FastAPI-backed)")

# Role selection buttons
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Admin"):
        st.session_state["role"] = "admin"
with col2:
    if st.button("Student"):
        st.session_state["role"] = "student"
with col3:
    if st.button("Parent"):
        st.session_state["role"] = "parent"
with col3:
    if st.button("teacher"):
        st.session_state["role"] = "teacher"
    

# Show current role
role = st.session_state["role"]
if role:
    st.markdown(f"**Current Role:** `{role}`")

# Display chat history
st.markdown("### 💬 Chat History")
for user_msg, bot_reply in st.session_state["chat_history"]:
    st.markdown(f"**You:** {user_msg}")
    st.markdown(f"**Bot:** {bot_reply}")

# Message input (all roles can type)
msg = st.text_input("Ask your question")

# Determine if operation is allowed
def is_operation_allowed(msg, role):
    if role == "admin":
        return True
    if any(word in msg.lower() for word in ["create", "update", "delete"]):
        return False
    return True

# Send button
if st.button("Send"):
    if not role:
        st.warning("Please select a role first.")
    elif not msg.strip():
        st.warning("Please enter a message.")
    elif role == "admin":
        try:
            res = requests.post(
                f"{API}/chat/admin",
                params={
                    "session_id": st.session_state["session_id"],
                    "message": msg
                }
            )
            st.write(f"Bot: {res.json().get('reply', '(No reply found)')}")
        except Exception as e:
            st.error(f"Error: {e}")
    elif role == "teacher":
        try:
            res = requests.post(
                f"{API}/chat/teacher",
                params={
                    "session_id": st.session_state["session_id"],
                    "message": msg
                }
            )
            st.write(f"Bot: {res.json().get('reply', '(No reply found)')}")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error(f"As a `{role}`, you are not allowed to perform this operation.")