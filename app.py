import streamlit as st
from utils.constants import AppConstants
from utils.bucket import upload_file_v2, get_s3_client, get_keys, format_size
from config import ACCESS_KEY_ID, SECRET_ACCESS_KEY, ENDPOINT_URL

st.set_page_config(layout=AppConstants.PAGE_LAYOUT, page_title=AppConstants.PAGE_TITLE)

st.title(AppConstants.PAGE_TITLE)

# --- Sidebar Configuration ---
st.sidebar.header(AppConstants.SIDEBAR_CONFIG_HEADER)

# Region Selection
region = st.sidebar.selectbox(AppConstants.SIDEBAR_REGION_LABEL, AppConstants.AVAILABLE_REGIONS)

# Expiration Selection
expiration_hours = st.sidebar.number_input(
    AppConstants.SIDEBAR_EXPIRATION_LABEL,
    min_value=AppConstants.EXPIRATION_MIN_HOURS,
    max_value=AppConstants.EXPIRATION_MAX_HOURS,
    value=AppConstants.EXPIRATION_DEFAULT_HOURS
)
expiration_seconds = int(expiration_hours * AppConstants.SECONDS_PER_HOUR)

# Initialize Client
s3_client = None
buckets = []
try:
    s3_client = get_s3_client(region)
    resp = s3_client.list_buckets()
    buckets = [b[AppConstants.KEY_NAME] for b in resp.get(AppConstants.KEY_BUCKETS, [])]
except Exception as e:
    st.sidebar.error(f"{AppConstants.SIDEBAR_ERROR_PREFIX}{e}")

# Bucket List in Sidebar
st.sidebar.header(AppConstants.SIDEBAR_BUCKETS_HEADER)
selected_bucket = None
if buckets:
    selected_bucket = st.sidebar.radio(AppConstants.SIDEBAR_BUCKETS_LABEL, buckets)
else:
    st.sidebar.warning(AppConstants.SIDEBAR_NO_BUCKETS_WARNING)

# --- Main App Logic ---

# Initialize session state for path navigation
if AppConstants.SESSION_CURRENT_PATH not in st.session_state:
    st.session_state[AppConstants.SESSION_CURRENT_PATH] = AppConstants.EMPTY_STRING

# Reset path if bucket changes
if AppConstants.SESSION_LAST_BUCKET not in st.session_state:
    st.session_state[AppConstants.SESSION_LAST_BUCKET] = selected_bucket

if st.session_state[AppConstants.SESSION_LAST_BUCKET] != selected_bucket:
    st.session_state[AppConstants.SESSION_CURRENT_PATH] = AppConstants.EMPTY_STRING
    st.session_state[AppConstants.SESSION_LAST_BUCKET] = selected_bucket

if selected_bucket and s3_client:
    st.header(f"{AppConstants.HEADER_BUCKET_PREFIX}{selected_bucket}")
    
    # 1. Upload Functionality
    st.subheader(AppConstants.UPLOAD_SUBHEADER)
    with st.expander(AppConstants.UPLOAD_EXPANDER_LABEL, expanded=False):
        with st.form("upload_form", clear_on_submit=True):
            uploaded_file = st.file_uploader(AppConstants.UPLOAD_FILE_LABEL, accept_multiple_files=False)
            submit_upload = st.form_submit_button(AppConstants.UPLOAD_BUTTON_LABEL)
            
            if submit_upload and uploaded_file:
                try:
                    # Construct key based on current path
                    file_key = f"{st.session_state[AppConstants.SESSION_CURRENT_PATH]}{uploaded_file.name}"
                    
                    
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

    st.divider()

    # 2. File Explorer
    
    # Breadcrumbs / Navigation Bar
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

    try:
        # Fetch items for the current path
        folders, files_list = get_keys(s3_client,selected_bucket, st.session_state[AppConstants.SESSION_CURRENT_PATH])
        
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
                c0, c1, c2, c3, c4 = st.columns([0.5, 4, 1, 2, 1])
                c0.markdown(AppConstants.TABLE_HEADER_SELECT)
                c1.markdown(AppConstants.TABLE_HEADER_NAME)
                c2.markdown(AppConstants.TABLE_HEADER_SIZE)
                c3.markdown(AppConstants.TABLE_HEADER_MODIFIED)
                c4.markdown(AppConstants.TABLE_HEADER_ACTION)
                
                selected_keys = []
                
                for file_data in files_list:
                    row_c0, row_c1, row_c2, row_c3, row_c4 = st.columns([0.5, 4, 1, 2, 1])
                    
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

else:
    st.info(AppConstants.INFO_SELECT_BUCKET)