# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""Various scene and object validation utility functions."""

import logging
import os

from ..data.ue_skeleton_names import EpicBasicSkeleton
from ..data.bind_modules_positions import BindModulePositions

from maya import cmds

from importlib import reload

LOG = logging.getLogger(os.path.basename(__file__))


def validate_bind_skeleton():
    """Validate that Basic Epic Bind skeleton exists in scene.

    Returns:
        bool: True if all joints exist. Otherwise, False.
    """
    LOG.debug("Validating Epic Bind skeleton exists in scene...")
    missing_joints = []
    for key in EpicBasicSkeleton:
        if key == EpicBasicSkeleton.ROOT:
            continue

        if not cmds.objExists(key.value):
            missing_joints.append(key.value)

    if len(missing_joints) > 0:
        error_msg = (
            "Failed to find the following joints in Epic Bind skeleton:\n"
            "------------------------------------------------\n"
        )
        error_msg += "\n".join(missing_joints)
        LOG.error(error_msg)
        return False

    return True


def does_bind_skeleton_exist():
    """Check if the Bind proxy skeleton exists in the scene.

    Returns:
        bool: True if skeleton joints exist. Otherwise, False.
    """
    for bind_module in BindModulePositions:
        for bind_joint in bind_module.value:
            if cmds.objExists(bind_joint["name"]):
                return True

    for bind_joint in EpicBasicSkeleton:
        if cmds.objExists(bind_joint.value):
            return True

    return False
