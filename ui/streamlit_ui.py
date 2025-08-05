import streamlit as st
import uuid
import requests

API = "http://127.0.0.1:8000"  # Adjust to your FastAPI endpoint

mode =""

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())
if "role" not in st.session_state:
    st.session_state["role"] = None
if "chat_history" not in st.session_state:
    res = requests.get(f"{API}/history/", params={"session_id": st.session_state["session_id"]})
    if res.ok:
        st.session_state["chat_history"] = [(item["user"], item["bot"]) for item in res.json()]
    else:
        st.session_state["chat_history"] = []

st.title("LangGraph Chatbot (FastAPI-backed)")

# Role selection buttons
with st.sidebar:
    st.write("### Select Role")

    if st.button("Admin"):
        st.session_state["role"] = "admin"

    if st.button("Student"):
        st.session_state["role"] = "student"

    if st.button("Parent"):
        st.session_state["role"] = "parent"

    if st.button("Teacher"):
        st.session_state["role"] = "teacher"

    st.markdown(f"**Current Role**: `{st.session_state.get('role', 'None')}`")  

role_options = {
    "admin": ["None","Info Related", "Performance"],
    "teacher": ["None","Mark Posting", "Performance"],
    "student": ["None","Performance"],
    "parent": ["None","Performance"]
}



# Show current role
role = st.session_state["role"]
if role:
    with st.sidebar:
    # Show options based on role
     mode = st.selectbox("Select Option", role_options.get(role, []))



if role:
    st.markdown(f"**Current Role:** `{role}`")

# Display chat history
st.markdown("### 💬 Chat History")
for user_msg, bot_reply in st.session_state["chat_history"]:
    st.markdown(f"**You:** {user_msg}")
    st.markdown(f"**Bot:** {bot_reply}")

# Message input (all roles can type)
msg = st.text_input("Ask your question")

# Function to determine if the operation is allowed based on role and message
def is_operation_allowed(msg, role):
    if role in ["admin", "teacher"]:
        return True
    if any(word in msg.lower() for word in ["create", "update", "delete"]):
        return False
    return True  # Default allow for other types of messages

role_endpoints = {
    "admin": "admin",
    "teacher": "teacher",
    "student": "performance",
    "parent": "performance"
}


if mode == "Performance":
    if not is_operation_allowed(msg, role):
        st.error(f"As a `{role}`, you are not allowed to perform this operation.")

    elif st.button("Get Performance"):
        if not role:
            st.warning("Please select a role first.")
        elif not msg.strip():
            st.warning("Please enter a message.")
        elif role in role_endpoints:
            try:
                res = requests.post(
                    f"{API}/chat/performance",
                    params={
                        "session_id": st.session_state.get("session_id", "default"),
                        "message": msg
                    }
                )
                data = res.json()
                st.success("Performance retrieved successfully.")
                st.write("Bot:", data.get("reply", "(No reply found)"))
                # st.write("AI:", data.get("aireply", "(AI reply not found)"))
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Invalid role selected.")

# --- Handle Mark Posting or Info Related Modes ---
elif mode in ["Mark Posting", "Info Related"]:
    if st.button("Send"):
        if not role:
            st.warning("Please select a role first.")
        elif not msg.strip():
            st.warning("Please enter a message.")
        elif role in role_endpoints:
            try:
                endpoint = role_endpoints[role]
                res = requests.post(
                    f"{API}/chat/{endpoint}",
                    params={
                        "session_id": st.session_state.get("session_id", "default"),
                        "message": msg
                    }
                )
                data = res.json()
                st.success("Message sent successfully.")
                st.write("Bot:", data.get("reply", "(No reply found)"))
                # st.write("AI:", data.get("aireply", "(AI reply not found)"))
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Invalid role selected.")