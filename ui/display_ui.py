import streamlit as st
import requests
import time
from session_util import initialize_session_state

initialize_session_state()
API = "http://127.0.0.1:8000"  # Adjust to your FastAPI endpoint

def displayui():
    try:
                role_logged = st.session_state['roleendpointsrole']
                on_regard = st.session_state["radio_action_on_regards"].lower().replace(" ", "_")
                res =""
                if st.session_state['mode'] == "bulk mark posting" or "bulk info and allocations":
                    payload = {"records": st.session_state['records']}
                    res = requests.post(f"{API}/{on_regard}/upload", json = payload)
                else :
                    payload = {
                        "session_id": st.session_state["session_id"],
                        "message": st.session_state['usermessage'],
                        "role" : st.session_state['roleendpointsrole'],
                        "radio_action_on_person" : st.session_state["radio_action_on_regards"]
                    }
                    st.markdown(st.session_state['mode'])
                    res = requests.post(f"{API}/chat/", params= payload)  
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
                

