
import streamlit as st
from utils.constants import AppConstants
from utils.bucket import get_keys, format_size, create_folder, delete_folder
from config import ACCESS_KEY_ID, SECRET_ACCESS_KEY, ENDPOINT_URL

def render_file_explorer(s3_client, selected_bucket, current_path, expiration_seconds, region):
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
            # Folder List Header (Optional, or just list them)
            # To look like "list form", we'll use columns similar to files but simplified
            
            for folder in folders:
                 # Use same column metrics for alignment
                 # c0: Spacer/Select, c1: Name, c2: Size, c3: Modified, c4: Action
                 row_c0, row_c1, row_c2, row_c3, row_c4 = st.columns([0.5, 4, 1, 2, 1], vertical_alignment="center")
                 
                 # c0: Folder Icon/Spacer
                 with row_c0:
                     st.write("📁") # Just visual indication

                 # c1: Folder Name (Clickable)
                 with row_c1:
                     if st.button(f"{folder}", key=f"{AppConstants.FOLDER_KEY_PREFIX}{folder}"):
                        st.session_state[AppConstants.SESSION_CURRENT_PATH] += f"{folder}/"
                        st.rerun()

                 # c2, c3: Empty for folders
                 row_c2.write("-")
                 row_c3.write("-")

                 # c4: Delete Action
                 with row_c4:
                        if st.button("🗑️", key=f"del_folder_{folder}", help=f"Delete folder: {folder}"):
                            st.session_state[f"confirm_delete_{folder}"] = True
                            st.rerun()
                 
                 # Confirmation Logic (keep outside valid columns context or handle cleanly)
                 if st.session_state.get(f"confirm_delete_{folder}", False):
                         st.warning(f"Delete '{folder}' and all its contents?")
                         c_d1, c_d2 = st.columns(2)
                         if c_d1.button("Yes", key=f"yes_del_{folder}"):
                             try:
                                 folder_key = f"{current_path}{folder}/"
                                 delete_folder(
                                     bucket_name=selected_bucket,
                                     folder_path=folder_key,
                                     access_key=ACCESS_KEY_ID,
                                     secret_key=SECRET_ACCESS_KEY,
                                     region_name=region,
                                     endpoint_url=ENDPOINT_URL
                                 )
                                 st.success(f"Deleted {folder}")
                                 del st.session_state[f"confirm_delete_{folder}"]
                                 st.rerun()
                             except Exception as e:
                                 st.error(f"Error: {e}")
                         if c_d2.button("No", key=f"no_del_{folder}"):
                             del st.session_state[f"confirm_delete_{folder}"]
                             st.rerun()


        # Display Files
        if files_list:
            st.write(AppConstants.FILES_SUBHEADER)
            
            # Files Header & List
            # Header
            c0, c1, c2, c3, c4 = st.columns([0.5, 4, 1, 2, 1], vertical_alignment="center")
            
            # Select All Logic
            def toggle_all():
                new_state = st.session_state.get("select_all", False)
                for f in files_list:
                    st.session_state[f"select_{f['Key']}"] = new_state

            c0.checkbox("Select All", key="select_all", on_change=toggle_all, label_visibility="collapsed")
            
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
            if st.button(AppConstants.BUTTON_DELETE_SELECTED):
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
