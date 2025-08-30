import streamlit as st
from core.model.schema import UserCreate, UserUpdate, ParentCreate, OfficeStaffCreate, OfficeStaffUpdate, ParentUpdate, UserDelete, StudentCreate, StudentUpdate, TeacherCreate, TeacherUpdate
from ui.session import initialize_session_state

initialize_session_state()

def inforelated():
        
        col1, col2, col3 = st.columns(3)  # example: 2 columns

        with col1:
            st.session_state["radio_action"] = st.columns(1)[0].radio(
                "Choose action",
                ["create", "update", "delete", "view"],
                horizontal=True
            )
        
        if st.session_state["radio_action"] in ["create", "update", "delete", "view"]:
            with col2:
                st.session_state["radio_action_on_regards"] = st.radio(
                "Choose person",
                ["student", "parent", "teacher", "office staff"], horizontal=True)
        
        student_fields = ["id","name","fathername","mothername","dateofbirth","address","city","pincode","contactnumber",
                            "email", "aadhar","reason","parentid","parentrelation"]
        parent_fields = ["id","fathername","mothername","dateofbirth","address","city","pincode","contactnumber",
                            "email", "aadhar","reason","parentrelation", "occupation"]
        teacher_fields = ["id","fathername","mothername","dateofbirth","address","city","pincode","contactnumber",
                            "email", "aadhar","reason","subject", "graduatedegree"]
        radio_selected = ""
        
        def selected_person (value):
            match value:
                case "student": 
                    with col3:
                        st.session_state["table"] = "student"
                        radio_selected = st.radio("select fields", ["all","select fields"])
                        if radio_selected is not "all":
                            st.session_state["multiselect"] = st.multiselect(
                                "Select required fields:", student_fields)
                            
                case "parent": 
                    with col3:
                        st.session_state["table"] = "parent"
                        radio_selected = st.radio("select fields", ["all","selected fields"])
                        if radio_selected is not "all":
                            st.session_state["multiselect"] = st.multiselect(
                                "Select required fields:", parent_fields)
                            
                case "teacher": 
                    with col3:
                        st.session_state["table"] = "teacher"
                        radio_selected = st.radio("select fields", ["all","selected fields"])
                        if radio_selected is not "all":
                            st.session_state["multiselect"] = st.multiselect(
                                "Select rquired fields:", teacher_fields)
                            
                case "office staff": 
                    with col3:
                        st.session_state["table"] = "officestaff"
                        radio_selected = st.radio("select fields", ["all","selected fields"])
                        if radio_selected is not "all":
                            st.session_state["multiselect"] = st.multiselect(
                                "Select required fields:", teacher_fields)                        

    
        if st.session_state["radio_action"] in ["view"]:
            selected_person(st.session_state["radio_action_on_regards"])
            if radio_selected is "all":
                st.session_state["selected_field"] = "*"
            else:
                st.session_state["selected_field"] = st.session_state["multiselect"]

        not_required_words =  ["create", "update", "delete", "change", "transfer", "password", "alter", "drop","add", "addition", "deletion"]

        

        msg_parts = ""
        
        parent_create = ParentCreate.__annotations__
        parent_update = ParentUpdate.__annotations__
        student_create = StudentCreate.__annotations__
        student_update = StudentUpdate.__annotations__
        teacher_create = UserCreate.__annotations__ | TeacherCreate.__annotations__
        teacher_update = UserUpdate.__annotations__ | TeacherUpdate.__annotations__
        officestaff_create = UserCreate.__annotations__ | OfficeStaffCreate.__annotations__
        officestaff_update = UserUpdate.__annotations__ | OfficeStaffUpdate.__annotations__

        userdelete = UserDelete.__annotations__

        if st.session_state["radio_action"] == "create" and st.session_state["radio_action_on_regards"] == "parent":      
            for field_name in parent_create:
                st.session_state[field_name] = st.text_input(field_name.capitalize())
            
            msg_parts = [f"{field_name}:{st.session_state[field_name]}" for field_name in parent_create]            

        elif st.session_state["radio_action"] == "update" and st.session_state["radio_action_on_regards"] == "parent":      
            for field_name in parent_update:
                st.session_state[field_name] = st.text_input(field_name.capitalize(), "")
            msg_parts = [f"{field_name} is {st.session_state[field_name]}" for field_name in parent_update 
                         if st.session_state.get(field_name, "").strip() != ""]
        
        elif st.session_state["radio_action"] == "create" and st.session_state["radio_action_on_regards"] == "student":
            for field_name in student_create:
                st.session_state[field_name] = st.text_input(field_name.capitalize(), "")
            msg_parts = [f"{field_name} is {st.session_state[field_name]}" for field_name in student_create
                         if st.session_state.get(field_name, "").strip() != ""]
            
        elif st.session_state["radio_action"] == "update" and st.session_state["radio_action_on_regards"] == "student":
            for field_name in student_update:
                st.session_state[field_name] = st.text_input(field_name.capitalize(), "")
            msg_parts = [f"{field_name} is {st.session_state[field_name]}" for field_name in student_update
                         if st.session_state.get(field_name, "").strip() != ""]
            
        elif st.session_state["radio_action"] == "create" and st.session_state["radio_action_on_regards"] == "teacher":
            for field_name in teacher_create:
                st.session_state[field_name] = st.text_input(field_name.capitalize(), "")
            msg_parts = [f"{field_name} is {st.session_state[field_name]}" for field_name in teacher_create
                         if st.session_state.get(field_name, "").strip() != ""]
            
        elif st.session_state["radio_action"] == "update" and st.session_state["radio_action_on_regards"] == "teacher":
            for field_name in teacher_update:
                st.session_state[field_name] = st.text_input(field_name.capitalize(), "")
            msg_parts = [f"{field_name} is {st.session_state[field_name]}" for field_name in teacher_update
                         if st.session_state.get(field_name, "").strip() != ""]
            
        elif st.session_state["radio_action"] == "create" and st.session_state["radio_action_on_regards"] == "office staff":
            for field_name in officestaff_create:
                st.session_state[field_name] = st.text_input(field_name.capitalize(), "")
            msg_parts = [f"{field_name} is {st.session_state[field_name]}" for field_name in officestaff_create
                         if st.session_state.get(field_name, "").strip() != ""]
            
        elif st.session_state["radio_action"] == "update" and st.session_state["radio_action_on_regards"] == "office staff":
            for field_name in officestaff_update:
                st.session_state[field_name] = st.text_input(field_name.capitalize(), "")
            msg_parts = [f"{field_name} is {st.session_state[field_name]}" for field_name in officestaff_update
                         if st.session_state.get(field_name, "").strip() != ""]


        elif st.session_state["radio_action"] == "delete" and st.session_state["radio_action_on_regards"] != "none":
            for field_name in userdelete:
                st.session_state[field_name] = st.text_input(field_name.capitalize())
            msg_parts = [f"{field_name}:{st.session_state[field_name]}" for field_name in userdelete]

        if (st.session_state["radio_action"] in ["create", "update", "delete"]):
            st.session_state['usermessage'] = f"{st.session_state['radio_action']} {st.session_state['radio_action_on_regards']} details as follows: {msg_parts}"
        if st.session_state["radio_action"] in ["view"]:
            st.session_state["radio_action_on_regards"] = "information"
            user_message = f"{st.text_input('Enter ID as example student STUD0001 and all or select fields', '')}"
            if any(word in user_message.lower() for word in not_required_words):
                st.session_state['usermessage'] = ""
            else:
                st.session_state['usermessage'] = f"select {st.session_state['selected_field']} from table {st.session_state['table']} where {user_message}"

        

        