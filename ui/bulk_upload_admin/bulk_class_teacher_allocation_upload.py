import streamlit as st
import pandas as pd
from session_util import initialize_session_state
from buttons.ui_button import button_upload

initialize_session_state()
API = "http://127.0.0.1:8000"  # Adjust to your FastAPI endpoint,

def bulk_class_teacher_allocation_upload():
        
        st.title("Bulk Upload class teacher allocation Info")

        button_upload()
  