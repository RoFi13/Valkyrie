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


def reset_transforms(
    node: str, translation: bool = True, rotation: bool = True, scale: bool = True
):
    """Reset transform attributes on Maya node."""
    if translation:
        cmds.setAttr(f"{node}.tx", 0)
        cmds.setAttr(f"{node}.ty", 0)
        cmds.setAttr(f"{node}.tz", 0)
    if rotation:
        cmds.setAttr(f"{node}.rx", 0)
        cmds.setAttr(f"{node}.ry", 0)
        cmds.setAttr(f"{node}.rz", 0)
    if scale:
        cmds.setAttr(f"{node}.sx", 1)
        cmds.setAttr(f"{node}.sy", 1)
        cmds.setAttr(f"{node}.sz", 1)


# def freeze_transforms(node: str, translation: bool = True, rotation: bool = True, scale: bool = True):
#     cmds.makeIdentity(
#             apply=True, translate=True, rotate=True, scale=True, normal=False
#         )
#     if translation:
#         cmds.setAttr(f"{node}.tx", 0)
#         cmds.setAttr(f"{node}.ty", 0)
#         cmds.setAttr(f"{node}.tz", 0)
#     if rotation:
#         cmds.setAttr(f"{node}.rx", 0)
#         cmds.setAttr(f"{node}.ry", 0)
#         cmds.setAttr(f"{node}.rz", 0)
#     if scale:
#         cmds.setAttr(f"{node}.sx", 1)
#         cmds.setAttr(f"{node}.sy", 1)
#         cmds.setAttr(f"{node}.sz", 1)
