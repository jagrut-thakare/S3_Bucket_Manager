import streamlit as st
import boto3
import os
from dotenv import load_dotenv
from botocore.client import Config
from utils.constants import AppConstants

# Load environment variables
load_dotenv()

ACCESS_KEY_ID = os.getenv(AppConstants.ENV_ACCESS_KEY_ID)
SECRET_ACCESS_KEY = os.getenv(AppConstants.ENV_SECRET_ACCESS_KEY)
ENDPOINT_URL = os.getenv(AppConstants.ENV_ENDPOINT_URL)

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

@st.cache_resource
def get_s3_client(region_name):
    """
    Initialize S3 client with caching.
    """
    kwargs = {
        AppConstants.AWS_ACCESS_KEY_ID: ACCESS_KEY_ID,
        AppConstants.AWS_SECRET_ACCESS_KEY: SECRET_ACCESS_KEY,
        AppConstants.AWS_REGION_NAME: region_name,
        # Removing explicit signature version to allow longer expirations 
        # as seen in download_from_s3.py
        # AppConstants.AWS_CONFIG: Config(signature_version=AppConstants.S3_SIGNATURE_VERSION)
    }
    if ENDPOINT_URL:
        kwargs[AppConstants.AWS_ENDPOINT_URL] = ENDPOINT_URL
        
    return boto3.client(AppConstants.S3_SERVICE_NAME, **kwargs)

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

def get_keys(bucket_name, prefix=""):
    """
    List keys in a bucket under a specific prefix, emulating a folder structure.
    Returns: folders (list of names), files (list of dicts with details)
    """
    folders = set()
    files = []
    
    paginator = s3_client.get_paginator(AppConstants.S3_LIST_OBJECTS_V2)
    # We add a delimiter to get common prefixes (folders)
    for page in paginator.paginate(
        **{
            AppConstants.PAGINATOR_BUCKET: bucket_name, 
            AppConstants.PAGINATOR_PREFIX: prefix, 
            AppConstants.PAGINATOR_DELIMITER: AppConstants.PATH_SEPARATOR
        }
    ):
        # Extract subfolders (CommonPrefixes)
        if AppConstants.KEY_COMMON_PREFIXES in page:
            for p in page[AppConstants.KEY_COMMON_PREFIXES]:
                # Prefix is like 'folder/subfolder/'
                # We want just the folder name relative to current prefix
                full_prefix = p[AppConstants.KEY_PREFIX]
                folder_name = full_prefix[len(prefix):].strip(AppConstants.PATH_SEPARATOR)
                folders.add(folder_name)
        
        # Extract files (Contents)
        if AppConstants.KEY_CONTENTS in page:
            for obj in page[AppConstants.KEY_CONTENTS]:
                key = obj[AppConstants.KEY_KEY]
                # Skip the folder itself if it appears as a 0-byte object
                if key == prefix:
                    continue
                
                file_name = key[len(prefix):]
                files.append({
                    "Key": key,
                    "Name": file_name,
                    "Size": obj[AppConstants.KEY_SIZE],
                    "LastModified": obj[AppConstants.KEY_LAST_MODIFIED]
                })
    
    return sorted(list(folders)), sorted(files, key=lambda x: x["Name"])

def format_size(size):
    for unit in AppConstants.SIZE_UNITS:
        if size < 1024.0:
            return AppConstants.SIZE_FORMAT_STRING.format(size=size, unit=unit)
        size /= 1024.0
    return AppConstants.SIZE_PB_FORMAT.format(size=size)

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
                        s3_client.upload_fileobj(uploaded_file, selected_bucket, file_key)
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
        folders, files_list = get_keys(selected_bucket, st.session_state[AppConstants.SESSION_CURRENT_PATH])
        
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
            # Header
            c1, c2, c3, c4 = st.columns([4, 1, 2, 1])
            c1.markdown(AppConstants.TABLE_HEADER_NAME)
            c2.markdown(AppConstants.TABLE_HEADER_SIZE)
            c3.markdown(AppConstants.TABLE_HEADER_MODIFIED)
            c4.markdown(AppConstants.TABLE_HEADER_ACTION)
            
            for file_data in files_list:
                with st.container():
                    row_c1, row_c2, row_c3, row_c4 = st.columns([4, 1, 2, 1])
                    
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
                        
    except Exception as e:
        st.error(f"{AppConstants.ERROR_LISTING_CONTENTS}{e}")

else:
    st.info(AppConstants.INFO_SELECT_BUCKET)