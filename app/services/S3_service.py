import shutil

import boto3
import traceback
import os

from app.config import Config

# Initialize a session using your credentials
session = boto3.Session(
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
    region_name='us-east-1'
)

# Initialize the S3 client
s3_client = session.client('s3')


def download_file(bucket_name, object_key, download_path):
    """
    Download a file from an S3 bucket.

    :param bucket_name: The name of the S3 bucket
    :param object_key: The key of the object in the S3 bucket
    :param download_path: The path where the file will be saved locally
    """
    try:
        s3_client.download_file(bucket_name, object_key, download_path)
        print(f"File downloaded successfully to {download_path}")
        print(os.getcwd())
    except Exception as e:
        print(f"Error downloading file: {e}")
        traceback.print_exc()


def upload_file_s3(local_file_path, s3_path):
    s3_client.upload_file(local_file_path, Config.AWS_S3_BUCKET_NAME, s3_path)
    print("Uploaded the file to: ", s3_path)
    if os.path.isdir(local_file_path):
        shutil.rmtree(local_file_path)
