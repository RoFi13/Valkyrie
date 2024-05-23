"""Arm module"""

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


def createArmMD(clavJnt, shoulderJnt, wristJnt, CTLLIB):
    """
    Creates the arm module control rig.
    """
    #################################################################################
    # Open Undo chunk
    cmds.undoInfo(chunkName="armModule_chunk", openChunk=True)
    clavJntName = clavJnt.text()
    shoulderJntName = shoulderJnt.text()
    wristJntName = wristJnt.text()

    clavEndJnt = cmds.listRelatives(clavJntName, children=True, type="joint")[0]

    # Get side of body prefix and color choice for controls
    sidePrefix = clavJntName[:2]
    if sidePrefix == "L_":
        # Color is Blue
        ctrlColor = str(6)
    elif sidePrefix == "R_":
        ctrlColor = str(13)

    #################################################################################
    # Duplicate clavicle hierarchy and rename
    dupClavJnts = vutil.dupJointChain(clavJntName, "End")
    clavBindChain = []
    for jnt in dupClavJnts:
        splitName = jnt.split("_JNT")[0]
        clavBindChain.append(cmds.rename(jnt, splitName + "Bind_JNT"))

    # Duplicate shoulder hierarchy for bind joints
    cmds.select(clear=True)
    dupBindJnts = vutil.dupJointChain(shoulderJntName, wristJntName)
    bindChain = []
    print(dupBindJnts)
    for jnt in dupBindJnts:
        if "twist" in jnt or "Twist" in jnt:
            try:
                cmds.delete(jnt)
            except ValueError:
                pass
        else:
            splitName = jnt.split("_JNT")[0]
            print(splitName)

            newName = cmds.rename(jnt, splitName + "Bind_JNT")
            bindChain.append(newName)

    # Duplicate arm hierarchy for IK joints and rename
    dupIkJnts = vutil.dupJointChain(shoulderJntName, wristJntName)
    ikChain = []
    for jnt in dupIkJnts:
        if not "twist" in jnt and not "Twist" in jnt:
            splitName = jnt.split("_JNT")[0]
            ikChain.append(cmds.rename(jnt, splitName + "IK_JNT"))
        else:
            try:
                cmds.delete(jnt)
            except ValueError:
                pass

    # Duplicate arm hierarchy for FK joints and rename
    dupFkJnts = vutil.dupJointChain(shoulderJntName, wristJntName)
    fkChain = []
    for jnt in dupFkJnts:
        if not "twist" in jnt and not "Twist" in jnt:
            splitName = jnt.split("_JNT")[0]
            fkChain.append(cmds.rename(jnt, splitName + "FK_JNT"))
        else:
            try:
                cmds.delete(jnt)
            except ValueError:
                pass

    #################################################################################
    # Create IKFK switch Control and create blend constraints and nodes
    ikFkSwitchOffset = rc.createIKFKBlendCtrl(sidePrefix, "arm")
    # Snap IKFK switch control to shoulder joint and zero out rotations
    cmds.delete(
        cmds.pointConstraint(shoulderJntName, ikFkSwitchOffset, maintainOffset=False)
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
    for jnt in fkChain:
        # Create circle controls and snap to joint locations and orientations for offset nodes
        ctrl = rc.createCircleCtrl(jnt.split("_JNT")[0] + "_CTL")
        cmds.select(ctrl, replace=True)
        draw.changeColor(ctrlColor)
        ctrlGrp = cmds.group(ctrl, name=ctrl.split("_CTL")[0] + "Offset_GRP")
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

    # Parent FK controls hierarchy
    print(fkCtrlGrps)
    cmds.parent(fkCtrlGrps[2], fkCtrls[1])
    cmds.parent(fkCtrlGrps[1], fkCtrls[0])

    # Point constrain switch offset to the FK control
    cmds.pointConstraint(fkCtrlGrps[0], ikFkSwitchOffset, maintainOffset=True)

    #################################################################################
    # Create Ik controller and IK handle with Pole vector
    ikCtrl = rc.createCubeCtrl(ikChain[-1].split("_JNT")[0] + "_CTL")
    cmds.select(ikCtrl, replace=True)
    draw.changeColor(ctrlColor)
    ikCtrlOffset = cmds.group(ikCtrl, name=ikCtrl.split("_CTL")[0] + "Offset_GRP")
    cmds.delete(cmds.parentConstraint(ikChain[-1], ikCtrlOffset, maintainOffset=False))
    # Create Ik Handle and parent under control
    IKH = cmds.ikHandle(
        startJoint=ikChain[0],
        endEffector=ikChain[-1],
        priority=1,
        solver="ikRPsolver",
        setupForRPsolver=True,
    )[0]
    cmds.parent(IKH, ikCtrl)
    # Create Pole Vector; first create triangle geo at each of the joints world space locations
    shoulderPoint = cmds.xform(
        ikChain[0], query=True, translation=True, worldSpace=True
    )
    elbowPoint = cmds.xform(ikChain[1], query=True, translation=True, worldSpace=True)
    wristPoint = cmds.xform(ikChain[-1], query=True, translation=True, worldSpace=True)
    armPlane = cmds.polyCreateFacet(
        constructionHistory=False,
        point=[
            (shoulderPoint[0], shoulderPoint[1], shoulderPoint[2]),
            (elbowPoint[0], elbowPoint[1], elbowPoint[2]),
            (wristPoint[0], wristPoint[1], wristPoint[2]),
        ],
    )
    # Select first and last verteces on new geo and create a locator at center between them
    cmds.select(armPlane[0] + ".vtx[0]", armPlane[0] + ".vtx[2]", replace=True)
    vertexSel = cmds.ls(selection=True)
    pvLoc = vutil.createLocAtCenter(vertexSel)[0]
    # Aim constrain new locator towards wrist with up vector pointing towards elbow
    cmds.delete(
        cmds.aimConstraint(
            ikChain[-1],
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
        0, 75, 0, pvLoc, relative=True, objectSpace=True, worldSpaceDistance=False
    )
    # Create Pole vector control and snap to temp locator
    pvCtrl = rc.createSphereCtrl("%sarmPV_CTL" % ikChain[0][:2])
    cmds.select(pvCtrl, replace=True)
    draw.changeColor(ctrlColor)
    pvCtrlOffset = cmds.group(pvCtrl, name=pvCtrl.split("_CTL")[0] + "Offset_GRP")
    cmds.delete(cmds.pointConstraint(pvLoc, pvCtrlOffset, maintainOffset=False))
    cmds.poleVectorConstraint(pvCtrl, IKH, weight=1)

    # Cleanup
    cmds.delete(pvLoc, armPlane)

    # Organize nodes
    armModuleGrp = cmds.group(empty=True, name="%sarm_GRP" % fkChain[0][:2])
    armJointsGrp = cmds.group(
        empty=True, name="%sarm_JOINTS_GRP" % fkChain[0][:2], parent=armModuleGrp
    )
    armControlsGrp = cmds.group(
        empty=True, name="%sarm_CONTROLS_GRP" % fkChain[0][:2], parent=armModuleGrp
    )
    armGutsGrp = cmds.group(
        empty=True, name="%sarm_GUTS_GRP" % fkChain[0][:2], parent=armModuleGrp
    )
    # Parent control rig nodes to proper root organization nodes
    cmds.parent(bindChain[0], ikChain[0], fkChain[0], armJointsGrp)
    cmds.parent(
        ikFkSwitchOffset, fkCtrlGrps[0], ikCtrlOffset, pvCtrlOffset, armControlsGrp
    )

    # Add visibility switches to FK and IK controls
    cmds.connectAttr(reverseNode + ".outputX", ikCtrlOffset + ".visibility")
    cmds.connectAttr(reverseNode + ".outputX", pvCtrlOffset + ".visibility")
    cmds.connectAttr(multiDNode + ".outputX", fkCtrlGrps[0] + ".visibility")
    cmds.setAttr(IKH + ".visibility", 0)
    # Orient constrain the wristIk joint to the wristIK controller
    cmds.orientConstraint(ikCtrl, ikChain[-1], maintainOffset=True)

    #################################################################################
    # Clavicle Module
    # Create clavicle control and offset and constrain bind joint to controls
    clavCtrl = rc.createSphereCtrl("%sclavicle_CTL" % clavBindChain[0][:2])
    cmds.select(clavCtrl, replace=True)
    draw.changeColor(ctrlColor)
    clavCtrlOffset = cmds.group(clavCtrl, name=clavCtrl.split("_CTL")[0] + "Offset_GRP")
    cmds.delete(
        cmds.parentConstraint(clavBindChain[0], clavCtrlOffset, maintainOffset=False)
    )
    cmds.parentConstraint(clavCtrl, clavBindChain[0], maintainOffset=True)

    # Constrain arm bind joint and arm IK joint to clavicle end joint
    cmds.pointConstraint(clavBindChain[-1], bindChain[0], maintainOffset=True)
    cmds.pointConstraint(clavBindChain[-1], ikChain[0], maintainOffset=True)
    cmds.pointConstraint(clavBindChain[-1], fkCtrlGrps[0], maintainOffset=True)
    # Add point constraint to FK arm joint
    cmds.pointConstraint(clavBindChain[-1], fkCtrlGrps[0], maintainOffset=True)

    # Organize Nodes
    clavModuleGrp = cmds.group(empty=True, name="%sclavicle_GRP" % dupClavJnts[0][:2])
    clavJointsGrp = cmds.group(
        empty=True,
        name="%sclavicle_JOINTS_GRP" % dupClavJnts[0][:2],
        parent=clavModuleGrp,
    )
    clavControlsGrp = cmds.group(
        empty=True,
        name="%sclavicle_CONTROLS_GRP" % dupClavJnts[0][:2],
        parent=clavModuleGrp,
    )
    clavGutsGrp = cmds.group(
        empty=True,
        name="%sclavicle_GUTS_GRP" % dupClavJnts[0][:2],
        parent=clavModuleGrp,
    )
    # Parent control offsets and guts in clavicle module groups
    cmds.parent(clavCtrlOffset, clavControlsGrp)
    cmds.parent(clavBindChain[0], clavJointsGrp)

    #################################################################################
    # Parent and scale constrain the rig joints to the new control rig joints i.e. the bind joints
    # Clavicle
    cmds.parentConstraint(clavBindChain[0], clavJntName, maintainOffset=True)
    cmds.scaleConstraint(clavBindChain[0], clavJntName, maintainOffset=True)
    cmds.parentConstraint(clavBindChain[1], clavEndJnt, maintainOffset=True)
    cmds.scaleConstraint(clavBindChain[1], clavEndJnt, maintainOffset=True)
    # Upper arm
    cmds.parentConstraint(bindChain[0], shoulderJntName, maintainOffset=True)
    cmds.scaleConstraint(bindChain[0], shoulderJntName, maintainOffset=True)
    # Elbow
    elbowJnt = cmds.listRelatives(shoulderJntName, children=True, type="joint")[0]
    cmds.parentConstraint(bindChain[1], elbowJnt, maintainOffset=True)
    cmds.scaleConstraint(bindChain[1], elbowJnt, maintainOffset=True)
    # Wrist
    cmds.parentConstraint(bindChain[2], wristJntName, maintainOffset=True)
    cmds.scaleConstraint(bindChain[2], wristJntName, maintainOffset=True)

    # Final lock and hide controller attributes
    transAttrs = [".tx", ".ty", ".tz"]
    rotateAttrs = [".rx", ".ry", ".rz"]
    scaleAttrs = [".sx", ".sy", ".sz"]
    visAttrs = [".v"]

    # Clavicle ctrl
    vutil.lockAndHideAttrs(clavCtrl, transAttrs)
    vutil.lockAndHideAttrs(clavCtrl, scaleAttrs)
    vutil.lockAndHideAttrs(clavCtrl, visAttrs)
    # IK Hand ctrl
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
    cmds.undoInfo(chunkName="armModule_chunk", closeChunk=True)
    print("Arm Module is created.")


###############################################################################################################################
###############################################################################################################################
def createStabilizeCurve():
    cmds.undoInfo(chunkName="stabilizeCrv_chunk", openChunk=True)
    # Create straight curve with locator at end of it
    stabCrv = cmds.curve(
        name="side_shoulderStabilize_CRV",
        d=1,
        knot=[0, 1],
        point=[(-25, 0, 0), (25, 0, 0)],
    )
    stabLoc = cmds.spaceLocator(name="side_shoulderStabilize_LOC")[0]
    cmds.setAttr(stabLoc + ".tx", 25)
    cmds.parent(stabLoc, stabCrv)
    cmds.undoInfo(chunkName="stabilizeCrv_chunk", closeChunk=True)

    cmds.confirmDialog(
        title="Instructions",
        message="Parent Stabilize Curve under ClavicleBind_JNT and then snap to ShoulderBind_JNT.",
        button=["OK"],
        defaultButton="OK",
        cancelButton="OK",
        dismissString="OK",
    )


def createShoulderStabilizer(
    lineClavicle, lineShoulder, lineIkElbow, lineStabilizeCurve, lineMultiTwistJoints
):
    cmds.undoInfo(chunkName="stabilizer_chunk", openChunk=True)
    # Twist joints should be on the main rig, not the control rig
    # Get clavicle bind joint and the shoulder bind joint
    clavJnt = lineClavicle.text()
    shoulderJnt = lineShoulder.text()
    elbowJnt = lineIkElbow.text()
    getStabCrv = lineStabilizeCurve.text()
    # Get twist joints and create list from text field string
    allTwistJnts = lineMultiTwistJoints.text()
    twistJnts = allTwistJnts.split(",")
    # Get side of body prefix and color choice for controls
    sidePrefix = clavJnt[:2]
    # Get stabilizer curve and locator and rename to appropriate side prefix
    getStabLoc = cmds.listRelatives(getStabCrv, children=True, type="transform")[0]
    stabCrv = cmds.rename(getStabCrv, getStabCrv.replace("side_", sidePrefix))
    stabLoc = cmds.rename(getStabLoc, getStabLoc.replace("side_", sidePrefix))

    # # Parent curve under control rig clavicle
    # cmds.parent(stabCrv, "L_clavicleBind_JNT")

    # # Snap curve to control rig shoulder bind joint location
    # cmds.delete(cmds.parentConstraint("L_armBind_JNT", stabCrv, maintainOffset=False))

    # # Rotate curve to user liking for angle of stabilizing
    # cmds.rotate(49.582151,-10.383164,-110.507414, stabCrv, relative=True, objectSpace=True, forceOrderXYZ=True)

    # Create stabilizer groups: L_arm_STABLE, L_arm_ANGLE_OFF, L_arm_ANGLE
    stableGrp = cmds.group(name="%sarm_STABLE" % sidePrefix, empty=True, world=True)
    angleOffGrp = cmds.group(
        name="%sarm_ANGLE_OFF" % sidePrefix, empty=True, parent=stableGrp
    )
    cmds.setAttr(angleOffGrp + ".rx", 180)
    angleGrp = cmds.group(
        name="%sarm_ANGLE" % sidePrefix, empty=True, parent=angleOffGrp
    )

    # Parent STABLE group under clavicle bind joint and snap to shoulder IK joint
    cmds.parent(stableGrp, clavJnt)
    cmds.delete(cmds.parentConstraint(shoulderJnt, stableGrp, maintainOffset=False))

    # Aim constrain the STABLE group to IK elbow joint with:
    # aim = X
    # up = -Y
    # type = object up
    # object = locator
    if sidePrefix == "L_":
        stableAimCon = cmds.aimConstraint(
            elbowJnt,
            stableGrp,
            aimVector=(1, 0, 0),
            upVector=(0, 1, 0),
            worldUpType="object",
            worldUpObject=stabLoc,
        )
    elif sidePrefix == "R_":
        stableAimCon = cmds.aimConstraint(
            elbowJnt,
            stableGrp,
            aimVector=(-1, 0, 0),
            upVector=(0, -1, 0),
            worldUpType="object",
            worldUpObject=stabLoc,
        )

    # Aim constrain the ANGLE group to IK elbow joint with:
    # aim = X
    # up = -Y
    # type = object rotation up
    # vector = -Y
    # object = shoulder IK joint
    if sidePrefix == "L_":
        stableAimCon = cmds.aimConstraint(
            elbowJnt,
            angleGrp,
            aimVector=(1, 0, 0),
            upVector=(0, 1, 0),
            worldUpType="objectrotation",
            worldUpVector=(0, 1, 0),
            worldUpObject=shoulderJnt,
        )
    elif sidePrefix == "R_":
        stableAimCon = cmds.aimConstraint(
            elbowJnt,
            angleGrp,
            aimVector=(-1, 0, 0),
            upVector=(0, -1, 0),
            worldUpType="objectrotation",
            worldUpVector=(0, 1, 0),
            worldUpObject=shoulderJnt,
        )

    # Create multDiv node and connect the rotateX into multDiv's inputs
    multDiv = cmds.shadingNode(
        "multiplyDivide", name="%sshoulderStabilize_MLT" % sidePrefix, asUtility=True
    )
    cmds.connectAttr(angleGrp + ".rotateX", multDiv + ".input1X")
    cmds.connectAttr(angleGrp + ".rotateX", multDiv + ".input1Y")

    # Set multDiv input 2's to distribute rotation amounts i.e. 0.666, .333 for two twist joints
    cmds.setAttr(multDiv + ".input2X", 0.666666)
    cmds.setAttr(multDiv + ".input2Y", 0.333333)

    # Connect the multDiv's outputs to the corresponding twist joint rotations, in this case, rotateX
    cmds.connectAttr(multDiv + ".outputX", "%s.rotateX" % twistJnts[0])
    cmds.connectAttr(multDiv + ".outputY", "%s.rotateX" % twistJnts[1])

    cmds.undoInfo(chunkName="stabilizer_chunk", closeChunk=True)

    print("Stabilizer is created.")


###############################################################################################################################
###############################################################################################################################
