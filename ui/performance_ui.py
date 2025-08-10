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

    role = st.session_state.role

    def is_operation_allowed(msg, role):
        if role in ["admin", "teacher"]:
            return True
        if any(word in msg.lower() for word in ["create", "update", "delete"]):
            return False
        return True

    st.session_state.msg = st.text_input("Ask your question")

    if not is_operation_allowed(st.session_state.msg, role):
            st.error(f"As a `{role}`, you are not allowed to perform this operation.")

    elif st.button("Get Performance"):
            try:
                res = requests.post(
                    f"{API}/chat/performance",
                    params={
                        "session_id": st.session_state["session_id"],
                        "message": st.session_state.msg
                    }
                )
                data = res.json()
                st.markdown(data.get("reply", "(No reply found)"))
            except Exception as e:
                st.error(f"Error: {e}")

