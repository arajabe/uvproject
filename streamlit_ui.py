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

initialize_session_state()

if not st.session_state.logged_in:
    login_screen()
else:
    dashboard()
