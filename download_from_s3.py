import boto3
from datetime import timedelta

ACCESS_KEY = "immersouser"
SECRET_KEY = "7asiEMavUpJwrWgEUEKGmjMl7NkihTLYLZvjiU/V"
ENDPOINT   = "https://sosnm1.shakticloud.ai:9024"
BUCKET_NAME = "immersobuk01"
s3 = boto3.client(
    "s3",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    endpoint_url=ENDPOINT
)
# Object key from your path
obj_key = "Eros-universe/ai-tools-thumbnail/5147eac61a78670cdbfe8882add0063c1208f389.png"

expiry_seconds = 100 * 4 * 90 * 24 * 60 * 60
# Generate presigned URL valid for 1 hour (3600 seconds)
url = s3.generate_presigned_url(
    "get_object",
    Params={
        "Bucket": BUCKET_NAME, 
        "Key": obj_key,
        # "ResponseContentType": "image/png",  # or image/jpeg
        # "ResponseContentDisposition": "inline"
        },
    ExpiresIn=expiry_seconds
)

print(url)
