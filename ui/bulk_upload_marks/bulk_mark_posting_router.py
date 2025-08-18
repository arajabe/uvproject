import streamlit as st
import pandas as pd
from session_util import initialize_session_state
from ui.bulk_upload_marks.bulk_subject_term_split_upload import bulk_subject_term_split
from ui.bulk_upload_marks.bulk_assignement_upload import bulk_assignement
from ui.bulk_upload_marks.bulk_term_mark_upload import bulk_term_mark

initialize_session_state()
API = "http://127.0.0.1:8000"  # Adjust to your FastAPI endpoint,

def bulk_mark_posting_router():
        
    col1, = st.columns(1)  # example: 2 columns
    with col1:
        st.session_state["radio_action_on_regards"] = st.radio(
        "Choose the  any one option",
        ["Assignement", "Subject Term Split", "Term Mark"], horizontal=True)

    def bulk_router(value):    
        match value :
            case "Subject Term Split":
                bulk_subject_term_split()
            case "Assignement":
                bulk_assignement()
            case "Term Mark":
                bulk_term_mark()
    
    bulk_router(st.session_state["radio_action_on_regards"])


                
        