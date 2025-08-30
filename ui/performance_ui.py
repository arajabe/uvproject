import streamlit as st
import requests
import requests
from ui.session import initialize_session_state
from config import API_URL

initialize_session_state()

def performance():

    role = st.session_state['logedin_role']

    def is_operation_allowed(msg, role):
        if role in ["admin", "teacher"]:
            return True
        if any(word in msg.lower() for word in ["create", "update", "delete","password","adition", "modification", "deletion"]):
            return False
        return True
    col1, col2, col3 = st.columns(3)

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

    # Step 4: If exam is not in the main list → free text input
    else:
        st.session_state.msg = st.text_input("Ask your question")

    if not is_operation_allowed(st.session_state.msg, role):
            st.error(f"As a `{role}`, you are not allowed to perform this operation.")

    elif st.button("Get Performance"):
            try:
                res = requests.post(
                    f"{API_URL}/chat/performance",
                    params={
                        "session_id": st.session_state["session_id"],
                        "message": st.session_state.msg,
                        "role" : role,
                        "performance_request" : st.session_state["radio_action"],
                        "exam" : st.session_state["exam"]
                    }
                )
                data = res.json()
                st.markdown(data.get("reply", "(No reply found)"))
            except Exception as e:
                st.error(f"Error: {e}")

