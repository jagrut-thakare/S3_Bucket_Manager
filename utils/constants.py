class AppConstants:
    PAGE_TITLE = "S3 Browser & Uploader"
    PAGE_LAYOUT = "wide"
    
    # Environment Variables
    ENV_ACCESS_KEY_ID = "ACCESS_KEY_ID"
    ENV_SECRET_ACCESS_KEY = "SECRET_ACCESS_KEY"
    ENV_ENDPOINT_URL = "ENDPOINT_URL"

    # S3 Config
    S3_SERVICE_NAME = "s3"
    S3_SIGNATURE_VERSION = "s3v4"
    S3_LIST_OBJECTS_V2 = "list_objects_v2"
    S3_GET_OBJECT = "get_object"
    
    # AWS Config Keys (boto3)
    AWS_ACCESS_KEY_ID = "aws_access_key_id"
    AWS_SECRET_ACCESS_KEY = "aws_secret_access_key"
    AWS_REGION_NAME = "region_name"
    AWS_CONFIG = "config"
    AWS_ENDPOINT_URL = "endpoint_url"

    # S3 Response Keys
    KEY_BUCKETS = "Buckets"
    KEY_NAME = "Name"
    KEY_CONTENTS = "Contents"
    KEY_COMMON_PREFIXES = "CommonPrefixes"
    KEY_PREFIX = "Prefix"
    KEY_KEY = "Key"
    KEY_SIZE = "Size"
    KEY_LAST_MODIFIED = "LastModified"
    
    # Session State
    SESSION_CURRENT_PATH = "current_path"
    SESSION_LAST_BUCKET = "last_bucket"
    
    # Sidebar
    SIDEBAR_CONFIG_HEADER = "Configuration"
    SIDEBAR_REGION_LABEL = "Region"
    SIDEBAR_BUCKETS_HEADER = "Available Buckets"
    SIDEBAR_BUCKETS_LABEL = "Buckets"
    SIDEBAR_NO_BUCKETS_WARNING = "No buckets found or connection failed."
    SIDEBAR_ERROR_PREFIX = "Error connecting to S3: "
    
    # Regions
    REGION_US_EAST_1 = "us-east-1"
    REGION_AP_SOUTH_1 = "ap-south-1"
    AVAILABLE_REGIONS = [REGION_US_EAST_1, REGION_AP_SOUTH_1]

    # Main App Logic
    HEADER_BUCKET_PREFIX = "Bucket: "
    UPLOAD_SUBHEADER = "⬆️ Upload File"
    UPLOAD_EXPANDER_LABEL = "Upload a file to current folder"
    UPLOAD_FILE_LABEL = "Choose files (or drag & drop a folder or zip file)"
    UPLOAD_BUTTON_LABEL = "⬆️ Upload"
    UPLOAD_SUCCESS_PREFIX = "⬆️ Uploaded: "
    UPLOAD_FAILED_PREFIX = "⬆️ Upload failed: "
    UPLOAD_SPINNER_PREFIX = "⬆️ Uploading "
    FORM_UPLOAD = "upload_form"
    
    # Navigation
    NAV_CURRENT_PATH_PREFIX = "**Current Path:** "
    NAV_ROOT_LABEL = "`/` (Root)"
    NAV_BACK_BUTTON = "⬅️ Back"
    NAV_HOME_BUTTON = "🏠 Home"
    
    # File Explorer
    DIR_EMPTY_INFO = "This directory is empty."
    FOLDERS_SUBHEADER = "### Folders"
    FILES_SUBHEADER = "### Files"
    FOLDER_KEY_PREFIX = "folder_"
    
    # Table Headers
    TABLE_HEADER_NAME = "**Name**"
    TABLE_HEADER_SIZE = "**Size**"
    TABLE_HEADER_MODIFIED = "**Last Modified**"
    TABLE_HEADER_ACTION = "**Action**"
    
    # File Rows
    FILE_ICON_PREFIX = "📄 "
    FOLDER_ICON_PREFIX = "📁 "
    
    # Download
    DOWNLOAD_LINK_TEXT = "[⬇️ Download]({url})"
    DOWNLOAD_ERROR_MSG = "Error"
    
    # Errors
    ERROR_LISTING_CONTENTS = "Error listing bucket contents: "
    INFO_SELECT_BUCKET = "⬅️ Please select a bucket from the sidebar to view contents."

    # Date Format
    DATE_FORMAT = "%Y-%m-%d %H:%M"

    # Misc
    PATH_SEPARATOR = "/"
    EMPTY_STRING = ""
    
    # Pagination
    PAGINATOR_BUCKET = "Bucket"
    PAGINATOR_PREFIX = "Prefix"
    PAGINATOR_DELIMITER = "Delimiter"
    
    # Presigned URL
    PRESIGNED_PARAMS = "Params"
    PRESIGNED_EXPIRES_IN = "ExpiresIn"
    PRESIGNED_BUCKET = "Bucket"
    PRESIGNED_KEY = "Key"
    PRESIGNED_EXPIRY_SECONDS = 3600
    
    # Expiration Config
    SIDEBAR_EXPIRATION_LABEL = "Link Validity (Hours)"
    EXPIRATION_MIN_HOURS = 1
    EXPIRATION_MAX_HOURS = 876600 # 100 Years (approx)
    EXPIRATION_DEFAULT_HOURS = 1
    SECONDS_PER_HOUR = 3600
    
    # Unit Formatting
    SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB']
    SIZE_FORMAT_STRING = "{size:.1f} {unit}"
    SIZE_PB_FORMAT = "{size:.1f} PB"

    # Bulk Delete
    TABLE_HEADER_SELECT = "**Select**"
    BUTTON_DELETE_SELECTED = "🗑️ Delete Selected"
    DELETE_SUCCESS_MSG = "Successfully deleted {count} files."
    DELETE_ERROR_MSG = "Error deleting files: "
    NO_FILES_SELECTED_MSG = "No files selected for deletion."
    CHECKBOX_LABEL = "Select"
    DELETE_SPINNER_PREFIX = "Deleting selected files..."

    # Create Folder
    CREATE_FOLDER_SUBHEADER = "📁 Create Folder"
    CREATE_FOLDER_EXPANDER = "📁 Create New Folder"
    CREATE_FOLDER_LABEL = "📁 Folder Name"
    CREATE_FOLDER_BUTTON = "📁 Create Folder"
    CREATE_FOLDER_SUCCESS = "📁 Created folder: "
    CREATE_FOLDER_ERROR = "📁 Error creating folder: "
    CREATE_FOLDER_EXISTS_OR_INVALID = "📁 Invalid folder name or folder already exists."
