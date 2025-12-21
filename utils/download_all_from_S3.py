import boto3
from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_KEY = os.getenv("ACCESS_KEY_ID")
SECRET_KEY = os.getenv("SECRET_ACCESS_KEY")
ENDPOINT   = os.getenv("ENDPOINT_URL")
BUCKET_NAME = "devimmersobuk02"
FOLDER_PREFIX = "Play_app"  # folder path (can be empty string for full bucket)
EXPIRY_SECONDS = 100 * 4 * 90 * 24 * 60 * 60  # 90 days

s3 = boto3.client(
    "s3",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    endpoint_url=ENDPOINT
)

# List all objects (recursively)
objects = []
paginator = s3.get_paginator("list_objects_v2")
for page in paginator.paginate(Bucket=BUCKET_NAME, Prefix=FOLDER_PREFIX):
    if "Contents" in page:
        objects.extend(page["Contents"])

# Generate presigned URLs for each object
urls = {}
for obj in objects:
    key = obj["Key"]
    if key.endswith((".jpg", ".jpeg", ".png", ".svg", ".gif", ".webp")):
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": key},
            ExpiresIn=EXPIRY_SECONDS
        )
        urls[key] = url

# Print or save the results
for key, url in urls.items():
    print(f"{key} -> {url}")
