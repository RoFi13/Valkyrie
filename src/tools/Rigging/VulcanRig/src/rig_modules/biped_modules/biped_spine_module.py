# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""Spine Rig Module."""

import ast
import logging
import os

from maya import cmds

from Core import core_paths as cpath
from Core.ui.UIUtilTools.src import pyside_util_tools as put

from Util.UtilTools.src import maya_pyside_interface as mpi

from .. import module_product_factories

from Rigging.VulcanRig.src.data.ue_skeleton_names import EpicBasicSkeleton
from Rigging.VulcanRig.src.data import module_metadata
from Rigging.VulcanRig.src.util import vulcan_utils as vutil

from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTreeWidget,
    QVBoxLayout,
)

from importlib import reload

reload(module_product_factories)
reload(vutil)
reload(put)
reload(mpi)
reload(module_metadata)

# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 2)}"

LOG = logging.getLogger(os.path.basename(__file__))


class BipedSpineModule(module_product_factories.ModuleProductFactory):
    def __init__(
        self,
        vulcan_window: QMainWindow,
        module_name: str = "",
        parent_module: module_product_factories.ModuleProductFactory = None,
    ):
        super().__init__(vulcan_window)

        self._current_metadata = module_metadata.BipedSpineConfig(
            module_name=module_name
        )
        self.hbox_start_joint: QHBoxLayout
        self.lbl_start_joint: QLabel
        self.txt_start_joint: QLineEdit
        self.btn_grab_start_joint: QPushButton
        self.hbox_end_joint: QHBoxLayout
        self.lbl_end_joint: QLabel
        self.txt_end_joint: QLineEdit
        self.btn_grab_end_joint: QPushButton

    def get_metanode_metadata(self):
        """Get the metanode's metadata.

        Returns:
            ModuleConfig: Dataclass module's metadata.
        """
        metadata_dict = ast.literal_eval(
            cmds.getAttr(
                f"{self._current_metadata.metanode}."
                f"{module_metadata.MetadataAttributes.MODULE_META_ATTRIBUTE.value}"
            )
        )
        return module_metadata.BipedSpineConfig(**metadata_dict)

    def build_proxy(self):
        cmds.undoInfo(chunkName="ProxyBipedSpineModule_chunk", openChunk=True)

        cmds.undoInfo(chunkName="ProxyBipedSpineModule_chunk", closeChunk=True)

    def build_module(self):
        cmds.undoInfo(chunkName="BuildBipedSpineModule_chunk", openChunk=True)

        cmds.undoInfo(chunkName="BuildBipedSpineModule_chunk", closeChunk=True)

    def build_details_panel(self):
        put.clear_box_layout(self._vulcan_window.root.vb_details)

        metadata = self.get_module_metadata()

        # Build GUI elements for root module
        self.hbox_start_joint = QHBoxLayout()
        self.lbl_start_joint = QLabel("Start Joint:", self._vulcan_window)
        self.txt_start_joint = QLineEdit(self._vulcan_window)
        self.txt_start_joint.setEnabled(False)
        self.btn_grab_start_joint = QPushButton("Grab")

        self.hbox_start_joint.addWidget(self.lbl_start_joint)
        self.hbox_start_joint.addWidget(self.txt_start_joint)
        self.hbox_start_joint.addWidget(self.btn_grab_start_joint)

        self.hbox_end_joint = QHBoxLayout()
        self.lbl_end_joint = QLabel("End Joint:", self._vulcan_window)
        self.txt_end_joint = QLineEdit(self._vulcan_window)
        self.txt_end_joint.setEnabled(False)
        self.btn_grab_end_joint = QPushButton("Grab")

        self.hbox_end_joint.addWidget(self.lbl_end_joint)
        self.hbox_end_joint.addWidget(self.txt_end_joint)
        self.hbox_end_joint.addWidget(self.btn_grab_end_joint)

        bottom_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self._vulcan_window.root.vb_details.addLayout(self.hbox_start_joint)
        self._vulcan_window.root.vb_details.addLayout(self.hbox_end_joint)

        lbl_build_options = QLabel("Build Options")
        hline_build_options = put.create_line()

        self._vulcan_window.root.vb_details.addWidget(lbl_build_options)
        self._vulcan_window.root.vb_details.addWidget(hline_build_options)

        self._vulcan_window.root.vb_details.addItem(bottom_spacer)

        self.set_details_panel_defaults()
        # txt_asset_name.setText(metadata.asset_name)

        # Setup signals
        self.btn_grab_start_joint.clicked.connect(
            lambda: mpi.add_selection_to_textfield(self.txt_start_joint)
        )
        self.btn_grab_end_joint.clicked.connect(
            lambda: mpi.add_selection_to_textfield(self.txt_end_joint)
        )

    def set_details_panel_defaults(self):
        joints_placeholder_text = (
            "Click the Grab button to pick your selected Maya joint."
        )
        self.txt_start_joint.setPlaceholderText(joints_placeholder_text)
        self.txt_end_joint.setPlaceholderText(joints_placeholder_text)

        if cmds.objExists(EpicBasicSkeleton.SPINE_01.value):
            self.txt_start_joint.setText(EpicBasicSkeleton.SPINE_01.value)
        if cmds.objExists(EpicBasicSkeleton.SPINE_05.value):
            self.txt_end_joint.setText(EpicBasicSkeleton.SPINE_05.value)


def createSpineMD(lineStartJnt, lineEndJnt):
    """
    Creates the spine module control rig.
    """
    return
    #################################################################################
    # Open Undo chunk
    cmds.undoInfo(chunkName="spineModule_chunk", openChunk=True)
    # Get start and end joint from UI
    startJnt = lineStartJnt.text()
    endJnt = lineEndJnt.text()
    #################################################################################
    # Duplicate joint chain from start to end joint twice; rename one to IK and the other to FK
    # Duplicate arm hierarchy for IK joints and rename
    dupIkJnts = vutil.dupJointChain(startJnt, endJnt)
    ikChain = []
    for jnt in dupIkJnts:
        splitName = jnt.split("_JNT")[0]
        ikChain.append(cmds.rename(jnt, splitName + "IKBind_JNT"))

    # Duplicate arm hierarchy for FK joints and rename
    dupFkJnts = vutil.dupJointChain(startJnt, endJnt)
    fkChain = []
    for jnt in dupFkJnts:
        splitName = jnt.split("_JNT")[0]
        fkChain.append(cmds.rename(jnt, splitName + "FK_JNT"))
    #################################################################################
    # Create root controller with offset
    rootCtrl = rc.createSquareCtrl("C_root_CTL")
    rootCtrlOffset = cmds.group(rootCtrl, name=rootCtrl.replace("_CTL", "Offset_GRP"))
    cmds.select(rootCtrl, replace=True)
    # draw.changeColor("17")
    cmds.delete(cmds.parentConstraint(fkChain[0], rootCtrlOffset, maintainOffset=False))
    # Create FK controls for each FK spine joint
    fkCtrlGrps = []
    fkCtrls = []
    for jnt in fkChain[1:-1]:
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

    # Parent FK hierarchy
    # This basically just parents the offset group nodes to the control number right above it
    # i.e. offset04 -> ctrl03; offset03 -> ctrl02
    i = 0
    offsetNum = -1
    ctrlNum = -2
    while i <= 100:
        if not fkCtrlGrps[offsetNum] == fkCtrlGrps[1]:
            cmds.parent(fkCtrlGrps[offsetNum], fkCtrls[ctrlNum])
        else:
            cmds.parent(fkCtrlGrps[offsetNum], fkCtrls[ctrlNum])
            break
        offsetNum -= 1
        ctrlNum -= 1
        i += 1

    #################################################################################
    # Duplicate starting joint and last joint separately from the rest of the chain
    # Rename new start joint as C_pelvis_JNT and end joint as C_chest_JNT
    pelvisJnt = cmds.duplicate(startJnt, parentOnly=True, name="C_pelvis_JNT")
    chestJnt = cmds.duplicate(endJnt, parentOnly=True, name="C_chest_JNT")
    # Create controls for the pelvis and chest
    pelvisCtrl = rc.createPelvisCtrl("C_pelvis_CTL")
    pelvisOffset = cmds.group(pelvisCtrl, name=pelvisCtrl.replace("_CTL", "Offset_GRP"))
    cmds.delete(cmds.parentConstraint(pelvisJnt, pelvisOffset, maintainOffset=False))
    # Using the same type of modified nurbs controller for the chest as well. This is on purpose
    chestCtrl = rc.createPelvisCtrl("C_chest_CTL")
    chestOffset = cmds.group(chestCtrl, name=chestCtrl.replace("_CTL", "Offset_GRP"))
    cmds.delete(cmds.parentConstraint(chestJnt, chestOffset, maintainOffset=False))

    # Create Ik spline handle using the IK joint chain with following settings:
    # The following ikHandle command returns: [ikHandle1, effector1, curve1]
    spineHandle = cmds.ikHandle(
        startJoint=ikChain[0],
        endEffector=ikChain[-1],
        solver="ikSplineSolver",
        numSpans=4,
        parentCurve=False,
        simplifyCurve=True,
        createCurve=True,
        twistType="linear",
    )
    spineIKH = cmds.rename(spineHandle[0], "C_spineIK_IKH")
    spineIkCrv = cmds.rename(spineHandle[-1], "C_spineIK_CRV")
    # Parent the pelvis joint under pelvis control and chest joint under chest control
    cmds.parent(pelvisJnt, pelvisCtrl)
    cmds.parent(chestJnt, chestCtrl)
    # Select pelvis and chest joints and the IK handle curve and bind skin
    spineCluster = cmds.skinCluster(
        pelvisJnt,
        chestJnt,
        spineIkCrv,
        name="spineCRV_SKC",
        toSelectedBones=True,
        bindMethod=1,
        skinMethod=0,
        normalizeWeights=1,
        weightDistribution=0,
        maximumInfluences=3,
        obeyMaxInfluences=True,
        removeUnusedInfluence=True,
    )

    #################################################################################
    # Lots of parenting and organization!
    # Create module group organization
    spineModuleGrp = cmds.group(empty=True, name="%sspine_GRP" % fkChain[0][:2])
    spineJointsGrp = cmds.group(
        empty=True, name="%sspine_JOINTS_GRP" % fkChain[0][:2], parent=spineModuleGrp
    )
    spineControlsGrp = cmds.group(
        empty=True, name="%sspine_CONTROLS_GRP" % fkChain[0][:2], parent=spineModuleGrp
    )
    spineGutsGrp = cmds.group(
        empty=True, name="%sspine_GUTS_GRP" % fkChain[0][:2], parent=spineModuleGrp
    )
    # Parent the chest control offset under end FK joint
    cmds.parent(chestOffset, fkChain[-1])
    # Parent the FK control hierarchy under the start FK joint
    cmds.parent(fkCtrlGrps[0], fkChain[0])
    # Parent the start FK joint under the root control
    cmds.parent(fkChain[0], rootCtrl)
    # Parent the pelvis offset under the root control
    cmds.parent(pelvisOffset, rootCtrl)
    # Parent Ik handle and ik handle curve under guts
    cmds.parent(spineIKH, spineIkCrv, spineGutsGrp)
    # Parent root offset group under controls
    cmds.parent(rootCtrlOffset, spineControlsGrp)
    # Parent Ik joint chain under joints
    cmds.parent(ikChain[0], spineJointsGrp)

    """
	Based on Fabio's class, this is the following twist joint settings. As I build my own skeletons from scratch, I would ideally
	want to set up proper joint orientations for animation purposes i.e. root control translate Z+ makes character go forward in space.
	Also I want my rotate orders to be zxy all around and joint orientations should be x-y-z; x down the bone
	Enable twist controls on ik handle with following setup:
		1. World up type = Object rotation up (start/end)
		2. Forward axis = X+
		3. Up Axis = Z+
		4. Up vector = 0,0,1
		5. Up vector 2 = 0,0,1
		6. World up object = pelvis FK ctrl
		7. World up object 2 = chest FK ctrl
		8. Twist value type = start/end
	"""
    # Setting a bunch of attributes
    cmds.setAttr(spineIKH + ".dTwistControlEnable", True)
    cmds.setAttr(spineIKH + ".dWorldUpType", 4)
    cmds.setAttr(spineIKH + ".dForwardAxis", 0)
    cmds.setAttr(spineIKH + ".dWorldUpAxis", 3)

    cmds.setAttr(spineIKH + ".dWorldUpVectorX", 0)
    cmds.setAttr(spineIKH + ".dWorldUpVectorY", 0)
    cmds.setAttr(spineIKH + ".dWorldUpVectorZ", 1)

    cmds.setAttr(spineIKH + ".dWorldUpVectorEndX", 0)
    cmds.setAttr(spineIKH + ".dWorldUpVectorEndY", 0)
    cmds.setAttr(spineIKH + ".dWorldUpVectorEndZ", 1)
    # Since there is not setAttr for the textfields for worldUpObjects, you need to do the following connection
    cmds.connectAttr(
        pelvisCtrl + ".worldMatrix[0]", spineIKH + ".dWorldUpMatrix", force=True
    )
    cmds.connectAttr(
        chestCtrl + ".worldMatrix[0]", spineIKH + ".dWorldUpMatrixEnd", force=True
    )

    cmds.setAttr(spineIKH + ".dTwistValueType", 1)

    #################################################################################
    # Parent and orient constrain the rig joints to the bind joints
    rigJnts = vutil.getJointHierarchy(startJnt, endJnt)
    r = 0
    for jnt in rigJnts:
        cmds.parentConstraint(ikChain[r], jnt, maintainOffset=True)
        cmds.scaleConstraint(ikChain[r], jnt, maintainOffset=True)
        r += 1

    # Final lock and hide controller attributes
    transAttrs = [".tx", ".ty", ".tz"]
    rotateAttrs = [".rx", ".ry", ".rz"]
    scaleAttrs = [".sx", ".sy", ".sz"]
    visAttrs = [".v"]

    # Root ctrl
    vutil.lockAndHideAttrs(rootCtrl, scaleAttrs)
    vutil.lockAndHideAttrs(rootCtrl, visAttrs)
    # Pelvis ctrl
    vutil.lockAndHideAttrs(pelvisCtrl, scaleAttrs)
    vutil.lockAndHideAttrs(pelvisCtrl, visAttrs)
    # Chest ctrl
    vutil.lockAndHideAttrs(chestCtrl, scaleAttrs)
    vutil.lockAndHideAttrs(chestCtrl, visAttrs)
    # Spine ctrls
    for ctrl in fkCtrls:
        vutil.lockAndHideAttrs(ctrl, transAttrs)
        vutil.lockAndHideAttrs(ctrl, scaleAttrs)
        vutil.lockAndHideAttrs(ctrl, visAttrs)

    # Close Undo chunk
    cmds.undoInfo(chunkName="spineModule_chunk", closeChunk=True)
    print("Spine Module is created.")


###############################################################################################################################
###############################################################################################################################
