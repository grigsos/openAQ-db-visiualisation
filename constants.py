import os
import boto3

DEPLOYMENT_FILE : str = os.environ.get('DEPLOYMENT_FILE')
LOCAL_FILE : str = os.environ.get('LOCAL_FILE')
REGION_NAME: str = os.environ.get('REGION_NAME')
S3_BUCKET_NAME : str = os.environ.get('S3_BUCKET_NAME')
TABLE_NAME: str = os.environ.get('TABLE_NAME')

s3 = boto3.resource('s3')
bucket = None

def initialize_s3_bucket():
    global bucket
    bucket = s3.Bucket(S3_BUCKET_NAME)
    return bucket

def get_s3_bucket():
    global bucket
    if bucket is None:
        initialize_s3_bucket()
    return bucket