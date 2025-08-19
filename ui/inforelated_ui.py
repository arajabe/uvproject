import streamlit as st
import uuid
import requests
import time
from typing import TypedDict, List, Optional,Annotated
import os, json, requests
from pydantic import BaseModel, EmailStr,constr, StringConstraints
import pandas
from datetime import date
from core.model.schema import UserCreate, UserUpdate, ParentCreate, OfficeStaffCreate, OfficeStaffUpdate, ParentUpdate, UserDelete, StudentCreate, StudentUpdate, TeacherCreate, TeacherUpdate
from session_util import initialize_session_state

initialize_session_state()
API = "http://127.0.0.1:8000"  # Adjust to your FastAPI endpoint,

def inforelated():
        
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
                "Choose person",
                ["none","student", "parent", "teacher", "office staff"],
                horizontal=True
            )


        if (st.session_state["radio_action"] == "none" and st.session_state["radio_action_on_regards"] == "none"):
            st.session_state["action"] = st.text_input("What is your request?", st.session_state["action"])
            st.session_state["action"] = st.session_state["action"].lower()

        

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
        
        st.session_state['usermessage'] = f"{st.session_state["radio_action"]}{" "}{st.session_state["radio_action_on_regards"]} details as follows: {msg_parts}"

        st.markdown(st.session_state['usermessage'])    
        

        