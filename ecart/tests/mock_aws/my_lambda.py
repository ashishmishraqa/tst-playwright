import boto3
import os

def handler(event, context):
    s3 = boto3.client("s3")  # ✅ picks up env vars automatically
    bucket = os.environ.get("BUCKET_NAME", "test-bucket")
    s3.put_object(Bucket=bucket, Key=event["key"], Body=b"data")