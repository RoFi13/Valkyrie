"""Neck and Head Module."""

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


def createNeckHeadMD(lineStartJnt, lineEndJnt):
    """
    Creates the neck and head module control rig. Simple FK chain. I don't think an IK head is necessary for animation.
    At least not for biped humanoids. Maybe for creatures.
    """
    #################################################################################
    # Open Undo chunk
    cmds.undoInfo(chunkName="neckHeadModule_chunk", openChunk=True)
    # Get start and end joint from UI
    startJnt = lineStartJnt.text()
    endJnt = lineEndJnt.text()
    #################################################################################
    # Duplicate arm hierarchy for FK joints and rename
    dupFkJnts = vutil.dupJointChain(startJnt, endJnt)
    fkChain = []
    for jnt in dupFkJnts:
        splitName = jnt.split("_JNT")[0]
        fkChain.append(cmds.rename(jnt, splitName + "FKBind_JNT"))
    #################################################################################
    # Create FK controls for each FK neck joint
    fkCtrlGrps = []
    fkCtrls = []
    for jnt in fkChain:
        # Create circle controls and snap to joint locations and orientations for offset nodes
        ctrl = rc.createSquareCtrl(jnt.replace("Bind_JNT", "_CTL"))
        cmds.select(ctrl, replace=True)
        draw.changeColor("17")
        ctrlGrp = cmds.group(ctrl, name=ctrl.replace("_CTL", "Offset_GRP"))
        cmds.delete(cmds.parentConstraint(jnt, ctrlGrp, maintainOffset=False))
        # Append new nodes to list
        fkCtrlGrps.append(ctrlGrp)
        fkCtrls.append(ctrl)
        if not fkChain[0] in jnt:
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
    # Lots of parenting and organization!
    # Create module group organization
    neckHeadModuleGrp = cmds.group(empty=True, name="%sneckHead_GRP" % fkChain[0][:2])
    neckHeadJointsGrp = cmds.group(
        empty=True,
        name="%sneckHead_JOINTS_GRP" % fkChain[0][:2],
        parent=neckHeadModuleGrp,
    )
    neckHeadControlsGrp = cmds.group(
        empty=True,
        name="%sneckHead_CONTROLS_GRP" % fkChain[0][:2],
        parent=neckHeadModuleGrp,
    )
    neckHeadGutsGrp = cmds.group(
        empty=True,
        name="%sneckHead_GUTS_GRP" % fkChain[0][:2],
        parent=neckHeadModuleGrp,
    )
    # Parent the FK control hierarchy under the controls group
    cmds.parent(fkCtrlGrps[0], neckHeadControlsGrp)
    # Parent Ik joint chain under joints
    cmds.parent(fkChain[0], neckHeadJointsGrp)

    #################################################################################
    # Parent and orient constrain the rig joints to the bind joints
    rigJnts = vutil.getJointHierarchy(startJnt, endJnt)
    r = 0
    for jnt in rigJnts:
        cmds.parentConstraint(fkChain[r], jnt, maintainOffset=True)
        cmds.scaleConstraint(fkChain[r], jnt, maintainOffset=True)
        r += 1

    # Final lock and hide controller attributes
    transAttrs = [".tx", ".ty", ".tz"]
    rotateAttrs = [".rx", ".ry", ".rz"]
    scaleAttrs = [".sx", ".sy", ".sz"]
    visAttrs = [".v"]

    # FK ctrls
    for ctrl in fkCtrls:
        vutil.lockAndHideAttrs(ctrl, transAttrs)
        vutil.lockAndHideAttrs(ctrl, scaleAttrs)
        vutil.lockAndHideAttrs(ctrl, visAttrs)

    # Close Undo chunk
    cmds.undoInfo(chunkName="neckHeadModule_chunk", closeChunk=True)
    print("Neck/Head Module is created.")


###############################################################################################################################
###############################################################################################################################
