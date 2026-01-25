
import streamlit as st
from utils.constants import AppConstants
from utils.bucket import upload_file_v2
from config import ACCESS_KEY_ID, SECRET_ACCESS_KEY, ENDPOINT_URL

def render_upload_section(s3_client, selected_bucket, current_path, region):
    """
    Renders the file upload section.
    """
    st.subheader(AppConstants.UPLOAD_SUBHEADER)
    with st.expander(AppConstants.UPLOAD_EXPANDER_LABEL, expanded=False):
        with st.form("upload_form", clear_on_submit=True):
            uploaded_file = st.file_uploader(AppConstants.UPLOAD_FILE_LABEL, accept_multiple_files=False)
            submit_upload = st.form_submit_button(AppConstants.UPLOAD_BUTTON_LABEL)
            
            if submit_upload and uploaded_file:
                try:
                    # Construct key based on current path
                    file_key = f"{current_path}{uploaded_file.name}"
                    
                    with st.spinner(f"{AppConstants.UPLOAD_SPINNER_PREFIX}{file_key}..."):
                        # Use the v2 uploader function
                        upload_file_v2(
                            file_obj=uploaded_file,
                            bucket_name=selected_bucket,
                            object_key=file_key,
                            access_key=ACCESS_KEY_ID,
                            secret_key=SECRET_ACCESS_KEY,
                            endpoint_url=ENDPOINT_URL,
                            region_name=region
                        )
                    st.success(f"{AppConstants.UPLOAD_SUCCESS_PREFIX}{file_key}")
                    st.rerun()
                except Exception as e:
                    st.error(f"{AppConstants.UPLOAD_FAILED_PREFIX}{e}")
