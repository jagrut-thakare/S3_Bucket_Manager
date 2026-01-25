import boto3
from botocore.config import Config
from utils.constants import AppConstants
from config import ACCESS_KEY_ID, SECRET_ACCESS_KEY, ENDPOINT_URL
import streamlit as st

def upload_file_v2(file_obj, bucket_name, object_key, access_key, secret_key, endpoint_url=None, region_name=None):
    """
    Uploads a file object to S3 using signature version 's3' (v2).
    This creates a dedicated temporary client to avoid affecting the global app client.
    """
    kwargs = {
        AppConstants.AWS_ACCESS_KEY_ID: access_key,
        AppConstants.AWS_SECRET_ACCESS_KEY: secret_key,
        AppConstants.AWS_REGION_NAME: region_name,
        AppConstants.AWS_CONFIG: Config(signature_version='s3')
    }
    if endpoint_url:
        kwargs[AppConstants.AWS_ENDPOINT_URL] = endpoint_url
        
    # Create a new client specifically for this upload
    s3_v2_client = boto3.client(AppConstants.S3_SERVICE_NAME, **kwargs)
    
    # Ensure pointer is at the start (just in case)
    file_obj.seek(0)
    
    s3_v2_client.upload_fileobj(file_obj, bucket_name, object_key)
    return True

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

def get_keys(s3_client, bucket_name, prefix=""):
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