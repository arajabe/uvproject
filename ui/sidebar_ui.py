import streamlit as st
from ui.session import initialize_session_state
import requests
from config import API_URL

initialize_session_state()

def sidebar():

        # Sidebar role display
    with st.sidebar:
        st.markdown(f"**Logged in as:** `{st.session_state['username']}`")
        st.markdown(f"**Role:** `{st.session_state['logedin_role']}`")
        if st.button("Change Password"):
            st.session_state["Change Password"] = "Change Password"
        if st.button("Logout"):
            res = requests.post(f"{API_URL}/login/logout", params={
                "username": st.session_state['username']})
            if (res.status_code ==200):
                st.session_state['logged_in'] = False
                st.session_state['username'] = ""
                st.session_state['logedin_role'] = None
                st.session_state.chat_history = []
                st.rerun()
    
    role = st.session_state['logedin_role']

        # Role-based options
    role_options = {
        "admin": ["Info Related", "Performance", "Class Teacher Allocation", "Student Allocation", "bulk info and allocations", "Application Form"],
        "teacher": ["Mark Posting", "Performance", "bulk mark posting"],
        "student": ["Performance"],
        "parent": ["Performance"],
        "officestaff" :["Info Related"]
    }

    st.session_state['mode'] = st.sidebar.selectbox("Select Option", role_options.get(role, []))

