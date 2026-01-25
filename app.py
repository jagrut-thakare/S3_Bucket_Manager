import streamlit as st
from utils.constants import AppConstants
from components.sidebar import render_sidebar
from components.uploader import render_upload_section
from components.navigation import render_navigation
from components.explorer import render_file_explorer
from utils.session import init_session_state


def main():
    st.set_page_config(layout=AppConstants.PAGE_LAYOUT, page_title=AppConstants.PAGE_TITLE)

    st.title(AppConstants.PAGE_TITLE)

    # 1. Sidebar Configuration
    s3_client, selected_bucket, expiration_seconds, region = render_sidebar()

    # 2. Main App Logic
    # Initialize session state
    init_session_state(selected_bucket)

    if selected_bucket and s3_client:
        st.header(f"{AppConstants.HEADER_BUCKET_PREFIX}{selected_bucket}")
        
        # 3. Upload Section
        render_upload_section(s3_client, selected_bucket, st.session_state[AppConstants.SESSION_CURRENT_PATH], region)

        st.divider()

        # 4. Navigation
        render_navigation()

        # 5. File Explorer
        render_file_explorer(s3_client, selected_bucket, st.session_state[AppConstants.SESSION_CURRENT_PATH], expiration_seconds)

    else:
        st.info(AppConstants.INFO_SELECT_BUCKET)

if __name__ == "__main__":
    main()