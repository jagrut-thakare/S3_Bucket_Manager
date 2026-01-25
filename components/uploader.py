
import streamlit as st
from utils.constants import AppConstants
from utils.bucket import upload_file_v2, create_folder
from config import ACCESS_KEY_ID, SECRET_ACCESS_KEY, ENDPOINT_URL

def render_upload_section(s3_client, selected_bucket, current_path, region):
    """
    Renders the file upload section.
    """
    st.subheader(AppConstants.UPLOAD_SUBHEADER)
    with st.expander(AppConstants.UPLOAD_EXPANDER_LABEL, expanded=False):
        with st.form("upload_form", clear_on_submit=True):
            uploaded_files = st.file_uploader(
                AppConstants.UPLOAD_FILE_LABEL, 
                accept_multiple_files=True,
                help="Drag & drop files here. To preserve folder structure, upload a .zip file and check the box below."
            )
            
            # Option to treat zip as folder
            extract_zip = st.checkbox("📂 Upload as Folder (Auto-extract .zip)", value=False)
            
            submit_upload = st.form_submit_button(AppConstants.UPLOAD_BUTTON_LABEL)
            
            if submit_upload and uploaded_files:
                try:
                    success_count = 0
                    with st.spinner(AppConstants.UPLOAD_SPINNER_PREFIX):
                        for uploaded_file in uploaded_files:
                            # Handle Zip files for folder structure ONLY if requested
                            if extract_zip and uploaded_file.name.lower().endswith(".zip"):
                                import zipfile
                                import io
                                try:
                                    with zipfile.ZipFile(uploaded_file) as z:
                                        for filename in z.namelist():
                                            # Skip directories
                                            if filename.endswith('/'):
                                                continue
                                                
                                            # Read file data
                                            with z.open(filename) as f:
                                                file_content = f.read()
                                                file_io = io.BytesIO(file_content)
                                                
                                                # Construct complete key (current path + zip internal path)
                                                # We don't include the zip filename itself in the path
                                                file_key = f"{current_path}{filename}"
                                                
                                                upload_file_v2(
                                                    file_obj=file_io,
                                                    bucket_name=selected_bucket,
                                                    object_key=file_key,
                                                    access_key=ACCESS_KEY_ID,
                                                    secret_key=SECRET_ACCESS_KEY,
                                                    endpoint_url=ENDPOINT_URL,
                                                    region_name=region
                                                )
                                                success_count += 1
                                except Exception as zip_err:
                                    st.error(f"Error extracting {uploaded_file.name}: {zip_err}")
                            else:
                                # Normal File Upload
                                # Construct key based on current path
                                file_key = f"{current_path}{uploaded_file.name}"
                                
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
                                success_count += 1
                        
                    st.success(f"{AppConstants.UPLOAD_SUCCESS_PREFIX}{success_count} files.")
                    st.rerun()
                except Exception as e:
                    st.error(f"{AppConstants.UPLOAD_FAILED_PREFIX}{e}")

def render_create_folder(selected_bucket, current_path, region):
    """
    Renders the create folder section.
    """
    st.subheader(AppConstants.CREATE_FOLDER_SUBHEADER) # Using standard header to match Upload
    # Actually user wants side by side.
    # We will use the expander as requested/implied by previous context, but maybe adjust header.
    # Let's stick to the form inside logic.
    
    with st.expander("Create Folder", expanded=False):
        with st.form("create_folder_form", clear_on_submit=True):
            new_folder_name = st.text_input(AppConstants.CREATE_FOLDER_LABEL)
            submitted = st.form_submit_button(AppConstants.CREATE_FOLDER_BUTTON)
            if submitted and new_folder_name:
                try:
                    folder_key = f"{current_path}{new_folder_name.strip()}/"
                    create_folder(
                        bucket_name=selected_bucket, 
                        folder_path=folder_key,
                        access_key=ACCESS_KEY_ID,
                        secret_key=SECRET_ACCESS_KEY,
                        endpoint_url=ENDPOINT_URL,
                        region_name=region
                    ) 
                    st.success(f"{AppConstants.CREATE_FOLDER_SUCCESS}{new_folder_name}")
                    st.rerun()
                except Exception as e:
                    st.error(f"{AppConstants.CREATE_FOLDER_ERROR}{e}")
