# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""Spine Rig Module build instructions."""

from __future__ import annotations
import ast
import logging
import os
from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
)

from maya import cmds

from .. import module_product_factories

from Core import core_paths as cpath
from Core.ui.UIUtilTools.src import pyside_util_tools as put

# from Rigging.VulcanRig.src.controls.control_factory import ControlFactory
from Rigging.VulcanRig.src.controls import control_factory
from Rigging.VulcanRig.src.data import module_metadata, build_options
from Rigging.VulcanRig.src.data.build_options import ControllerBuildOptions
from Rigging.VulcanRig.src.data.module_types import ModuleType
from Rigging.VulcanRig.src.data.ue_skeleton_names import EpicBasicSkeleton
from Rigging.VulcanRig.src.util import vulcan_utils as vutil

from Util.UtilTools.src import maya_pyside_interface as mpi
from Util.UtilTools.src import animation_utils


if TYPE_CHECKING:
    from Rigging.VulcanRig.src.vulcan_rig import VulcanRig

from importlib import reload

reload(module_product_factories)
reload(animation_utils)
reload(vutil)
reload(control_factory)
reload(build_options)
reload(put)
reload(mpi)
reload(module_metadata)

# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 2)}"

LOG = logging.getLogger(os.path.basename(__file__))


def create_kinematic_chain(start_joint: str, end_joint: str, is_ik: bool = True):
    """Create a new Kinematic chain, either IK or FK."""
    suffix = "IK_JNT"
    if not is_ik:
        suffix = "FK_JNT"
    new_joint_chain = []
    for chain_joint in vutil.duplicate_joint_chain(start_joint, end_joint):
        new_joint_name = f"{chain_joint.split('_dup')[0]}_{suffix}"
        new_joint_chain.append(cmds.rename(chain_joint, new_joint_name))

    return new_joint_chain


def generate_spine_module(start_joint: str, end_joint: str):
    """Creates the spine module control rig."""
    controller_factory = control_factory.ControlFactory()
    #################################################################################
    # Get start and end joint from UI
    # start_joint = lineStartJnt.text()
    # end_joint = lineEndJnt.text()
    #################################################################################

    # Duplicate joint chain from start to end joint twice; rename one to IK and the other to FK
    # Duplicate arm hierarchy for IK joints and rename
    ik_chain = create_kinematic_chain(start_joint, end_joint)
    # Duplicate arm hierarchy for FK joints and rename
    fk_chain = create_kinematic_chain(start_joint, end_joint, False)
    #################################################################################
    # Create root controller with offset
    root_ctrl = controller_factory.create_controller(
        ControllerBuildOptions("square", "root")
    )
    # root_ctrl_offset = controller_factory.add_offset_group(root_ctrl)
    root_ctrl_offset = controller_factory.create_offset_group(
        root_ctrl.split("_CTL")[0], fk_chain[0], match_rotation=False
    )
    cmds.parent(root_ctrl, root_ctrl_offset)
    animation_utils.reset_transforms(root_ctrl, rotation=True)
    cmds.setAttr(f"{root_ctrl}.scale", 2.1, 2.1, 2.1, type="double3")
    cmds.makeIdentity(apply=True, translate=True, rotate=True, scale=True, normal=False)

    # TODO: Work on this next 6/1/24
    # Create FK controls for each FK spine joint
    fkCtrlGrps = []
    fkCtrls = []
    for jnt in fk_chain[1:-1]:
        # Create circle controls and snap to joint locations and orientations for offset nodes
        ctrl = rc.createSquareCtrl(jnt.replace("_JNT", "_CTL"))
        cmds.select(ctrl, replace=True)
        draw.changeColor("17")
        ctrlGrp = cmds.group(ctrl, name=ctrl.replace("_CTL", "Offset_GRP"))
        cmds.delete(cmds.parentConstraint(jnt, ctrlGrp, maintainOffset=False))
        # Append new nodes to list
        fkCtrlGrps.append(ctrlGrp)
        fkCtrls.append(ctrl)
        if not "arm" in ctrl:
            # Orient constrain FK joints to FK controls; May not need to store these orient constraints in memory
            cmds.orientConstraint(ctrl, jnt, maintainOffset=False)
        else:
            # Parent constraint for FK arm joint to controller since I'm not using different space switches for FK arms
            cmds.parentConstraint(ctrl, jnt, maintainOffset=False)

    # # Parent FK hierarchy
    # # This basically just parents the offset group nodes to the control number right above it
    # # i.e. offset04 -> ctrl03; offset03 -> ctrl02
    # i = 0
    # offsetNum = -1
    # ctrlNum = -2
    # while i <= 100:
    #     if not fkCtrlGrps[offsetNum] == fkCtrlGrps[1]:
    #         cmds.parent(fkCtrlGrps[offsetNum], fkCtrls[ctrlNum])
    #     else:
    #         cmds.parent(fkCtrlGrps[offsetNum], fkCtrls[ctrlNum])
    #         break
    #     offsetNum -= 1
    #     ctrlNum -= 1
    #     i += 1

    # #################################################################################
    # # Duplicate starting joint and last joint separately from the rest of the chain
    # # Rename new start joint as C_pelvis_JNT and end joint as C_chest_JNT
    # pelvisJnt = cmds.duplicate(start_joint, parentOnly=True, name="C_pelvis_JNT")
    # chestJnt = cmds.duplicate(end_joint, parentOnly=True, name="C_chest_JNT")
    # # Create controls for the pelvis and chest
    # pelvisCtrl = rc.createPelvisCtrl("C_pelvis_CTL")
    # pelvisOffset = cmds.group(pelvisCtrl, name=pelvisCtrl.replace("_CTL", "Offset_GRP"))
    # cmds.delete(cmds.parentConstraint(pelvisJnt, pelvisOffset, maintainOffset=False))
    # # Using the same type of modified nurbs controller for the chest as well. This is on purpose
    # chestCtrl = rc.createPelvisCtrl("C_chest_CTL")
    # chestOffset = cmds.group(chestCtrl, name=chestCtrl.replace("_CTL", "Offset_GRP"))
    # cmds.delete(cmds.parentConstraint(chestJnt, chestOffset, maintainOffset=False))

    # # Create Ik spline handle using the IK joint chain with following settings:
    # # The following ikHandle command returns: [ikHandle1, effector1, curve1]
    # spineHandle = cmds.ikHandle(
    #     startJoint=ik_chain[0],
    #     endEffector=ik_chain[-1],
    #     solver="ikSplineSolver",
    #     numSpans=4,
    #     parentCurve=False,
    #     simplifyCurve=True,
    #     createCurve=True,
    #     twistType="linear",
    # )
    # spineIKH = cmds.rename(spineHandle[0], "C_spineIK_IKH")
    # spineIkCrv = cmds.rename(spineHandle[-1], "C_spineIK_CRV")
    # # Parent the pelvis joint under pelvis control and chest joint under chest control
    # cmds.parent(pelvisJnt, pelvisCtrl)
    # cmds.parent(chestJnt, chestCtrl)
    # # Select pelvis and chest joints and the IK handle curve and bind skin
    # spineCluster = cmds.skinCluster(
    #     pelvisJnt,
    #     chestJnt,
    #     spineIkCrv,
    #     name="spineCRV_SKC",
    #     toSelectedBones=True,
    #     bindMethod=1,
    #     skinMethod=0,
    #     normalizeWeights=1,
    #     weightDistribution=0,
    #     maximumInfluences=3,
    #     obeyMaxInfluences=True,
    #     removeUnusedInfluence=True,
    # )

    # #################################################################################
    # # Lots of parenting and organization!
    # # Create module group organization
    # spineModuleGrp = cmds.group(empty=True, name="%sspine_GRP" % fk_chain[0][:2])
    # spineJointsGrp = cmds.group(
    #     empty=True, name="%sspine_JOINTS_GRP" % fk_chain[0][:2], parent=spineModuleGrp
    # )
    # spineControlsGrp = cmds.group(
    #     empty=True, name="%sspine_CONTROLS_GRP" % fk_chain[0][:2], parent=spineModuleGrp
    # )
    # spineGutsGrp = cmds.group(
    #     empty=True, name="%sspine_GUTS_GRP" % fk_chain[0][:2], parent=spineModuleGrp
    # )
    # # Parent the chest control offset under end FK joint
    # cmds.parent(chestOffset, fk_chain[-1])
    # # Parent the FK control hierarchy under the start FK joint
    # cmds.parent(fkCtrlGrps[0], fk_chain[0])
    # # Parent the start FK joint under the root control
    # cmds.parent(fk_chain[0], root_ctrl)
    # # Parent the pelvis offset under the root control
    # cmds.parent(pelvisOffset, root_ctrl)
    # # Parent Ik handle and ik handle curve under guts
    # cmds.parent(spineIKH, spineIkCrv, spineGutsGrp)
    # # Parent root offset group under controls
    # cmds.parent(root_ctrl_offset, spineControlsGrp)
    # # Parent Ik joint chain under joints
    # cmds.parent(ik_chain[0], spineJointsGrp)

    # """


# Based on Fabio's class, this is the following twist joint settings. As I build my own skeletons from scratch, I would ideally
# want to set up proper joint orientations for animation purposes i.e. root control translate Z+ makes character go forward in space.
# Also I want my rotate orders to be zxy all around and joint orientations should be x-y-z; x down the bone
# Enable twist controls on ik handle with following setup:
# 	1. World up type = Object rotation up (start/end)
# 	2. Forward axis = X+
# 	3. Up Axis = Z+
# 	4. Up vector = 0,0,1
# 	5. Up vector 2 = 0,0,1
# 	6. World up object = pelvis FK ctrl
# 	7. World up object 2 = chest FK ctrl
# 	8. Twist value type = start/end
# """
# # Setting a bunch of attributes
# cmds.setAttr(spineIKH + ".dTwistControlEnable", True)
# cmds.setAttr(spineIKH + ".dWorldUpType", 4)
# cmds.setAttr(spineIKH + ".dForwardAxis", 0)
# cmds.setAttr(spineIKH + ".dWorldUpAxis", 3)

# cmds.setAttr(spineIKH + ".dWorldUpVectorX", 0)
# cmds.setAttr(spineIKH + ".dWorldUpVectorY", 0)
# cmds.setAttr(spineIKH + ".dWorldUpVectorZ", 1)

# cmds.setAttr(spineIKH + ".dWorldUpVectorEndX", 0)
# cmds.setAttr(spineIKH + ".dWorldUpVectorEndY", 0)
# cmds.setAttr(spineIKH + ".dWorldUpVectorEndZ", 1)
# # Since there is not setAttr for the textfields for worldUpObjects, you need to do the following connection
# cmds.connectAttr(
#     pelvisCtrl + ".worldMatrix[0]", spineIKH + ".dWorldUpMatrix", force=True
# )
# cmds.connectAttr(
#     chestCtrl + ".worldMatrix[0]", spineIKH + ".dWorldUpMatrixEnd", force=True
# )

# cmds.setAttr(spineIKH + ".dTwistValueType", 1)

# #################################################################################
# # Parent and orient constrain the rig joints to the bind joints
# rigJnts = vutil.getJointHierarchy(start_joint, end_joint)
# r = 0
# for jnt in rigJnts:
#     cmds.parentConstraint(ik_chain[r], jnt, maintainOffset=True)
#     cmds.scaleConstraint(ik_chain[r], jnt, maintainOffset=True)
#     r += 1

# # Final lock and hide controller attributes
# transAttrs = [".tx", ".ty", ".tz"]
# rotateAttrs = [".rx", ".ry", ".rz"]
# scaleAttrs = [".sx", ".sy", ".sz"]
# visAttrs = [".v"]

# # Root ctrl
# vutil.lockAndHideAttrs(root_ctrl, scaleAttrs)
# vutil.lockAndHideAttrs(root_ctrl, visAttrs)
# # Pelvis ctrl
# vutil.lockAndHideAttrs(pelvisCtrl, scaleAttrs)
# vutil.lockAndHideAttrs(pelvisCtrl, visAttrs)
# # Chest ctrl
# vutil.lockAndHideAttrs(chestCtrl, scaleAttrs)
# vutil.lockAndHideAttrs(chestCtrl, visAttrs)
# # Spine ctrls
# for ctrl in fkCtrls:
#     vutil.lockAndHideAttrs(ctrl, transAttrs)
#     vutil.lockAndHideAttrs(ctrl, scaleAttrs)
#     vutil.lockAndHideAttrs(ctrl, visAttrs)
