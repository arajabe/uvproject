import streamlit as st
from core.model.schema import ( MarkCreate, MarkDelete,
                               AssignementCreate, AssignementUpdate, AssignementDelete, 
                               SubjectTermSplitCreate, SubjectTermSplitDelete)
from session_util import initialize_session_state

initialize_session_state()

def markposting():
        
        col1, col2,col3 = st.columns(3)  # example: 2 columns

        with col1:
            st.session_state["radio_action"] = st.columns(1)[0].radio(
                "Choose action",
                ["none","create", "update", "delete", "view"],
                horizontal=True
            )
        
        if st.session_state["radio_action"] in ["create", "update", "delete","view"]:
            with col2:
                st.session_state["radio_action_on_regards"] = st.radio(
                "Choose the  any one option",
                ["Assignement", "Subject Term Split", "Term Mark", "Quiz", "Other Activity"],
                horizontal=True
            )
        
        assignement_fields = ["id","student_id","term","period","language_1",
                              "language_2","maths","science","social_science"]

        mark_fields = ["id","student_id","student_id","term","period","language_1",
                       "language_2","maths","science","social_science"]
        subject_term_split_fields = ["id","student_id","term","mark_section_A","mark_section_B","mark_section_C",
                                     "mark_section_D","subject_total","abscent"]
        radio_selected = ""
        
        def selected_person (value):
            match value:
                case "Assignement": 
                    with col3:
                        st.session_state["table"] = "assignement"
                        radio_selected = st.radio("select fields", ["all","select fields"])
                        if radio_selected is not "all":
                            st.session_state["multiselect"] = st.multiselect(
                                "Select required fields:", assignement_fields)
                            
                case "Subject Term Split": 
                    with col3:
                        st.session_state["table"] = "subject_term_split"
                        radio_selected = st.radio("select fields", ["all","selected fields"])
                        if radio_selected is not "all":
                            st.session_state["multiselect"] = st.multiselect(
                                "Select required fields:", subject_term_split_fields)
                            
                case "Term Mark": 
                    with col3:
                        st.session_state["table"] = "termmark"
                        radio_selected = st.radio("select fields", ["all","selected fields"])
                        if radio_selected is not "all":
                            st.session_state["multiselect"] = st.multiselect(
                                "Select rquired fields:", mark_fields)

    
        if st.session_state["radio_action"] in ["view"]:
            selected_person(st.session_state["radio_action_on_regards"])
            if radio_selected is "all":
                st.session_state["selected_field"] = "*"
            else:
                st.session_state["selected_field"] = st.session_state["multiselect"]

        not_required_words =  ["create", "update", "delete", "change", "transfer", "password", "alter", "drop","add", "addition", "deletion"]
        msg_parts = ""
        
                
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
            
        if st.session_state["radio_action"] in ["create", "update", "delete"]:                
            st.session_state['usermessage'] = f"{st.session_state["radio_action"]}{" "} {""}{st.session_state["radio_action_on_regards"]}{""} details as follows: {msg_parts}"

            st.markdown(st.session_state['usermessage'])

        elif st.session_state["radio_action"] in ["view"]:
            st.session_state["radio_action_on_regards"] = "information"
            user_message = f"{st.text_input("what is you question?", "")}"
            if any(word in user_message.lower() for word in not_required_words):
                st.session_state['usermessage'] = ""
                st.markdown(st.session_state['usermessage'])
            else:
                st.session_state['usermessage'] = f"select {st.session_state["selected_field"]} from table {st.session_state["table"]} where {user_message}"
                st.markdown(st.session_state['usermessage'])
        