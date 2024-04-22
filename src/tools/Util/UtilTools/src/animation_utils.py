# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""Various functions for animation modification in Maya"""

import logging
import os

from maya import cmds

LOG = logging.getLogger(os.path.basename(__file__))


def zero_rotate_z():
    """Zero out rotate Z for the selected transform node.

    Set all keyframes of selected object for rotate Z attribute to zero.
    """
    selection = cmds.ls(selection=True)

    for node in selection:
        cmds.selectKey(clear=True)
        cmds.selectKey(node + ".rotateZ", keyframe=True, replace=True)
        cmds.keyframe(animation="keys", absolute=True, valueChange=0)


def set_keys_to_stepped_tangents():
    """Make all selected nodes stepped keys on all channel box attributes."""
    selection = cmds.ls(selection=True)
    all_attributes = cmds.listAttr(selection, locked=False, keyable=True)
    cmds.selectKey(clear=True)
    cmds.selectKey(selection, attribute=all_attributes, keyframe=True, addTo=True)
    cmds.keyTangent(outTangentType="step")


def set_keys_to_auto_tangents():
    """Change selected nodes keys to auto tangents."""
    selection = cmds.ls(selection=True)
    all_attributes = cmds.listAttr(selection, locked=False, keyable=True)
    cmds.selectKey(clear=True)
    cmds.selectKey(selection, attribute=all_attributes, keyframe=True, addTo=True)
    cmds.keyTangent(inTangentType="auto", outTangentType="auto")
