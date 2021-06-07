import importlib
from unittest import mock

from app.config import get_settings, SECRETS
import app.config as config


@mock.patch("app.config.get_secret")
def test_get_settings(get_secret):
    get_secret.return_value = "x"
    settings = get_settings()

    for secret in SECRETS:
        assert settings.decrypted_secrets[secret] == get_secret.return_value
    assert settings.app_name == "liamsdemo"


@mock.patch.dict("os.environ", {"SERVER_SOFTWARE": "gunicorn"})
def test_get_logger():
    importlib.reload(config)
