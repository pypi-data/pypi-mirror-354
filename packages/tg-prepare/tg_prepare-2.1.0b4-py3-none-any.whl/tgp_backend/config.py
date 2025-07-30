# -*- coding: utf-8 -*-
# Copyright (C) 2023-2024 TU-Dresden (ZIH)
# ralf.klammer@tu-dresden.de
import logging

from configparser import ConfigParser

log = logging.getLogger(__name__)


def get_config_value(section, parameter, default=None):
    _config = ConfigParser()
    _config.read("config.ini")

    if section not in _config:
        log.warn("Section: %s not in *.ini -> using default" % section)
        return default
    config_val = _config[section].get(parameter)
    if not config_val:
        log.info(
            "Parameter: %s not in section: (%s) of *.ini -> using default: %s"
            % (parameter, section, default)
        )
        return default
    else:
        return config_val


LOG_LEVEL = get_config_value("log", "level", default="INFO")
MAIN_PATH = get_config_value("main", "path", default="./projects")
MAX_FILENAME_LENGTH = get_config_value("main", "maxFileNameLength", default=15)
