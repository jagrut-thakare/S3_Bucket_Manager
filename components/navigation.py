
import streamlit as st
from utils.constants import AppConstants

def render_navigation():
    """
    Renders the breadcrumbs and navigation buttons.
    Returns:
        str: The updated current path (though largely managed via session state inside)
    """
    col_nav1, col_nav2 = st.columns([5, 1])
    with col_nav1:
        if st.session_state[AppConstants.SESSION_CURRENT_PATH]:
            st.markdown(f"{AppConstants.NAV_CURRENT_PATH_PREFIX}`/{st.session_state[AppConstants.SESSION_CURRENT_PATH]}`")
            if st.button(AppConstants.NAV_BACK_BUTTON):
                # Go up one level
                parts = st.session_state[AppConstants.SESSION_CURRENT_PATH].strip(AppConstants.PATH_SEPARATOR).split(AppConstants.PATH_SEPARATOR)
                if len(parts) <= 1:
                    st.session_state[AppConstants.SESSION_CURRENT_PATH] = AppConstants.EMPTY_STRING
                else:
                    st.session_state[AppConstants.SESSION_CURRENT_PATH] = AppConstants.PATH_SEPARATOR.join(parts[:-1]) + AppConstants.PATH_SEPARATOR
                st.rerun()
        else:
            st.markdown(f"{AppConstants.NAV_CURRENT_PATH_PREFIX}{AppConstants.NAV_ROOT_LABEL}")
            
    with col_nav2:
         if st.button(AppConstants.NAV_HOME_BUTTON):
            st.session_state[AppConstants.SESSION_CURRENT_PATH] = AppConstants.EMPTY_STRING
            st.rerun()
