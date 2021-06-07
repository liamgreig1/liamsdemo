import base64

from unittest import mock

from app.secrets import get_secret, _get_local_secret, _get_aws_secret


@mock.patch("app.secrets._get_local_secret")
def test_get_secret(mock_get_local_secret):
    get_secret("x")

    mock_get_local_secret.assert_called_with("x")


@mock.patch.dict("os.environ", {"ENVIRONMENT_NAME": "prod"})
@mock.patch("app.secrets._get_aws_secret")
def test_get_secret_aws(mock_get_aws_secret):
    get_secret("x")

    mock_get_aws_secret.assert_called_with("x")


@mock.patch.dict("os.environ", {"SECRETS_123": "hello"})
def test__get_local_secret():
    assert "hello" == _get_local_secret("123")


@mock.patch("app.secrets.boto3.session.Session")
def test__get_aws_secret(session):
    x = session.return_value
    p = x.client.return_value
    p.get_secret_value.return_value = {"SecretString": '{"HOST_NAME": 123}'}

    assert {'HOST_NAME': 123} == _get_aws_secret("HOST_NAME")


@mock.patch("app.secrets.boto3.session.Session")
def test__get_aws_secret_binary(session):
    x = session.return_value
    p = x.client.return_value
    p.get_secret_value.return_value = {
        "SecretBinary": base64.b64encode(b'{"HOST_NAME": 123}')
    }

    assert b'{"HOST_NAME": 123}' == _get_aws_secret("HOST_NAME")
