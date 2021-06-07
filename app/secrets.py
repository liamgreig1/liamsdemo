import os
import base64
import json

import boto3


def get_secret(secret_name):
    if os.environ.get("ENVIRONMENT_NAME", "") not in ["prod", "sandbox"]:
        return _get_local_secret(secret_name)

    return _get_aws_secret(secret_name)


def _get_local_secret(secret_name):
    return os.environ[f"SECRETS_{secret_name}"]


def _get_aws_secret(secret_name):
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager")

    get_secret_value_response = client.get_secret_value(SecretId=secret_name)

    if "SecretString" in get_secret_value_response:
        return json.loads(get_secret_value_response["SecretString"])
    else:
        return base64.b64decode(get_secret_value_response["SecretBinary"])
