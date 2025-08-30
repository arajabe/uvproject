import streamlit as st
from ui.login_ui import login_screen
from ui.session import initialize_session_state
from ui.session_timeout import check_session_timeout
from ui.dashboard_ui import dashboard

initialize_session_state()
check_session_timeout()

if not st.session_state.logged_in:
    login_screen()
else:
    dashboard()
