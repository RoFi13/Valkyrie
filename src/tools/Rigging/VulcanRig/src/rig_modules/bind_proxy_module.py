# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""Bare bones Unreal Bind Skeleton functions."""

from enum import Enum
import logging
import os

from maya import cmds, mel

from Core import core_paths as cpath

from ..data.bind_modules_positions import BindModulePositions
from ..data.ue_skeleton_names import EpicBasicSkeleton, EpicCorrectiveJoints
from ..util import vulcan_validations

from importlib import reload

reload(vulcan_validations)


# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 2)}"

LOG = logging.getLogger(os.path.basename(__file__))

HALF_BIND_SKELETON = (
    f"{cpath.get_parent_directory(__file__, 1)}/data/half_bind_skeleton.fbx"
)


def create_unreal_bind_skeleton():
    """Import right half of the unreal bind skeleton."""
    if vulcan_validations.does_bind_skeleton_exist():
        LOG.warning("Bind Proxy skeleton already exists in the scene!")
        return

    cmds.file(
        HALF_BIND_SKELETON,
        i=True,
        type="FBX",
        ignoreVersion=True,
        renameAll=True,
        mergeNamespacesOnClash=False,
        renamingPrefix="BPX",
        options="fbx",
    )


def orient_joint_chain(module: BindModulePositions):
    """Give the joint chain an initial orientation.

    Args:
        module (BindModulePositions): Module to orient.
    """
    cmds.joint(
        module.value[0]["name"],
        edit=True,
        orientJoint="xyz",
        secondaryAxisOrient="zdown",
        autoOrientSecondaryAxis=False,
        children=True,
        zeroScaleOrient=True,
    )


def finalize_bind_skeleton():
    """Mirror proxy Bind skeleton."""
    if not cmds.objExists(f"{EpicBasicSkeleton.PELVIS.value}_BPX"):
        LOG.warning(
            "Proxy Bind skeleton doesn't exist. Expecting proxy UE skeleton with "
            "'%s' joint existing as root.",
            EpicBasicSkeleton.PELVIS.value,
        )
        return

    cmds.select(f"{EpicBasicSkeleton.PELVIS.value}_BPX", replace=True)
    # Remove BPX suffix
    mel.eval('searchReplaceNames "_BPX" " " hierarchy')

    # Mirror Joints
    cmds.select(
        BindModulePositions.LEG_R.value[0]["name"].replace("_BPX", ""), replace=True
    )
    cmds.mirrorJoint(mirrorYZ=True, mirrorBehavior=True, searchReplace=["_r", "_l"])

    cmds.select(
        BindModulePositions.ARM_R.value[0]["name"].replace("_BPX", ""), replace=True
    )
    cmds.mirrorJoint(mirrorYZ=True, mirrorBehavior=True, searchReplace=["_r", "_l"])

    # Mirror last lone joints
    cmds.select(EpicCorrectiveJoints.CLAVICLE_PEC_R.value, replace=True)
    cmds.mirrorJoint(mirrorYZ=True, mirrorBehavior=True, searchReplace=["_r", "_l"])
    cmds.select(EpicCorrectiveJoints.SPINE_04_LATISSIMUS_R.value, replace=True)
    cmds.mirrorJoint(mirrorYZ=True, mirrorBehavior=True, searchReplace=["_r", "_l"])
