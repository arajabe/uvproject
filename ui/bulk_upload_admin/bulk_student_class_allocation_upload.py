import streamlit as st
import pandas as pd
from session_util import initialize_session_state
from ui.buttons.ui_button import button_upload

initialize_session_state()
API = "http://127.0.0.1:8000"  # Adjust to your FastAPI endpoint,

def bulk_student_class_allocation_upload():
        
        st.title("Bulk Upload student class allocation Info")

        button_upload()
  