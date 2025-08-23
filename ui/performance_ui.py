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

def performance():

    role = st.session_state['logedin_role']

    def is_operation_allowed(msg, role):
        if role in ["admin", "teacher"]:
            return True
        if any(word in msg.lower() for word in ["create", "update", "delete","password","adition", "modification", "deletion"]):
            return False
        return True
    col1, col2, col3, col4 = st.columns(4)  # example: 2 columns

    with col1:
            st.session_state["exam"] = st.columns(1)[0].radio(
                "Exams",
                ["Termmark", "Assignement", "Split Term Mark","any question"],
                horizontal=True
            )
    if st.session_state["exam"] in ["Termmark", "Assignement", "Split Term Mark",]:
        rodio_bt = ""
        if role in ["admin", "teacher"]:
         with col2:
              rodio_bt = st.radio("select any one", ["overall", "indiviual"])
         
        if role in ["admin", "teacher"] and rodio_bt in ['overall']:
         with col3:
            st.session_state["radio_action"] = st.columns(1)[0].radio(
                "Overall",
                ["Overall_total", "Overall_subject", "Overall_trend", "Overall_rank", "Overall_strength_weaknes", ],
                horizontal=True
            )
        
        elif role in ["admin", "teacher"] and rodio_bt in ['indiviual']:
         with col3:
            st.session_state["radio_action"] = st.columns(1)[0].radio(
                "Inividual",
                ["Inividual_total", "Inividual_subject", "Inividual_trend", "Inividual_rank", "Inividual_strength_weakness", ],
                horizontal=True
            )
        elif role in ["student", "parent"]:
         with col3:
            st.session_state["radio_action"] = st.columns(1)[0].radio(
                "Inividual",
                ["Inividual_total", "Inividual_subject", "Inividual_trend", "Inividual_rank", "Inividual_strength_weakness", ],
                horizontal=True
            )
    if st.session_state["exam"] not in ["Termmark", "Assignement", "Split Term Mark",]:
        st.session_state.msg = st.text_input("Ask your question")

    if not is_operation_allowed(st.session_state.msg, role):
            st.error(f"As a `{role}`, you are not allowed to perform this operation.")

    elif st.button("Get Performance"):
            try:
                res = requests.post(
                    f"{API}/chat/performance",
                    params={
                        "session_id": st.session_state["session_id"],
                        "message": st.session_state.msg,
                        "role" : role,
                        "performance_request" : st.session_state["radio_action"],
                        "exam" : st.session_state["exam"]
                    }
                )
                data = res.json()
                st.markdown(data.get("reply", "(No reply found)"))
            except Exception as e:
                st.error(f"Error: {e}")

