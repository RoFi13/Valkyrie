# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""Various maya constraint utility functions."""
# Can't find PySide2 modules pylint: disable=I1101

import logging
import os

from maya import cmds

LOG = logging.getLogger(os.path.basename(__file__))


def batch_parent_constraint(maintain_offset: bool = True):
    """Batch parent constraints non offset.

    Args:
        maintain_offset (bool, optional): Whether to have the parent constraint
            maintain it's offset. Defaults to True.
    """
    # Need at least 2 objects selected
    selection = cmds.ls(selection=True)
    if len(selection) < 2:
        LOG.info("Select at least 2 objects")
        return

    driver_object = selection[0]
    driven_objects = selection[1:]
    for item in driven_objects:
        LOG.info("object: %s", item)
        cmds.parentConstraint(driver_object, item, maintainOffset=maintain_offset)
