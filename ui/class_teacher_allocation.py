import streamlit as st
from core.model.schema import ( MarkCreate, MarkDelete,
                               AssignementCreate, AssignementUpdate, AssignementDelete, 
                               SubjectTermSplitCreate, SubjectTermSplitDelete)
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
                st.session_state["radio_action_on_class_teacher"] = st.radio(
                "Choose the  any one option",
                ["none", "Class Teacher Allocation"],
                horizontal=True
            )
                
        if (st.session_state["radio_action"] == "none"):
            st.session_state["action"] = st.text_input("What is your request?", st.session_state["action"])
            st.session_state["action"] = st.session_state["action"].lower()
        
        msg_parts = ""

        if st.session_state["radio_action"] == "create" and st.session_state["radio_action_on_class_teacher"] == "Class Teacher Allocation":      
            for field_name in mark_create:
                st.session_state[field_name] = st.text_input(field_name.capitalize())
            
            msg_parts = [f"{field_name}:{st.session_state[field_name]}" for field_name in mark_create
                         if st.session_state.get(field_name, "").strip() != ""]

        st.session_state['usermessage'] = f"{st.session_state["radio_action"]}{" "} {""}{st.session_state["radio_action_on_performance"]}{""} details as follows: {msg_parts}"

        st.markdown(st.session_state['usermessage'])
        