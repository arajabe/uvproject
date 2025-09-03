import streamlit as st
import requests
from ui.session import initialize_session_state
from config import API_URL
import time 

initialize_session_state()

def performance():

    role = st.session_state['logedin_role']
    payload = {}

    def is_operation_allowed(msg, role):
        if role in ["admin", "teacher"]:
            return True
        if any(word in msg.lower() for word in ["create", "update", "delete","password","adition", "modification", "deletion"]):
            return False
        return True
    col1, col2, col3, col4,col5 = st.columns(5)

    # Step 1: Exam selection
    with col1:
        st.session_state["exam"] = st.radio(
            "Exams",
            ["Termmark", "Assignement", "Split Term Mark", "any question"],
            horizontal=True
        )

    # Step 2: If exam is in the defined list
    if st.session_state["exam"] in ["Termmark", "Assignement", "Split Term Mark"]:      

        rodio_bt = ""

        # Only for admin/teacher → choose overall/individual
        if role in ["admin", "teacher"]:
            with col2:
                rodio_bt = st.radio("Select any one", ["overall", "individual"], horizontal= False)

        # Step 3: Action options
        with col3:
            if role in ["admin", "teacher"] and rodio_bt == "overall":
                st.session_state["radio_action"] = st.radio(
                    "Overall",
                    ["Overall_total", "Overall_subject", "Overall_trend", "Overall_rank", "Overall_strength_weaknes"],
                    horizontal=True
                )        
            else:
                # default for individual + student/parent
                st.session_state["radio_action"] = st.radio(
                    "Individual",
                    ["individual_total", "individual_subject", "individual_trend", "individual_rank", "individual_strength_weakness"],
                    horizontal=True
             )
        with col4:
             st.session_state["term"] = st.radio("Term", ["1", "2", "3"])
             
        payload = { "session_id": st.session_state["session_id"],
                "message": st.session_state.msg,
                "role" : role,
                "performance_request" : st.session_state["radio_action"],
                "exam" : st.session_state["exam"],
                "term" : st.session_state["term"],
                "status" : rodio_bt}        
        
        if st.session_state["exam"] in ["Assignement"]:
             with col5: 
                st.session_state["period"] = st.radio("Period", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
                payload["period"] = st.session_state["period"]
    # Step 4: If exam is not in the main list → free text input
    else:
        st.session_state.msg = st.text_input("Ask your question")    

    if rodio_bt == "overall":
        payload["username"] = st.session_state["username"]
    else:
        st.session_state["student_id"] = st.text_input("Enter Student_id", "")
        payload["username"] = st.session_state["username"]
        payload["student_id"] = st.session_state["student_id"]

    if not is_operation_allowed(st.session_state.msg, role):
            st.error(f"As a `{role}`, you are not allowed to perform this operation.")
    
    elif st.button("Get Performance"):
        if rodio_bt == "overall":
            try:
                res = requests.post(
                    f"{API_URL}/chat/performance", params = payload)
                data = res.json()
                if res.status_code == 422:
                    st.markdown("select all fields")
                elif res.status_code == 200:
                    st.markdown(data.get("reply", "(No reply found)"))
            except Exception as e:
                st.error(f"Error: {e}")
        elif rodio_bt == "individual":
            try:
                res = requests.post(
                    f"{API_URL}/chat/performance", params = payload)
                data = res.json()
                st.markdown(data.get("reply", "(No reply found)"))
            except Exception as e:
                st.error(f"Error: {e}")

