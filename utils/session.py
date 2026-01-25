
import streamlit as st
from utils.constants import AppConstants

def init_session_state(selected_bucket):
    """
    Initializes and manages the session state for path navigation.
    Resets the current path to root if the selected bucket changes.
    """
    # Initialize session state for path navigation
    if AppConstants.SESSION_CURRENT_PATH not in st.session_state:
        st.session_state[AppConstants.SESSION_CURRENT_PATH] = AppConstants.EMPTY_STRING

    # Initialize last bucket if not present
    if AppConstants.SESSION_LAST_BUCKET not in st.session_state:
        st.session_state[AppConstants.SESSION_LAST_BUCKET] = selected_bucket

    # Reset path if bucket changes
    if st.session_state[AppConstants.SESSION_LAST_BUCKET] != selected_bucket:
        st.session_state[AppConstants.SESSION_CURRENT_PATH] = AppConstants.EMPTY_STRING
        st.session_state[AppConstants.SESSION_LAST_BUCKET] = selected_bucket
