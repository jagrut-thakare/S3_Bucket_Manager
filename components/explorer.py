
import streamlit as st
from utils.constants import AppConstants
from utils.bucket import get_keys, format_size

def render_file_explorer(s3_client, selected_bucket, current_path, expiration_seconds):
    """
    Renders the file explorer (folders and files).
    """
    try:
        # Fetch items for the current path
        folders, files_list = get_keys(s3_client, selected_bucket, current_path)
        
        if not folders and not files_list:
            st.info(AppConstants.DIR_EMPTY_INFO)
        
        # Display Folders
        if folders:
            st.write(AppConstants.FOLDERS_SUBHEADER)
            cols = st.columns(4) # Grid layout
            for i, folder in enumerate(folders):
                # Use columns to create a grid of folders
                with cols[i % 4]:
                    if st.button(f"{AppConstants.FOLDER_ICON_PREFIX}{folder}", key=f"{AppConstants.FOLDER_KEY_PREFIX}{folder}"):
                        st.session_state[AppConstants.SESSION_CURRENT_PATH] += f"{folder}/"
                        st.rerun()

        # Display Files
        if files_list:
            st.write(AppConstants.FILES_SUBHEADER)
            
            with st.form("files_form", clear_on_submit=False):
                # Header
                c0, c1, c2, c3, c4 = st.columns([0.5, 4, 1, 2, 1], vertical_alignment="center")
                c0.markdown(AppConstants.TABLE_HEADER_SELECT)
                c1.markdown(AppConstants.TABLE_HEADER_NAME)
                c2.markdown(AppConstants.TABLE_HEADER_SIZE)
                c3.markdown(AppConstants.TABLE_HEADER_MODIFIED)
                c4.markdown(AppConstants.TABLE_HEADER_ACTION)
                
                selected_keys = []
                
                for file_data in files_list:
                    row_c0, row_c1, row_c2, row_c3, row_c4 = st.columns([0.5, 4, 1, 2, 1], vertical_alignment="center")
                    
                    # Checkbox
                    with row_c0:
                        if st.checkbox(AppConstants.CHECKBOX_LABEL, key=f"select_{file_data['Key']}", label_visibility="collapsed"):
                            selected_keys.append(file_data['Key'])
                    
                    # Icon + Name
                    row_c1.write(f"{AppConstants.FILE_ICON_PREFIX}{file_data['Name']}")
                    
                    # Size
                    row_c2.write(format_size(file_data['Size']))
                    
                    # Time
                    row_c3.write(file_data['LastModified'].strftime(AppConstants.DATE_FORMAT))
                    
                    # Download Button (Generate Presigned URL)
                    with row_c4:
                        try:
                            # Use configured expiration time
                            url = s3_client.generate_presigned_url(
                                AppConstants.S3_GET_OBJECT,
                                Params={
                                    AppConstants.PRESIGNED_BUCKET: selected_bucket, 
                                    AppConstants.PRESIGNED_KEY: file_data['Key']
                                },
                                ExpiresIn=expiration_seconds
                            )
                            # Using HTML link styled as text/button for standard download
                            st.markdown(AppConstants.DOWNLOAD_LINK_TEXT.format(url=url), unsafe_allow_html=True)
                        except Exception as e:
                            st.error(AppConstants.DOWNLOAD_ERROR_MSG)
                
                st.divider()
                if st.form_submit_button(AppConstants.BUTTON_DELETE_SELECTED):
                    if selected_keys:
                        try:
                            with st.spinner(AppConstants.DELETE_SPINNER_PREFIX):
                                # Iterate and delete files one by one to avoid Missing Content-MD5 header issue
                                for k in selected_keys:
                                    s3_client.delete_object(Bucket=selected_bucket, Key=k)
                            
                            st.success(AppConstants.DELETE_SUCCESS_MSG.format(count=len(selected_keys)))
                            st.rerun()
                        except Exception as e:
                            st.error(f"{AppConstants.DELETE_ERROR_MSG}{e}")
                    else:
                        st.warning(AppConstants.NO_FILES_SELECTED_MSG)
                        
    except Exception as e:
        st.error(f"{AppConstants.ERROR_LISTING_CONTENTS}{e}")
