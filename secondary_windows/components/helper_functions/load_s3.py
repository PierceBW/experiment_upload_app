#Load in S3
import boto3
import os
from dotenv import load_dotenv


# Log in and get S3
load_dotenv()

client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('aws_access_key_id'),
    aws_secret_access_key=os.getenv('aws_secret_access_key'),
    aws_session_token=os.getenv('aws_session_token')
)