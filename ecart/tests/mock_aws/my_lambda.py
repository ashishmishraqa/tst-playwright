import os

import boto3


def handler(event):
    # s3 = boto3.client("s3")  # ✅ picks up env vars automatically
    client = boto3.client(service_name="s3")
    bucket = os.getenv("BUCKET_NAME")
    client.put_object(
        Bucket=bucket, Key=event["key"], Body=b"data"
    )  # data converted to bytes , because s3 needs object not a string
