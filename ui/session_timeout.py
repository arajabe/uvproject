import time
import streamlit as st
import requests
from config import API_URL

SESSION_TIMEOUT = 1800  # 30 minutes

def show_session_timer():
    if "last_active" not in st.session_state:
        st.session_state.last_active = time.time()

    elapsed = time.time() - st.session_state.last_active
    remaining = SESSION_TIMEOUT - int(elapsed)

    if remaining <= 0:
        remaining = 0

    mins, secs = divmod(remaining, 60)
    st.markdown(
        f"⏳ **Session time left:** {mins:02d}:{secs:02d}",
        unsafe_allow_html=True,
    )

    return remaining


def check_session_timeout():
    remaining = show_session_timer()

    if remaining <= 0:
        if "logout_confirmed" not in st.session_state:
            st.session_state.logout_confirmed = False

        if not st.session_state.logout_confirmed:
            st.warning("⚠️ Your session has expired. Do you want to log out?")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Log me out"):
                    res = requests.post(f"{API_URL}/login/logout", params={
                        "username": st.session_state.get("username", "")
                    })
                    if res.status_code == 200:
                        st.session_state.clear()
                        st.session_state.logout_confirmed = True
                        st.rerun()
            with col2:
                if st.button("Keep me signed in"):
                    st.session_state.last_active = time.time()
                    st.success("✅ Session extended.")
                    st.rerun()
            st.stop()

    else:
        # update "last_active" only when user interacts
        st.session_state.last_active = time.time()