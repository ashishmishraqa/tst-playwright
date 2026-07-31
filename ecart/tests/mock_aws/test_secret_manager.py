"""Provider-selection tests for framework credentials."""

import json

from ecart.utilities.secret_manager import SecretsManager


def test_environment_credentials_do_not_depend_on_ci_flag(monkeypatch):
    """Any runner uses environment credentials unless AWS is explicitly selected."""
    monkeypatch.setenv("CI", "true")
    monkeypatch.delenv("AWS_SECRET_NAME", raising=False)
    monkeypatch.setenv("USER_NAME", "local-user")
    monkeypatch.setenv("PASSWORD", "local-password")

    assert SecretsManager().get_secret() == {
        "username": "local-user",
        "password": "local-password",
    }


def test_aws_secret_name_selects_aws_secrets_manager(monkeypatch):
    class FakeSecretsClient:
        def get_secret_value(self, SecretId):
            assert SecretId == "ui-test-user"
            return {
                "SecretString": json.dumps(
                    {"username": "aws-user", "password": "aws-password"}
                )
            }

    captured = {}

    def create_client(service_name, region_name):
        captured.update(service_name=service_name, region_name=region_name)
        return FakeSecretsClient()

    monkeypatch.setenv("AWS_SECRET_NAME", "ui-test-user")
    monkeypatch.setenv("AWS_REGION", "us-west-2")
    monkeypatch.setattr("ecart.utilities.secret_manager.boto3.client", create_client)

    assert SecretsManager().get_secret() == {
        "username": "aws-user",
        "password": "aws-password",
    }
    assert captured == {"service_name": "secretsmanager", "region_name": "us-west-2"}
