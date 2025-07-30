import streamlit as st
import requests, uuid

API = "http://127.0.0.1:8000"
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

st.title("LangGraph Chatbot (FastAPI-backed)")

msg = st.text_input("Ask (e.g., 'create user Alice alice@x.com', 'delete user 2')")
if st.button("Send"):
    res = requests.post(f"{API}/chat/", params={"session_id": st.session_state["session_id"], "message": msg})
    st.write(f"Bot: {res.json()['reply']}")