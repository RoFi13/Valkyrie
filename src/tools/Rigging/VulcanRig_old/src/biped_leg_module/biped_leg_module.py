"""Biped Leg Module."""

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


def createBipedLeg(lineStartJnt, lineEndJnt):
    """
    Creates the Biped Leg module control rig.
    """
    #################################################################################
    # Check to make sure the reverse foot pivots are created in the scene
    tempFootLocs = [
        "temp_heelReverse_LOC",
        "temp_toeReverse_LOC",
        "temp_ballReverse_LOC",
        "temp_toeBallReverse_LOC",
    ]
    for temp in tempFootLocs:
        if not cmds.objExists(temp):
            cmds.error(
                "You are missing "
                + temp
                + " for your reverse leg setup. Please create the locators with the Place Foot Pivots button."
            )

    # Open Undo chunk
    cmds.undoInfo(chunkName="bipedLegModule_chunk", openChunk=True)
    # Get start and end joint from UI
    startJnt = lineStartJnt.text()
    endJnt = lineEndJnt.text()

    # Get side of body prefix and color choice for controls
    sidePrefix = startJnt[:2]
    if sidePrefix == "L_":
        # Color is Blue
        ctrlColor = str(6)
    elif sidePrefix == "R_":
        ctrlColor = str(13)

    #################################################################################
    # Duplicate joint chain from start to end joint twice; rename one to IK and the other to FK
    # Duplicate leg hierarchy and rename
    dupClavJnts = vutil.dupJointChain(startJnt, endJnt)
    bindChain = []
    for jnt in dupClavJnts:
        splitName = jnt.split("_JNT")[0]
        print(splitName)
        bindChain.append(cmds.rename(jnt, splitName + "Bind_JNT"))

    # Duplicate leg hierarchy for IK joints and rename
    dupIkJnts = vutil.dupJointChain(startJnt, endJnt)
    ikChain = []
    for jnt in dupIkJnts:
        splitName = jnt.split("_JNT")[0]
        ikChain.append(cmds.rename(jnt, splitName + "IK_JNT"))

    # Duplicate leg hierarchy for FK joints and rename
    dupFkJnts = vutil.dupJointChain(startJnt, endJnt)
    fkChain = []
    for jnt in dupFkJnts:
        splitName = jnt.split("_JNT")[0]
        fkChain.append(cmds.rename(jnt, splitName + "FK_JNT"))

    #################################################################################
    # Create IKFK switch Control and create blend constraints and nodes
    ikFkSwitchOffset = rc.createIKFKBlendCtrl(sidePrefix, "leg")
    # Snap IKFK switch control to leg joint and zero out rotations
    cmds.delete(
        cmds.pointConstraint(bindChain[0], ikFkSwitchOffset, maintainOffset=False)
    )
    # Get IKFK switch control
    ikFkSwitch = cmds.listRelatives(ikFkSwitchOffset, children=True)[0]
    cmds.select(ikFkSwitch, replace=True)
    draw.changeColor(ctrlColor)
    # Add custom IKFK switch attribute to control
    cmds.addAttr(
        ikFkSwitch,
        longName="IKFK",
        attributeType="float",
        min=0,
        max=10,
        defaultValue=0,
    )
    cmds.setAttr(ikFkSwitch + ".IKFK", edit=1, keyable=True)

    # Create orient constraints for all chains
    orientConList = []
    for i in range(len(bindChain)):
        orientCon = cmds.orientConstraint(
            ikChain[i], fkChain[i], bindChain[i], maintainOffset=True
        )
        orientConList.append(orientCon[0])
        cmds.setAttr(orientCon[0] + ".interpType", 2)

    # Create multiply divide node and reverse nodes for space switching
    multiDNode = cmds.createNode(
        "multiplyDivide", name=(bindChain[0].split("Bind_JNT")[0] + "Switch_MLT")
    )
    reverseNode = cmds.createNode(
        "reverse", name=(bindChain[0].split("Bind_JNT")[0] + "Switch_RVS")
    )
    cmds.setAttr(multiDNode + ".input2X", 0.1)
    cmds.connectAttr(ikFkSwitch + ".IKFK", multiDNode + ".input1X")
    cmds.connectAttr(multiDNode + ".outputX", reverseNode + ".inputX")

    # Connect multiply divide and reverse nodes with the constraints
    for i in range(len(orientConList)):
        cmds.connectAttr(
            "%s.outputX" % multiDNode, "%s.%sW1" % (orientConList[i], fkChain[i])
        )
        cmds.connectAttr(
            "%s.outputX" % reverseNode, "%s.%sW0" % (orientConList[i], ikChain[i])
        )

    #################################################################################
    # Create FK chain nurbs controls
    fkCtrlGrps = []
    fkCtrls = []
    for jnt in fkChain[:-1]:
        # Create circle controls and snap to joint locations and orientations for offset nodes
        ctrl = rc.createCircleCtrl(jnt.split("_JNT")[0] + "_CTL")
        cmds.select(ctrl, replace=True)
        draw.changeColor(ctrlColor)
        ctrlGrp = cmds.group(ctrl, name=ctrl.split("_CTL")[0] + "Offset_GRP")
        cmds.delete(cmds.parentConstraint(jnt, ctrlGrp, maintainOffset=False))
        # Append new nodes to list
        fkCtrlGrps.append(ctrlGrp)
        fkCtrls.append(ctrl)
        if not "leg" in ctrl:
            # Orient constrain FK joints to FK controls
            cmds.orientConstraint(ctrl, jnt, maintainOffset=False)
        else:
            # Parent constraint for FK leg joint to controller since I'm not using different space switches for FK legs
            cmds.parentConstraint(ctrl, jnt, maintainOffset=False)

    # Point constrain switch offset to the FK control
    cmds.pointConstraint(fkCtrlGrps[0], ikFkSwitchOffset, maintainOffset=True)

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
    # Create Ik foot control with offset
    for jnt in ikChain:
        if "foot" in jnt:
            ikFootJnt = jnt
        elif "toeIK" in jnt:
            ikToeJnt = jnt
        elif "End" in jnt:
            ikToeEndJnt = jnt

    ikCtrl = rc.createCubeCtrl(ikFootJnt.replace("_JNT", "_CTL"))
    cmds.select(ikCtrl, replace=True)
    draw.changeColor(ctrlColor)
    ikCtrlOffset = cmds.group(ikCtrl, name=ikCtrl.split("_CTL")[0] + "Offset_GRP")
    cmds.delete(cmds.parentConstraint(ikFootJnt, ikCtrlOffset, maintainOffset=False))
    # Orient IK foot offset group to the world
    # cmds.setAttr(ikCtrlOffset + ".rx", 0)
    # cmds.setAttr(ikCtrlOffset + ".ry", 0)
    # cmds.setAttr(ikCtrlOffset + ".rz", 0)

    # Create Ik Handle and parent under control
    footHandle = cmds.ikHandle(
        startJoint=ikChain[0],
        endEffector=ikFootJnt,
        priority=1,
        solver="ikRPsolver",
        setupForRPsolver=True,
    )
    footIKH = cmds.rename(footHandle[0], "%sfoot_IKH" % sidePrefix)
    # Create Pole Vector; first create triangle geo at each of the joints world space locations
    legPoint = cmds.xform(ikChain[0], query=True, translation=True, worldSpace=True)
    kneePoint = cmds.xform(ikChain[1], query=True, translation=True, worldSpace=True)
    footPoint = cmds.xform(ikFootJnt, query=True, translation=True, worldSpace=True)
    legPlane = cmds.polyCreateFacet(
        constructionHistory=False,
        point=[
            (legPoint[0], legPoint[1], legPoint[2]),
            (kneePoint[0], kneePoint[1], kneePoint[2]),
            (footPoint[0], footPoint[1], footPoint[2]),
        ],
    )
    # Select first and last verteces on new geo and create a locator at center between them
    cmds.select(legPlane[0] + ".vtx[0]", legPlane[0] + ".vtx[2]", replace=True)
    vertexSel = cmds.ls(selection=True)
    pvLoc = vutil.createLocAtCenter(vertexSel)[0]
    # Aim constrain new locator towards wrist with up vector pointing towards elbow
    cmds.delete(
        cmds.aimConstraint(
            ikFootJnt,
            pvLoc,
            aimVector=(1, 0, 0),
            upVector=(0, 1, 0),
            worldUpType="object",
            worldUpObject=ikChain[1],
            maintainOffset=False,
        )
    )
    # Move pole vector locator behind elbow
    cmds.move(
        0, 100, 0, pvLoc, relative=True, objectSpace=True, worldSpaceDistance=False
    )
    # Create Pole vector control and snap to temp locator
    pvCtrl = rc.createSphereCtrl("%slegPV_CTL" % sidePrefix)
    cmds.select(pvCtrl, replace=True)
    draw.changeColor(ctrlColor)
    pvCtrlOffset = cmds.group(pvCtrl, name=pvCtrl.replace("_CTL", "Offset_GRP"))
    cmds.delete(cmds.pointConstraint(pvLoc, pvCtrlOffset, maintainOffset=False))
    cmds.poleVectorConstraint(pvCtrl, footIKH, weight=1)
    # Cleanup
    cmds.delete(pvLoc, legPlane)

    #################################################################################
    # Create reverse foot setup
    # Create single chain Ik handle from ankle/foot to toe; then create another single chain Ik hanld from toe to toe end joint
    ballHandle = cmds.ikHandle(
        startJoint=ikFootJnt,
        endEffector=ikToeJnt,
        priority=1,
        solver="ikSCsolver",
        setupForRPsolver=False,
    )
    ballIKH = cmds.rename(ballHandle[0], "%sball_IKH" % sidePrefix)
    toeHandle = cmds.ikHandle(
        startJoint=ikToeJnt,
        endEffector=ikToeEndJnt,
        priority=1,
        solver="ikSCsolver",
        setupForRPsolver=False,
    )
    toeIKH = cmds.rename(toeHandle[0], "%stoe_IKH" % sidePrefix)

    # Recreate temp pivot locators with new locators that have offsets
    footLocs = []
    footLocOffsets = []
    for loc in tempFootLocs:
        newLoc = cmds.spaceLocator(name=loc.replace("temp_", sidePrefix))[0]
        locOffset = cmds.group(
            newLoc, world=True, name=newLoc.replace("_LOC", "Offset_GRP")
        )
        # Move offset into position of temp locs transforms
        cmds.delete(cmds.parentConstraint(loc, locOffset, maintainOffset=False))
        # Append new locators and offsets to list
        footLocs.append(newLoc)
        footLocOffsets.append(locOffset)

    # Parent foot Ik handle and ball ik handle under ballreverse_LOC
    cmds.parent(footIKH, ballIKH, footLocs[2])
    # Parent toe ik handle under toeBallReverse_LOC
    cmds.parent(toeIKH, footLocs[-1])
    # Parent ballReverse and toeBallReverse offsets under toeReverse_LOC
    cmds.parent(footLocOffsets[2], footLocOffsets[-1], footLocs[1])
    # Parent toeReverse offset under the heelReverse_LOC
    cmds.parent(footLocOffsets[1], footLocs[0])
    # Parent heelReverse offset under the footIk control
    cmds.parent(footLocOffsets[0], ikCtrl)

    # Create custom foot attributes on ik foot control
    footAttr = [
        "ballRoll",
        "heelStand",
        "heelPivot",
        "toeUpDown",
        "toeStand",
        "toePivot",
        "toeLeftRight",
        "ballLeftRight",
    ]
    for attr in footAttr:
        cmds.addAttr(ikCtrl, longName=attr, attributeType="float", defaultValue=0)
        cmds.setAttr(ikCtrl + "." + attr, edit=True, keyable=True)
    # Connect ik custom attributes to the foot locators rotations
    cmds.connectAttr(ikCtrl + ".heelStand", footLocs[0] + ".rotateX")
    cmds.connectAttr(ikCtrl + ".heelPivot", footLocs[0] + ".rotateY")
    cmds.connectAttr(ikCtrl + ".toeStand", footLocs[1] + ".rotateX")
    cmds.connectAttr(ikCtrl + ".ballRoll", footLocs[2] + ".rotateZ")
    cmds.connectAttr(ikCtrl + ".toeUpDown", footLocs[-1] + ".rotateZ")
    cmds.connectAttr(ikCtrl + ".toeLeftRight", footLocs[-1] + ".rotateY")
    cmds.connectAttr(ikCtrl + ".ballLeftRight", footLocs[2] + ".rotateY")
    cmds.connectAttr(ikCtrl + ".toePivot", footLocs[1] + ".rotateY")
    """
	NOTE FOR FUTURE ROB!!!
	If you orient the joints with XYZ orientation, then the above connections will make the custom attributes be negative values when
		being adjusted by the animator. So possibly you can add a reverse node for the certain attributes that make sense for animators.
	"""

    # Add visibility switches to FK and IK controls
    cmds.connectAttr(reverseNode + ".outputX", ikCtrlOffset + ".visibility")
    cmds.connectAttr(reverseNode + ".outputX", pvCtrlOffset + ".visibility")
    cmds.connectAttr(multiDNode + ".outputX", fkCtrlGrps[0] + ".visibility")
    # Hide other locators and ik handles
    cmds.setAttr(footIKH + ".visibility", 0)
    cmds.setAttr(ballIKH + ".visibility", 0)
    cmds.setAttr(toeIKH + ".visibility", 0)
    for loc in footLocs:
        cmds.setAttr(loc + ".visibility", 0)

    # Create module group organization
    legModuleGrp = cmds.group(empty=True, name="%sleg_GRP" % fkChain[0][:2])
    legJointsGrp = cmds.group(
        empty=True, name="%sleg_JOINTS_GRP" % fkChain[0][:2], parent=legModuleGrp
    )
    legControlsGrp = cmds.group(
        empty=True, name="%sleg_CONTROLS_GRP" % fkChain[0][:2], parent=legModuleGrp
    )
    legGutsGrp = cmds.group(
        empty=True, name="%sleg_GUTS_GRP" % fkChain[0][:2], parent=legModuleGrp
    )

    # Parenting rig control hierarchies under module groups
    cmds.parent(bindChain[0], ikChain[0], fkChain[0], legJointsGrp)
    cmds.parent(
        ikFkSwitchOffset, fkCtrlGrps[0], pvCtrlOffset, ikCtrlOffset, legControlsGrp
    )

    # Cleanup temp locators
    cmds.delete(tempFootLocs)

    #################################################################################
    # Attach rig joints to control rig bind joints with parent and scale constraints
    # Get rig joints from skeleton
    rigJnts = vutil.getJointHierarchy(startJnt, endJnt)
    r = 0
    for jnt in rigJnts:
        cmds.parentConstraint(bindChain[r], jnt, maintainOffset=True)
        cmds.scaleConstraint(bindChain[r], jnt, maintainOffset=True)
        r += 1

    # Final lock and hide controller attributes
    transAttrs = [".tx", ".ty", ".tz"]
    rotateAttrs = [".rx", ".ry", ".rz"]
    scaleAttrs = [".sx", ".sy", ".sz"]
    visAttrs = [".v"]

    # Ik foot ctrl
    vutil.lockAndHideAttrs(ikCtrl, scaleAttrs)
    vutil.lockAndHideAttrs(ikCtrl, visAttrs)
    # Pole vector ctrl
    vutil.lockAndHideAttrs(pvCtrl, rotateAttrs)
    vutil.lockAndHideAttrs(pvCtrl, scaleAttrs)
    vutil.lockAndHideAttrs(pvCtrl, visAttrs)
    # IKFK switch ctrl
    vutil.lockAndHideAttrs(ikFkSwitch, transAttrs)
    vutil.lockAndHideAttrs(ikFkSwitch, rotateAttrs)
    vutil.lockAndHideAttrs(ikFkSwitch, scaleAttrs)
    vutil.lockAndHideAttrs(ikFkSwitch, visAttrs)
    # FK ctrls
    for ctrl in fkCtrls:
        vutil.lockAndHideAttrs(ctrl, transAttrs)
        vutil.lockAndHideAttrs(ctrl, scaleAttrs)
        vutil.lockAndHideAttrs(ctrl, visAttrs)

    # Close Undo chunk
    cmds.undoInfo(chunkName="bipedLegModule_chunk", closeChunk=True)
    print("Biped Leg Module is created.")


###############################################################################################################################
###############################################################################################################################
def placeFootPivots():
    """
    Creates four temp locators for user to place where they want the pivots of the foot to be
    """
    tempFootLocs = [
        "temp_heelReverse_LOC",
        "temp_toeReverse_LOC",
        "temp_ballReverse_LOC",
        "temp_toeBallReverse_LOC",
    ]
    for loc in tempFootLocs:
        if not cmds.objExists(loc):
            cmds.spaceLocator(name=loc)
