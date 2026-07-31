import functools
import json
import os
import boto3
from botocore.exceptions import ClientError
from ecart.utilities.logger import get_logger
from ecart.utilities.data_utils import get_env


class SecretsManager:
    """Resolve UI credentials from an explicit provider configuration.

    ``AWS_SECRET_NAME`` selects AWS Secrets Manager.  Without it, credentials
    come from ``USER_NAME`` and ``PASSWORD`` in the process environment (or
    the local .env file loaded by settings).  This intentionally does not
    inspect CI-specific variables, so the same test command works in GitHub
    Actions, Jenkins, Docker, or any other runner.
    """

    log = get_logger(__name__)

    def __init__(self, region_name=None):
        self.region_name = (
            region_name
            or os.getenv("AWS_REGION")
            or os.getenv("AWS_DEFAULT_REGION")
            or "us-east-1"
        )

    @functools.lru_cache(maxsize=None)
    def get_secret(self, secret_name=None):
        """Return credentials from AWS when a secret name is explicitly set."""
        secret_name = secret_name or os.getenv("AWS_SECRET_NAME")
        if not secret_name:
            self.log.info("Using credentials from environment variables")
            return {
                "username": get_env("USER_NAME"),
                "password": get_env("PASSWORD"),
            }

        self.log.info(
            "Using AWS Secrets Manager for credentials", extra={"secret_name": secret_name}
        )
        client = boto3.client(
            service_name="secretsmanager", region_name=self.region_name
        )
        try:
            response = client.get_secret_value(SecretId=secret_name)

            secret = response.get("SecretString")
            if secret is None:
                raise RuntimeError(
                    f"Secret '{secret_name}' does not contain a SecretString value"
                )

            credentials = json.loads(secret)
            if not isinstance(credentials, dict) or not {
                "username",
                "password",
            }.issubset(credentials):
                raise RuntimeError(
                    f"Secret '{secret_name}' must contain 'username' and 'password' fields"
                )
            return credentials
        except ClientError as error:
            raise RuntimeError(
                f"Unable to retrieve AWS Secrets Manager secret '{secret_name}': {error}"
            ) from error
