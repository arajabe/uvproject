import uuid
import streamlit as st
from typing import get_type_hints
from core.model.schema import (
    AssignementCreate, AssignementUpdate, AssignementDelete,
    SubjectTermSplitCreate,SubjectTermSplitDelete,
    MarkCreate, MarkUpdate, MarkDelete,
    ParentCreate, ParentUpdate,
    UserCreate, UserUpdate, UserDelete,
    OfficeStaffCreate, OfficeStaffUpdate,
    StudentCreate, StudentUpdate,
    TeacherCreate, TeacherUpdate,
    ClassTeacherAllocation, StudentClassAllocation
)

def initialize_session_state():

    if "logged_in" not in st.session_state:
        st.session_state['logged_in'] = False
    if "username" not in st.session_state:
        st.session_state['username'] = ""
    if "role" not in st.session_state:
        st.session_state['logedin_role'] = "None"
    if "session_id" not in st.session_state:
        st.session_state['session_id'] = str(uuid.uuid4())
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "mode" not in st.session_state:
        st.session_state["mode"] = "None"
    if "reset_flag" not in st.session_state:
        st.session_state["reset_flag"] = False
    if "action" not in st.session_state:
        st.session_state["action"] = "Your request Details. Kindly chek and confirm"    
    
    for field_name in UserCreate.__annotations__:
        if field_name not in st.session_state:
            st.session_state[field_name] = ""    
    for field_name in UserUpdate.__annotations__:
        if field_name not in st.session_state:
            st.session_state[field_name] = "" 
    for field_name in UserDelete.__annotations__:
        if field_name not in st.session_state:
            st.session_state[field_name] = "" 

    for field_name in ParentCreate.__annotations__:
        if field_name not in st.session_state:
            st.session_state[field_name] = ""    
    for field_name in ParentUpdate.__annotations__:
        if field_name not in st.session_state:
            st.session_state[field_name] = "" 
    for field_name in StudentCreate.__annotations__:
        if field_name not in st.session_state:
            st.session_state[field_name] = ""
    for field_name in StudentUpdate.__annotations__:
        if field_name not in st.session_state:
            st.session_state[field_name] = ""
    for field_name in TeacherCreate.__annotations__:
        if field_name not in st.session_state:
            st.session_state[field_name] = "" 
    for field_name in TeacherUpdate.__annotations__:
        if field_name not in st.session_state:
            st.session_state[field_name] = ""
    for field_name in OfficeStaffCreate.__annotations__:
        if field_name not in st.session_state:
            st.session_state[field_name] = "" 
    for field_name in OfficeStaffUpdate.__annotations__:
        if field_name not in st.session_state:
            st.session_state[field_name] = ""
    for field_name in MarkCreate.__annotations__:
        if field_name not in st.session_state:
            st.session_state[field_name] = ""
    for field_name in MarkUpdate.__annotations__:
        if field_name not in st.session_state:
            st.session_state[field_name] = ""
    for field_name in MarkDelete.__annotations__:
        if field_name not in st.session_state:
            st.session_state[field_name] = ""
    for field_name in AssignementCreate.__annotations__:
        if field_name not in st.session_state:
            st.session_state[field_name] = ""
    for field_name in AssignementUpdate.__annotations__:
        if field_name not in st.session_state:
            st.session_state[field_name] = ""
    for field_name in AssignementDelete.__annotations__:
        if field_name not in st.session_state:
            st.session_state[field_name] = ""
    for field_name in SubjectTermSplitCreate.__annotations__:
        if field_name not in st.session_state:
            st.session_state[field_name] = ""
    for field_name in SubjectTermSplitDelete.__annotations__:
        if field_name not in st.session_state:
            st.session_state[field_name] = ""
    for field_name in StudentClassAllocation.__annotations__:
        if field_name not in st.session_state:
            st.session_state[field_name] = ""
    for field_name in ClassTeacherAllocation.__annotations__:
        if field_name not in st.session_state:
            st.session_state[field_name] = ""


    if "msg" not in st.session_state:
        st.session_state.msg = "Kindly enter your request"

    if "usermessage" not in st.session_state:
        st.session_state['usermessage'] = ""
    if "roleendpointsrole" not in st.session_state:
        st.session_state["roleendpointsrole"] = ""
    if "radio_action" not in st.session_state:
        st.session_state["radio_action"] = ""   
    if "radio_action_on_person" not in st.session_state:
        st.session_state['radio_action_on_person']="none"
    if "CONFIRM" not in st.session_state:
        st.session_state['CONFIRM'] = ""
    if "radio_action_on_performance" not in st.session_state:
        st.session_state["radio_action_on_performance"] = ""