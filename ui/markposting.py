import streamlit as st
from core.model.schema import ( MarkCreate, MarkDelete,
                               AssignementCreate, AssignementUpdate, AssignementDelete, 
                               SubjectTermSplitCreate, SubjectTermSplitDelete)
from session_util import initialize_session_state

initialize_session_state()
API = "http://127.0.0.1:8000"  # Adjust to your FastAPI endpoint,

def markposting():
        
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
                ["none", "Assignement", "Subject Term Split", "Term Mark", "Quiz", "Other Activity"],
                horizontal=True
            )
                
        if (st.session_state["radio_action"] == "none"):
            st.session_state["action"] = st.text_input("What is your request?", st.session_state["action"])
            st.session_state["action"] = st.session_state["action"].lower()
        
        msg_parts = ""
        
        mark_create = MarkCreate.__annotations__ 
        mark_delete = MarkDelete.__annotations__
        assignement_create = AssignementCreate.__annotations__
        assignement_update = AssignementUpdate.__annotations__
        assignement_delete = AssignementDelete.__annotations__
        subject_term_split_create = SubjectTermSplitCreate.__annotations__
        subject_term_split_delete = SubjectTermSplitDelete.__annotations__

        if st.session_state["radio_action"] == "create" and st.session_state["radio_action_on_regards"] == "Term Mark":      
            for field_name in mark_create:
                st.session_state[field_name] = st.text_input(field_name.capitalize())
            
            msg_parts = [f"{field_name}:{st.session_state[field_name]}" for field_name in mark_create]
        
        elif st.session_state["radio_action"] == "update" and st.session_state["radio_action_on_regards"] == "Term Mark":      
            for field_name in mark_create:
                st.session_state[field_name] = st.text_input(field_name.capitalize())
            
            msg_parts = [f"{field_name}:{st.session_state[field_name]}" for field_name in mark_create
                         if st.session_state.get(field_name, "").strip() != ""]
            
        elif st.session_state["radio_action"] == "delete" and st.session_state["radio_action_on_regards"] == "Term Mark":      
            for field_name in mark_delete:
                st.session_state[field_name] = st.text_input(field_name.capitalize())
            
            msg_parts = [f"{field_name}:{st.session_state[field_name]}" for field_name in mark_delete
                         if st.session_state.get(field_name, "").strip() != ""]
            
        elif st.session_state["radio_action"] == "create" and st.session_state["radio_action_on_regards"] == "Assignement":      
            for field_name in assignement_create:
                st.session_state[field_name] = st.text_input(field_name.capitalize())
            
            msg_parts = [f"{field_name}:{st.session_state[field_name]}" for field_name in assignement_create]
        
        elif st.session_state["radio_action"] == "update" and st.session_state["radio_action_on_regards"] == "Assignement":      
            for field_name in assignement_update:
                st.session_state[field_name] = st.text_input(field_name.capitalize())
            
            msg_parts = [f"{field_name}:{st.session_state[field_name]}" for field_name in assignement_update
                         if st.session_state.get(field_name, "").strip() != ""]

        elif st.session_state["radio_action"] == "delete" and st.session_state["radio_action_on_regards"] == "Assignement":      
            for field_name in assignement_delete:
                st.session_state[field_name] = st.text_input(field_name.capitalize())
            
            msg_parts = [f"{field_name}:{st.session_state[field_name]}" for field_name in assignement_delete
                         if st.session_state.get(field_name, "").strip() != ""]
            
        elif st.session_state["radio_action"] == "create" and st.session_state["radio_action_on_regards"] == "Subject Term Split":      
            for field_name in subject_term_split_create:
                st.session_state[field_name] = st.text_input(field_name.capitalize())
            
            msg_parts = [f"{field_name}:{st.session_state[field_name]}" for field_name in subject_term_split_create]

        elif st.session_state["radio_action"] == "update" and st.session_state["radio_action_on_regards"] == "Subject Term Split":      
            for field_name in subject_term_split_create:
                st.session_state[field_name] = st.text_input(field_name.capitalize())
            
            msg_parts = [f"{field_name}:{st.session_state[field_name]}" for field_name in subject_term_split_create
                         if st.session_state.get(field_name, "").strip() != ""]
            
        elif st.session_state["radio_action"] == "delete" and st.session_state["radio_action_on_regards"] == "Subject Term Split":      
            for field_name in subject_term_split_delete:
                st.session_state[field_name] = st.text_input(field_name.capitalize())
            
            msg_parts = [f"{field_name}:{st.session_state[field_name]}" for field_name in subject_term_split_delete
                         if st.session_state.get(field_name, "").strip() != ""]
                
        st.session_state['usermessage'] = f"{st.session_state["radio_action"]}{" "} {""}{st.session_state["radio_action_on_regards"]}{""} details as follows: {msg_parts}"

        st.markdown(st.session_state['usermessage'])
        