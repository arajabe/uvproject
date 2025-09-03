import streamlit as st
import pandas as pd
from ui.session import initialize_session_state
from ui.bulk_upload_admin.bulk_student_info_upload import bulk_student_info_upload
from ui.bulk_upload_admin.bulk_parent_info_upload import bulk_parent_info_upload
from ui.bulk_upload_admin.bulk_officestaff_info_upload import bulk_officestaff_info_upload
from ui.bulk_upload_admin.bulk_teacher_info_upload import bulk_teacher_info_upload
from ui.bulk_upload_admin.bulk_student_class_allocation_upload import bulk_student_class_allocation_upload
from ui.bulk_upload_admin.bulk_class_teacher_allocation_upload import bulk_class_teacher_allocation_upload
import time

initialize_session_state()

def bulk_admin_router():
        
    col1, = st.columns(1)  # example: 2 columns
    with col1:
        st.session_state["radio_action_on_regards"] = st.radio(
        "Choose the  any one option",
        ["student", "parent", "teacher", "office staff","student class allocation", "class teacher allocation"], horizontal=True)

    def bulk_router(value):
        match value :
            case "student":
                bulk_student_info_upload()
            case "parent":
                bulk_parent_info_upload()
            case "office staff":
                bulk_officestaff_info_upload()
            case "teacher":
                bulk_teacher_info_upload()
            case "student class allocation":
                bulk_student_class_allocation_upload()
            case "class teacher allocation":
                bulk_class_teacher_allocation_upload()

    
    bulk_router(st.session_state["radio_action_on_regards"])


                
        