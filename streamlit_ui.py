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
from ui.login_ui import login_screen
from session_util import initialize_session_state
from ui.dashboard_ui import dashboard



API = "http://127.0.0.1:8000"  # Adjust to your FastAPI endpoint

initialize_session_state()

if not st.session_state.logged_in:
    login_screen()
else:
    dashboard()
