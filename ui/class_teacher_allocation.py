import streamlit as st
from core.model.schema import (ClassTeacherAllocationCreate, ClassTeacherAllocationUpdate, AuditDelete)
from session_util import initialize_session_state

initialize_session_state()
API = "http://127.0.0.1:8000"  # Adjust to your FastAPI endpoint,

def class_teacher_allocation():
        
        col1, col2 = st.columns(2)  # example: 2 columns

        with col1:
            st.session_state["radio_action"] = st.columns(1)[0].radio(
                "Choose action",
                ["none","create", "update", "delete", "view"],
                horizontal=True
            )
        
        if st.session_state["radio_action"] != "none":
            with col2:
                st.session_state["radio_action_on_regards"] = st.radio(
                "Choose the  any one option",
                ["none", "Class Teacher Allocation"],
                horizontal=True
            )
                
        if (st.session_state["radio_action"] == "none"):
            st.session_state["action"] = st.text_input("What is your request?", st.session_state["action"])
            st.session_state["action"] = st.session_state["action"].lower()
        
        msg_parts = ""

        class_teacher_allocation_create = ClassTeacherAllocationCreate.__annotations__
        class_teacher_allocation_update = ClassTeacherAllocationUpdate.__annotations__
        audit_table_delete = AuditDelete.__annotations__

        if st.session_state["radio_action"] == "create" and st.session_state["radio_action_on_regards"] == "Class Teacher Allocation":      
            for field_name in class_teacher_allocation_create:
                st.session_state[field_name] = st.text_input(field_name.capitalize())
            
            msg_parts = [f"{field_name}:{st.session_state[field_name]}" for field_name in class_teacher_allocation_create
                         if st.session_state.get(field_name, "").strip() != ""]
            
        elif st.session_state["radio_action"] == "update" and st.session_state["radio_action_on_regards"] == "Class Teacher Allocation":      
            for field_name in class_teacher_allocation_update:
                st.session_state[field_name] = st.text_input(field_name.capitalize())
            
            msg_parts = [f"{field_name}:{st.session_state[field_name]}" for field_name in class_teacher_allocation_update
                         if st.session_state.get(field_name, "").strip() != ""]
            
        elif st.session_state["radio_action"] == "delete" and st.session_state["radio_action_on_regards"] == "Class Teacher Allocation":      
            for field_name in audit_table_delete:
                st.session_state[field_name] = st.text_input(field_name.capitalize())
            
            msg_parts = [f"{field_name}:{st.session_state[field_name]}" for field_name in audit_table_delete
                         if st.session_state.get(field_name, "").strip() != ""]

        st.session_state['usermessage'] = f"{st.session_state["radio_action"]}{" "} {""}{st.session_state["radio_action_on_regards"]}{""} details as follows: {msg_parts}"

        st.markdown(st.session_state['usermessage'])
        