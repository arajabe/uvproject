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
from ui.sidebar_ui import sidebar
from ui.performance_ui import performance
from ui.inforelated_ui import inforelated
from ui.display_ui import displayui

initialize_session_state()
API = "http://127.0.0.1:8000"  # Adjust to your FastAPI endpoint

def dashboard():      

    # Initialize session state for inputs
    for key in ["send"]:
        if key not in st.session_state:
            st.session_state[key] = ""

    sidebar()

    role = st.session_state.role

    st.markdown(
    "<h1 style='font-size: 20px;'> LangGraph Chatbot (FastAPI-backed) Login</h1>",
    unsafe_allow_html=True
    )

    st.markdown(
    "<h1 style='font-size: 20px;'>"f"**Current Role:** `{role}`"" Login</h1>",
    unsafe_allow_html=True
)

    st.markdown(f"**Current Role:** `{role}`")
    st.markdown("### 💬 Chat History")
    st.markdown(st.session_state["fathername"])
    #for user_msg, bot_reply in st.session_state.chat_history:
        #st.markdown(f"**You:** {user_msg}")
        #st.markdown(f"**Bot:** {bot_reply}")

    role_endpoints = {
        "admin": "admin",
        "teacher": "teacher",
        "student": "performance",
        "parent": "performance"
    }
    
    st.session_state.roleendpointsrole = role_endpoints[st.session_state.role]

    def session_mode(value):
        match value:
            case "Performance":
                performance()
            case "Info Related":
                inforelated() 

    session_mode(st.session_state.mode)
      

    if st.button("Send", st.session_state['send']):
        displayui()
            