import boto3
from moto import mock_aws
import pytest
from tests.mock_aws.my_lambda import handler


@pytest.fixture(scope="function")
def aws_credentials(monkeypatch):
    """Provide dummy AWS credentials so boto3 never looks for real ones."""
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")
    monkeypatch.setenv("AWS_SECURITY_TOKEN", "testing")
    monkeypatch.setenv("AWS_SESSION_TOKEN", "testing")


@pytest.fixture
def aws_env(aws_credentials):
    """Create a single Moto AWS context for each test run."""
    # Moto intercepts AWS calls inside this context, so no real AWS access is used.
    with mock_aws():
        yield


@pytest.fixture
def s3_client(aws_env):
    """Return an S3 client backed by the in-memory Moto mock."""
    client = boto3.client("s3", region_name="us-east-1")
    client.create_bucket(Bucket="test-bucket")
    return client


def test_lambda_uploads_to_s3(s3_client):
    """Verify the Lambda handler writes one object to the mocked S3 bucket."""
    handler({"key": "data.csv"}, None)
    print('file uploaded successfully to s3')

    objs = s3_client.list_objects(Bucket="test-bucket")
    assert "Contents" in objs, "No objects found; handler may not have uploaded"
    assert len(objs["Contents"]) == 1
