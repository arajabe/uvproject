import streamlit as st
import pandas as pd
from session_util import initialize_session_state
from ui.buttons.ui_button import button_upload

initialize_session_state()

def bulk_officestaff_info_upload():
        
        st.title("Bulk Upload office staff Info")

        button_upload()
  