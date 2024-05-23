"""Hand Module."""

try:
    reload  # Python 2.7
except NameError:
    try:
        from importlib import reload  # Python 3.4+
    except ImportError:
        from imp import reload  # Python 3.0 - 3.3

import os

import maya.cmds as cmds

from ..util import rig_controls as rc

reload(rc)
from ..util import vulcan_utils as vutil

reload(vutil)
from ..util import draw_override as draw

reload(draw)


def createHandModule():
    cmds.undoInfo(chunkName="handModule_chunk", openChunk=True)
    # Get selected wrist joint
    wristJnt = cmds.ls(selection=True)[0]

    # Get all finger joints
    allFingerJnts = cmds.listRelatives(wristJnt, allDescendents=True, type="joint")

    # Get side of body prefix and color choice for controls
    sidePrefix = wristJnt[:2]
    if sidePrefix == "L_":
        # Color is Blue
        ctrlColor = str(6)
    elif sidePrefix == "R_":
        ctrlColor = str(13)

    # Duplicate entire hand and finger hierarchy and rename with Bind
    dupJnts = cmds.duplicate(wristJnt, renameChildren=True)
    cmds.parent(dupJnts[0], world=True)
    handJnt = cmds.rename(wristJnt, "%shandBind_JNT" % sidePrefix)
    # Cleanup duplicate hierarchy for any constrainsts
    onlyDupJnts = []
    for item in dupJnts:
        if (
            not cmds.objectType(item, isType="parentConstraint")
            and not cmds.objectType(item, isType="scaleConstraint")
            and not cmds.objectType(item, isType="orientConstraint")
        ):
            onlyDupJnts.append(item)
        else:
            cmds.delete(item)

    # Rename duplicated bind joints
    bindJnts = []
    for jnt in onlyDupJnts:
        splitName = jnt.split("_JNT")[0]
        bindJnts.append(cmds.rename(jnt, splitName + "Bind_JNT"))

    #################################################################################
    # Create FK chain nurbs controls
    fkCtrlGrps = []
    fkCtrls = []
    for jnt in bindJnts:
        if not "End" in jnt and not "wrist" in jnt:
            # Create circle controls and snap to joint locations and orientations for offset nodes
            ctrl = rc.createCircleCtrl(jnt.split("_JNT")[0] + "_CTL")
            cmds.select(ctrl, replace=True)
            draw.changeColor(ctrlColor)
            ctrlGrp = cmds.group(ctrl, name=ctrl.split("_CTL")[0] + "Offset_GRP")
            cmds.delete(cmds.parentConstraint(jnt, ctrlGrp, maintainOffset=False))
            # Append new nodes to list
            fkCtrlGrps.append(ctrlGrp)
            fkCtrls.append(ctrl)

            # Parent constraint bind joints to
            cmds.parentConstraint(ctrl, jnt, maintainOffset=False)

    # Sort control groups into alphabetical order to make parenting more reliable
    fkCtrls.sort()
    fkCtrlGrps.sort()

    #################################################################################
    # Parent FK hierarchy
    # Index fingers
    cmds.parent(fkCtrlGrps[2], fkCtrls[1])
    cmds.parent(fkCtrlGrps[1], fkCtrls[0])
    # Middle fingers
    cmds.parent(fkCtrlGrps[5], fkCtrls[4])
    cmds.parent(fkCtrlGrps[4], fkCtrls[3])
    # Pinky fingers
    cmds.parent(fkCtrlGrps[8], fkCtrls[7])
    cmds.parent(fkCtrlGrps[7], fkCtrls[6])
    # Ring fingers
    cmds.parent(fkCtrlGrps[11], fkCtrls[10])
    cmds.parent(fkCtrlGrps[10], fkCtrls[9])
    # Thumb fingers
    cmds.parent(fkCtrlGrps[14], fkCtrls[13])
    cmds.parent(fkCtrlGrps[13], fkCtrls[12])

    #################################################################################
    # Parent constrain all top FK control offsets to the original wrist joint
    cmds.parentConstraint(handJnt, fkCtrlGrps[0], maintainOffset=True)
    cmds.parentConstraint(handJnt, fkCtrlGrps[3], maintainOffset=True)
    cmds.parentConstraint(handJnt, fkCtrlGrps[6], maintainOffset=True)
    cmds.parentConstraint(handJnt, fkCtrlGrps[9], maintainOffset=True)
    cmds.parentConstraint(handJnt, fkCtrlGrps[12], maintainOffset=True)

    # Parent constrain the wrist bind joint to both the FK and IK wrist controls
    parConSwitch = cmds.parentConstraint(
        "%swristFK_CTL" % sidePrefix,
        "%swristIK_CTL" % sidePrefix,
        handJnt,
        maintainOffset=True,
    )[0]
    # Connect the constraint to the IKFK switch nodes for proper switching
    allConns = cmds.listConnections("%sarmSwitch_CTL" % sidePrefix)
    for conn in allConns:
        if "Switch_MLT" in conn:
            multiDNode = conn

    multConns = cmds.listConnections(multiDNode)
    for conn in multConns:
        if "Switch_RVS" in conn:
            reverseNode = conn

    # Get existing constraint attributes
    allParConns = cmds.listAttr(parConSwitch, keyable=True)
    conAttr = []
    for con in allParConns:
        if "W" in con:
            if "wristFK_CTL" in con:
                wristFKAttr = parConSwitch + "." + con
            elif "wristIK_CTL" in con:
                wristIKAttr = parConSwitch + "." + con

    # Connect the utility nodes to the constraint's attributes for switching between fk and ik control
    cmds.connectAttr("%s.outputX" % multiDNode, wristFKAttr, force=True)
    cmds.connectAttr("%s.outputX" % reverseNode, wristIKAttr, force=True)

    # cmds.connectAttr("%s.outputX" % multiDNode, "%s.%s%sW0" % (parConSwitch, sidePrefix, "wristFK_CTL"), force=True)
    # cmds.connectAttr("%s.outputX" % reverseNode, "%s.%s%sW1" % (parConSwitch, sidePrefix, "wristIK_CTL"), force=True)

    #################################################################################
    # Organize Nodes
    handModuleGrp = cmds.group(empty=True, name="%shand_GRP" % sidePrefix)
    handJointsGrp = cmds.group(
        empty=True, name="%shand_JOINTS_GRP" % sidePrefix, parent=handModuleGrp
    )
    handControlsGrp = cmds.group(
        empty=True, name="%shand_CONTROLS_GRP" % sidePrefix, parent=handModuleGrp
    )
    handGutsGrp = cmds.group(
        empty=True, name="%shand_GUTS_GRP" % sidePrefix, parent=handModuleGrp
    )
    # Parent control offsets and guts in module groups
    # cmds.parent(handJnt, handJointsGrp)
    cmds.parent(fkCtrlGrps[0], handControlsGrp)
    cmds.parent(fkCtrlGrps[3], handControlsGrp)
    cmds.parent(fkCtrlGrps[6], handControlsGrp)
    cmds.parent(fkCtrlGrps[9], handControlsGrp)
    cmds.parent(fkCtrlGrps[12], handControlsGrp)

    #################################################################################
    # Parent and scale constrain all bind joints to rig joints
    for jnt in allFingerJnts:
        bindJntName = jnt.replace("_JNT", "Bind_JNT")
        cmds.parentConstraint(bindJntName, jnt, maintainOffset=False)
        cmds.scaleConstraint(bindJntName, jnt, maintainOffset=True)

    # Delete duplicated bind joints; no longer needed
    cmds.delete(bindJnts)

    # Cleanup for control attribute locking
    # FK ctrls
    transAttrs = [".tx", ".ty", ".tz"]
    scaleAttrs = [".sx", ".sy", ".sz"]
    visAttrs = [".v"]
    for ctrl in fkCtrls:
        vutil.lockAndHideAttrs(ctrl, transAttrs)
        vutil.lockAndHideAttrs(ctrl, scaleAttrs)
        vutil.lockAndHideAttrs(ctrl, visAttrs)

    cmds.undoInfo(chunkName="handModule_chunk", closeChunk=True)
