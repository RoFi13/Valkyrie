# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""Various Control curve utilities."""

import logging
import os
from random import randrange

from maya import cmds

from importlib import reload

LOG = logging.getLogger(os.path.basename(__file__))


def validate_name(control_name: str):
    """Validate control name so that it is unique in Maya scene.

    Args:
        control_name (str): Name to validate.

    Raises:
        NotImplementedError: Raised if developer fails to implement method.
    """
    if not cmds.objExists(control_name):
        return control_name

    node_num = 1
    while node_num < 9999:
        random_identifier = randrange(9999)
        control_name = f"{control_name}_{random_identifier}"
        if not cmds.objExists(control_name):
            break
        node_num += 1

    return control_name
