
import streamlit as st
from utils.constants import AppConstants
from utils.bucket import get_s3_client

def render_sidebar():
    """
    Renders the sidebar configuration and returns selected settings.
    Returns:
        tuple: (s3_client, selected_bucket, expiration_seconds)
    """
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
        
    return s3_client, selected_bucket, expiration_seconds, region
