# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""Various Windows OS functions."""

import logging
import os
from pathlib import PurePath
import subprocess

from maya import cmds

LOG = logging.getLogger(os.path.basename(__file__))


def open_file_directory():
    """Open the current selected shot's root folder."""
    current_file_path = PurePath(cmds.file(query=True, sceneName=True))
    parent_directory_path = current_file_path.parent
    with subprocess.Popen(f"explorer {parent_directory_path}"):
        pass
