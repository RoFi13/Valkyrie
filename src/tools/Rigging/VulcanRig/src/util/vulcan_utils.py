# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""Various Vulcan rigging utility functions."""

import logging
import os

from maya import cmds

from Core import core_paths as cpath


# from .. import module_product_factories


# reload(module_metadata)

# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 2)}"

LOG = logging.getLogger(os.path.basename(__file__))


def duplicate_joint_chain(
    start_joint: str, end_joint: str, include_twist_joints: bool = False
):
    """Duplicates joint hierarchy given the start and end joints in chain."""
    # Check to delete twist joints if desired
    if not include_twist_joints:
        joint_children = cmds.listRelatives(start_joint, allDescendents=True)
        for child in joint_children:
            if "twist" in child or "Twist" in child:
                cmds.delete(child)

    # Pickwalk down starting from the start_joint until it reaches the end joint,
    # storing each joint in a list on the way
    i = 0
    newJnts = [start_joint]
    cmds.select(start_joint, replace=True)
    while i < 99:
        # Pick walk and store each new joint down hierarchy
        curJnt = cmds.pickWalk(direction="down")[0]
        if end_joint in curJnt:
            # If the end_joint is equal to the current joint during pick walking, append to list and break loop
            newJnts.append(curJnt)
            break
        else:
            newJnts.append(curJnt)
        i += 1

    # Duplicate new joint list hierarchy
    dupJnts = cmds.duplicate(newJnts, parentOnly=True, renameChildren=True)
    # Parent to world space
    LOG.info("DUPLICATE JOINTS: %s", dupJnts[0])
    cmds.parent(dupJnts[0], world=True)

    LOG.info("test")

    return dupJnts
