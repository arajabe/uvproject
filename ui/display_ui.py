import streamlit as st
import uuid
import requests
import time
from typing import TypedDict, List, Optional,Annotated
import os, json, requests
from pydantic import BaseModel, EmailStr,constr, StringConstraints
import pandas
from datetime import date
from core.model.schema import UserCreate, UserUpdate
from session_util import initialize_session_state
from ui.sidebar_ui import sidebar
from ui.performance_ui import performance
from ui.inforelated_ui import inforelated

initialize_session_state()
API = "http://127.0.0.1:8000"  # Adjust to your FastAPI endpoint

def displayui():
    try:
                role_logged = st.session_state['roleendpointsrole']

                if role_logged == "admin":
                      Payload = {
                        "session_id": st.session_state["session_id"],
                        "message": st.session_state['usermessage'],
                        "role" : st.session_state['roleendpointsrole'],
                        "radio_action_on_person" : st.session_state["radio_action_on_person"]
                    }
                elif role_logged == "teacher":
                       Payload = {
                        "session_id": st.session_state["session_id"],
                        "message": st.session_state['usermessage'],
                        "role" : st.session_state['roleendpointsrole'],
                        "radio_action_on_person" : st.session_state["radio_action_on_performance"]
                    }


                res = requests.post(f"{API}/chat/", params= Payload)
                data = res.json()
                if res.status_code == 200:
                    st.success("Message sent successfully.")
                    st.markdown(f"**Bot:** {data.get('reply', '(No reply found)')}")
                    st.table(data.get('reply', '(No reply found)'))
                    st.session_state["reset_flag"] = True
                    st.session_state['mode'] = 'None'

                    if st.button("Reset" , key = "reset on sucess"):                           
                        st.rerun()
                        st.session_state['usermessage'] = "how can i help you" 

                    # Reset session state and restart from beginning
                    with st.spinner():
                          st.session_state['usermessage'] = "how can i help you" 
                          time.sleep(30)                          

                    st.session_state['usermessage'] = "how can i help you"          
                else:
                    st.error(f"Failed with status code: {res.status_code}")
                    
    except Exception as e:
                st.error(f"Error: {e}")
                

