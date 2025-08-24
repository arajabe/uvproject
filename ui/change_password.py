import streamlit as st
import requests
import requests
from session_util import initialize_session_state
from config import API_URL

initialize_session_state()

def change_password():

    username = st.session_state['username']

    with st.form("password_form"):
        old_password = st.text_input("Old Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")

        submit = st.form_submit_button("Update Password")

    # Button renamed here 👇
    if submit:
        if not old_password or not new_password or not confirm_password:
            st.warning("⚠️ Please fill in all fields")
            return

        if new_password != confirm_password:
            st.error("❌ New password and confirmation do not match")
            return

        payload = {
            "username": username,   # or user_id from session
            "old_password": old_password,
            "new_password": new_password
        }
        try:
            response = requests.post(f"{API_URL}/login/change-password", json=payload)

            if response.status_code == 200:
                st.success("✅ Password changed successfully! Please login again.")
                # Optionally force logout
                if "username" in st.session_state:
                    del st.session_state["username"]

            else:
                st.error(f"❌ Error: {response.json().get('detail', 'Something went wrong')}")

        except requests.exceptions.RequestException as e:
            st.error(f"🚨 Could not connect to server: {e}")