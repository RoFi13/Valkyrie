# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""Various functions for modeling utilities in Maya"""

import logging
import os

from maya import cmds

LOG = logging.getLogger(os.path.basename(__file__))


def copy_pivot():
    """Copy pivot translate and rotate from driver to driven (selection order)."""
    selection = cmds.ls(selection=True)
    if len(selection) != 2:
        logging.error("Please select a source and target object.")
        return

    target_parent = cmds.listRelatives(selection[1], parent=True)

    source_object_pivot = cmds.xform(
        selection[0], query=True, worldSpace=True, rotatePivot=True
    )
    cmds.parent(selection[1], selection[0])
    cmds.makeIdentity(selection[1], apply=True, translate=True, rotate=True, scale=True)
    cmds.xform(selection[1], worldSpace=True, pivots=source_object_pivot)
    cmds.parent(selection[1], world=True)

    try:
        cmds.parent(selection[1], target_parent)
    except RuntimeError:
        pass
