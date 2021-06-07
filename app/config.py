from functools import lru_cache
import logging
import logging.config
import os

from fastapi.logger import logger as fastapi_logger
from pydantic import BaseSettings

from app.secrets import get_secret


SECRETS = [
    # "liamsdemo_SECRET1"
]


class Settings(BaseSettings):
    app_name: str = "liamsdemo"
    decrypted_secrets: dict = {}

    def __init__(self):
        super(Settings, self).__init__()
        self.decrypt_secrets()

    def decrypt_secrets(self):
        for secret in SECRETS:
            self.decrypted_secrets[secret] = get_secret(secret)


@lru_cache()
def get_settings():
    return Settings()


root_level = logging.DEBUG

if "gunicorn" in os.environ.get("SERVER_SOFTWARE", ""):
    gunicorn_error_logger = logging.getLogger("gunicorn.error")
    root_level = gunicorn_error_logger.level
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.handlers = gunicorn_error_logger.handlers

    fastapi_logger.handlers = gunicorn_error_logger.handlers
else:
    fastapi_logger.setLevel(root_level)


logging_conf = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "%(asctime)s"
            " - %(process)s"
            " - %(name)s"
            " - %(levelname)s"
            " - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "level": root_level,
        },
    },
    "root": {"handlers": ["console"], "level": root_level},
    "loggers": {
        "gunicorn": {"propagate": True},
        "uvicorn": {"propagate": True},
        "uvicorn.access": {"propagate": True},
    },
}

if os.environ.get("ENVIRONMENT_NAME", "") in ["prod", "sandbox"]:
    logging_conf["handlers"]["watchtower"] = {
        "level": root_level,
        "class": "watchtower.CloudWatchLogHandler",
        "log_group": "liamsdemo",
        "stream_name": "logstream-{strftime:%y-%m-%d}",
        "formatter": "default",
    }
    logging_conf["root"]["handlers"].append("watchtower")

logging.config.dictConfig(logging_conf)
