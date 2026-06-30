import functools
import json
import os
import boto3
from botocore.exceptions import ClientError
from configs.settings import TestData


class SecretsManager:

    def __init__(self, region_name=None):


        self.is_ci = os.getenv("CI")
        if self.is_ci:
            self.region_name = os.getenv("AWS_REGION") or "us-east-1"
            self.client = boto3.client(service_name="secretsmanager", region_name=self.region_name)
        else:
            self.client = None

    @functools.lru_cache(maxsize=None)
    def get_secret(self, secret_name):
        if not self.is_ci:
            return {
      "username": TestData.get_env("USERNAME"),
      "password": TestData.get_env("PASSWORD")
    }
        try:

            response = self.client.get_secret_value(
                SecretId=secret_name
            )

            secret = response.get("SecretString")
            if secret is None:
                raise Exception(
                    f"Secret '{secret_name}' does not contain a SecretString value"
                )

            return json.loads(secret)

        except ClientError as e:

            raise Exception(
                f"Unable to fetch secret: {e}"
            )
