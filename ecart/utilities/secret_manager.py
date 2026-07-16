import functools
import json
import os
import boto3
from botocore.exceptions import ClientError
from ecart.configs.settings import TestData
from ecart.utilities.logger import get_logger


class SecretsManager:

    log = get_logger(__name__)

    def __init__(self, region_name=None):


        self.is_ci = os.getenv("CI")
        if self.is_ci:
            self.region_name = os.getenv("AWS_REGION") or "us-east-1"
            self.client = boto3.client(service_name="secretsmanager", region_name=self.region_name)
            self.log.info("Using AWS Secrets Manager")
        else:
            self.client = None
            self.log.info("Using local development environment, fetching secrets from environment variables")

    @functools.lru_cache(maxsize=None)
    def get_secret(self, secret_name):
        if not self.is_ci:
            return {
                      "username": TestData.get_env("USER_NAME"),
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
