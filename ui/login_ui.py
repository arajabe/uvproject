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

USERS = {
    "admin_user": {"password": "admin123", "role": "admin"},
    "teacher_user": {"password": "teach123", "role": "teacher"},
    "student_user": {"password": "stud123", "role": "student"},
    "parent_user": {"password": "parent123", "role": "parent"},
}


API = "http://127.0.0.1:8000"  # Adjust to your FastAPI endpoint


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
                st.session_state['logged_in'] = True
                st.session_state['username'] = data["username"]
                st.session_state['logedin_role'] = data["role"]

                # Optionally fetch chat history
                try:
                    res = requests.get(f"{API}/chat/history/", params={"session_id": st.session_state["session_id"]})
                    if res.ok:
                        st.session_state['chat_history'] = [(item["user"], item["bot"]) for item in res.json()]
                except:
                    st.session_state['chat_history'] = []

                st.success(f"Welcome, {data['username']}!")
                st.rerun()
            else:
                st.error("Login failed. Invalid credentials.")

        except Exception as e:
            st.error(f"Error connecting to backend: {e}")