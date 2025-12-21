import boto3
from botocore.config import Config

ACCESS_KEY = "immersouser"
SECRET_KEY = "7asiEMavUpJwrWgEUEKGmjMl7NkihTLYLZvjiU/V"
ENDPOINT   = "https://sosnm1.shakticloud.ai:9024"
BUCKET_NAME = "devimmersobuk02"

s3 = boto3.client(
    "s3",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    endpoint_url=ENDPOINT,
    config=Config(signature_version='s3')
)


def upload_image(local_path: str, s3_key: str = None) -> str:
    with open(local_path, 'rb') as f:
        s3.put_object(Bucket=BUCKET_NAME, Key=s3_key, Body=f.read())
    print(f"Uploaded: {local_path} -> s3://{BUCKET_NAME}/{s3_key}")
    return s3_key


if __name__ == "__main__":
    local_path = '/home/cepl/Desktop/temp/Face_Swap.png'
    s3_key = 'Face_Swap.png'
    
    upload_image(local_path, s3_key)
