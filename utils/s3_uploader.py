
import boto3
from botocore.config import Config
from utils.constants import AppConstants

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
