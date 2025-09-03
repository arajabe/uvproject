import streamlit as st
import requests
from ui.session import initialize_session_state
from config import API_URL
import time



initialize_session_state()

# -------------------------------
# Login Form
# -------------------------------
def login_screen():
    st.title("🔐 Login")

    username = st.text_input("User_Id")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            response = requests.post(f"{API_URL}/login", json={
                "username": username,
                "password": password
            })

            if response.status_code == 200:
                data = response.json()
                st.session_state['logged_in'] = True
                st.session_state['username'] = data["username"]
                st.session_state['logedin_role'] = data["role"]

                # Optionally fetch chat history
                try:
                    res = requests.get(f"{API_URL}/chat/history/", params={"session_id": st.session_state["session_id"]})
                    if res.ok:
                        st.session_state['chat_history'] = [(item["user"], item["bot"]) for item in res.json()]
                except:
                    st.session_state['chat_history'] = []

                st.success(f"Welcome, {data['username']}!")
                st.rerun()
            elif response.status_code == 403:
                st.error(f"Anouther user logged in for the account {username}")
            else:
                st.error("Login failed. Invalid credentials.")

        except Exception as e:
            st.error(f"Error connecting to backend: {e}")