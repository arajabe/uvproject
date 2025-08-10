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
                endpoint = st.session_state.roleendpointsrole
                res = requests.post(
                    f"{API}/chat/{endpoint}",
                    params={
                        "session_id": st.session_state["session_id"],
                        "message": st.session_state.usermessage
                    }
                )
                data = res.json()
                if res.status_code == 200:
                    st.success("Message sent successfully.")
                    st.markdown(f"**Bot:** {data.get('reply', '(No reply found)')}")
                    st.session_state["reset_flag"] = True
                    st.session_state['mode'] = 'None'

                    if st.button("Reset" , key = "reset on sucess"):
                        for key in ["id", "name", "email","send"]:
                            st.session_state[key] = ""
                        st.session_state["action"] = "how can i help you"    
                        st.rerun()

                    with st.spinner("🔄 Resetting form in 3 seconds..."):
                        time.sleep(60)
                    # Reset session state and restart from beginning
                    
                    if st.session_state["reset_flag"]:
                        st.session_state["action"] = "how can i help you"
                        st.session_state.chat_history = []
                        st.rerun()                
                else:
                    st.error(f"Failed with status code: {res.status_code}")
                    
    except Exception as e:
                st.error(f"Error: {e}")
                

