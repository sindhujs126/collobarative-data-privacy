"""
This module contains code to deal with application settings
:Author: Sindhu J S (sindhujs126@gmail.com)
"""
import os
from os import path
import logging
from functools import lru_cache
from pydantic import (BaseSettings)

logger = logging.getLogger(__name__)


class AppSettings(BaseSettings):
    """
    This class represents all settings the server would need.
    """
    try:
        if os.getuid() == 0:
            log_path = '/var/log'
        else:
            log_path = '/tmp'
    except Exception as e:
        log_path = '/tmp'
    if not path.exists(log_path):
        os.makedirs(log_path)
    log_file_path = path.join(log_path, 'data-cap-privacy.log')

    log_level: str = "DEBUG"

    class Config(BaseSettings.Config):
        env_prefix: str = ''  # defaults to 'APP_'; see description in pydantic docs
        case_insensitive = True
        allow_mutation: bool = False


@lru_cache()
def get_settings():
    """
    Creates a new instance of AppSettings and overrides the values from config file from environment.
    For more read https://pydantic-docs.helpmanual.io/#id5
    :return: Application settings instance
    """
    settings = AppSettings()
    return settings
