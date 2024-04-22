# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""Various Project utility functions."""

import logging
import os

from Core import core_paths as cpath
from Core.util import file_util_tools as fut

# Main paths
MAIN_PATHS = cpath.core_paths()

LOG = logging.getLogger(os.path.basename(__file__))


def get_project_configs():
    """Load JSON data from ProjectConfig.json file.

    Returns:
        bool: Return project config data as dictionary if found. Otherwise, None.
    """
    config_path = MAIN_PATHS["projectConfigs"]
    if not os.path.exists(config_path):
        LOG.warning(
            "No ProjectConfig.json file found in project at path %s...", config_path
        )
        return {}

    return fut.get_json_data(config_path)


def get_project_config_item(config_name: str):
    """Get project config dictionary item.

    Args:
        config_name (str): Name of key to get value from.import

    Returns:
        any: Value of key from configs. Could be str, int, float, etc.
    """
    project_configs = get_project_configs()

    if project_configs is None:
        return None

    return project_configs[config_name]
