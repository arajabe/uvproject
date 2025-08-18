import streamlit as st
import uuid
import requests
import time
from typing import TypedDict, List, Optional,Annotated
import os, json, requests
from pydantic import BaseModel, EmailStr,constr, StringConstraints
import pandas
from datetime import date
from core.model.schema import UserCreate, UserUpdate
from session_util import initialize_session_state

initialize_session_state()

API = "http://127.0.0.1:8000"  # Adjust to your FastAPI endpoint

def sidebar():

        # Sidebar role display
    with st.sidebar:
        st.markdown(f"**Logged in as:** `{st.session_state['username']}`")
        st.markdown(f"**Role:** `{st.session_state['logedin_role']}`")
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = ""
            st.session_state['logedin_role'] = None
            st.session_state.chat_history = []
            st.rerun()
    
    role = st.session_state['logedin_role']

        # Role-based options
    role_options = {
        "admin": ["None", "Info Related", "Performance", "Class Teacher Allocation", "Student Allocation", "bulk info and allocations"],
        "teacher": ["None", "Mark Posting", "Performance", "bulk mark posting"],
        "student": ["None", "Performance"],
        "parent": ["None", "Performance"]
    }

    st.session_state['mode'] = st.sidebar.selectbox("Select Option", role_options.get(role, []))

