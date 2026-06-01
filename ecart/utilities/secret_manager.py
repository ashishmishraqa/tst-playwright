import functools
import json
import os

import boto3
from botocore.exceptions import ClientError


class SecretsManager:

    def __init__(self, region_name=None):

        self.region_name = region_name or os.getenv(
            "AWS_REGION"
        ) or os.getenv("AWS_DEFAULT_REGION")
        self.client = boto3.client(
            service_name="secretsmanager",
            region_name=self.region_name
        )

    @functools.lru_cache(maxsize=None)
    def get_secret(self, secret_name):

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
