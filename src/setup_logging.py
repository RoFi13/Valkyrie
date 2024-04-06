# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""Set up logging levels and basic configurations."""

from datetime import datetime
import logging
import logging.config

from Core import core_paths

CONFIG_DIR = f"{core_paths.core_paths()['configs']}"
LOG_DIR = f"{core_paths.core_paths()['logs']}"


def setup_logging(current_env="dev"):
    """Load logging configuration"""
    log_configs = {"dev": "logging.dev.ini", "prod": "logging.prod.ini"}

    config_path = "/".join([CONFIG_DIR, log_configs[current_env]])

    # timestamp = datetime.now().strftime("%Y%m%d-%H.%M.%S")
    timestamp = datetime.now().strftime("%Y%m%d")

    logging.warning("Config path being loaded: %s", config_path)

    logging.config.fileConfig(
        config_path,
        disable_existing_loggers=False,
        defaults={"logfilename": f"{LOG_DIR}/{timestamp}.log"},
    )

    logging.warning("Current environment: %s", current_env)


if __name__ == "__main__":
    setup_logging()
