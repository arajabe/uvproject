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

with st.sidebar:
    option = st.selectbox('What do you want to do?',
                             ('performance')) 

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

def is_operation_allowed_teacher(msg, role):
    if role == "teacher":
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




# Send button
if st.button("get performance"):
    
    if not role:
        st.warning("Please select a role first.")
    elif not msg.strip():
        st.warning("Please enter a message.")
    
    ##elif not is_operation_allowed(msg, role):
        ##st.error(f"As a `{role}`, you are not allowed to perform this operation.")
    elif role in role_endpoints:
        try:
            endpoint = role_endpoints[role]
            res = requests.post(
                f"{API}/chat/performance",
                params={
                    "session_id": st.session_state["session_id"],
                    "message": msg
                }
            )
            data = res.json()
            st.write(f"Bot: {data.get('reply', '(No reply found)')}")
            # st.write(f"Bot: {data.get('aireply', '(AI reply not found)')}")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error(f"As a `{role}`, you are not allowed to perform this operation.")

    # Send button
if st.button("Send"):
    
    if not role:
        st.warning("Please select a role first.")
    elif not msg.strip():
        st.warning("Please enter a message.")
    
    ##elif not is_operation_allowed(msg, role):
        ##st.error(f"As a `{role}`, you are not allowed to perform this operation.")
    elif role in role_endpoints:
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
            st.write(f"Bot: {data.get('reply', '(No reply found)')}")
            # st.write(f"Bot: {data.get('aireply', '(AI reply not found)')}")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error(f"As a `{role}`, you are not allowed to perform this operation.")

    
    
    