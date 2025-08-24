import streamlit as st
from core.model.schema import ( StudentClassAllocationCreate, StudentClassAllocationUpdate, AuditDelete)
from session_util import initialize_session_state

initialize_session_state()

def student_class_allocation():
        
        col1, col2, col3 = st.columns(3)  # example: 2 columns

        with col1:
            st.session_state["radio_action"] = st.columns(1)[0].radio(
                "Choose action",
                ["create", "update", "delete", "view"],
                horizontal=True
            )
        
        if st.session_state["radio_action"] in ["create", "update", "delete"]:
            with col2:
                st.session_state["radio_action_on_regards"] = st.radio(
                "Choose the  any one option",
                ["Student Class Allocation"],
                horizontal=True
            )
        elif st.session_state["radio_action"] in ["view"]:
            with col3:
                radio_selected = st.radio("select all fields", ["all","selected fields"])
                if radio_selected is not "all":
                    st.session_state["multiselect"] = st.multiselect(
                    "Select fields:", ["id", "student_class", "class_section", "count"])

        selected = st.session_state["selected_field"]
        if st.session_state["radio_action"] in ["view"]:
            if radio_selected is "all":
                st.session_state["selected_field"] = "*"
            else:
                st.session_state["selected_field"] = st.session_state["multiselect"]

        not_required_words =  ["create", "update", "delete", "change", "transfer", "password", "alter", "drop","add","password"]
                
        if (st.session_state["radio_action"] == "none"):
            st.session_state["action"] = st.text_input("What is your request?", st.session_state["action"])
            st.session_state["action"] = st.session_state["action"].lower()
        
        msg_parts = ""

        student_class_allocation_create = StudentClassAllocationCreate.__annotations__
        student_class_allocation_update = StudentClassAllocationUpdate.__annotations__
        audit_table_delete = AuditDelete.__annotations__

        if st.session_state["radio_action"] == "create" and st.session_state["radio_action_on_regards"] == "Student Class Allocation":      
            for field_name in student_class_allocation_create:
                st.session_state[field_name] = st.text_input(field_name.capitalize())
            
            msg_parts = [f"{field_name}:{st.session_state[field_name]}" for field_name in student_class_allocation_create
                         if st.session_state.get(field_name, "").strip() != ""]
        elif st.session_state["radio_action"] == "update" and st.session_state["radio_action_on_regards"] == "Student Class Allocation":      
            for field_name in student_class_allocation_update:
                st.session_state[field_name] = st.text_input(field_name.capitalize())
            
            msg_parts = [f"{field_name}:{st.session_state[field_name]}" for field_name in student_class_allocation_update
                         if st.session_state.get(field_name, "").strip() != ""]
            
        elif st.session_state["radio_action"] == "delete" and st.session_state["radio_action_on_regards"] == "Student Class Allocation":      
            for field_name in audit_table_delete:
                st.session_state[field_name] = st.text_input(field_name.capitalize())
            
            msg_parts = [f"{field_name}:{st.session_state[field_name]}" for field_name in audit_table_delete
                         if st.session_state.get(field_name, "").strip() != ""]
            
        if st.session_state["radio_action"] in ["create", "update", "delete"]:
            st.session_state['usermessage'] = f"{st.session_state["radio_action"]}{" "} {""}{st.session_state["radio_action_on_regards"]}{""} details as follows: {msg_parts}"
            st.markdown(st.session_state['usermessage'])
        if st.session_state["radio_action"] in ["view"]:
            st.session_state["radio_action_on_regards"] = "information"
            user_message = f"{st.text_input("what is you question?", "")}"
            if any(word in user_message.lower() for word in not_required_words):
                st.session_state['usermessage'] = ""
                st.markdown(st.session_state['usermessage'])
            else:
                st.session_state['usermessage'] = f"select {st.session_state["selected_field"]} from studentclassallocation where {user_message}"
                st.markdown(st.session_state['usermessage'])