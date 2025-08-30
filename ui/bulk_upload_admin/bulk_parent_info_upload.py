import streamlit as st
import pandas as pd
from ui.session import initialize_session_state
from ui.buttons.ui_button_csv_xlsx_files_upload import button_upload

initialize_session_state()

def bulk_parent_info_upload():
        
        st.title("Bulk Upload parent Info")

        button_upload()
  