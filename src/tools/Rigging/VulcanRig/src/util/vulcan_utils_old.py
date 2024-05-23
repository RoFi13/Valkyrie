"""Vulcan Rigging Utilities."""

try:
    reload  # Python 2.7
except NameError:
    try:
        from importlib import reload  # Python 3.4+
    except ImportError:
        from imp import reload  # Python 3.0 - 3.3

import logging
import os

import maya.cmds as cmds
import maya.mel as mel

from Util.UtilTools.src import modeling_utils as mutil

reload(mutil)
from . import rig_controls as rc

reload(rc)

LOG = logging.getLogger(os.path.basename(__file__))


def insertJnts(numJnts, startJnt, endJnt):
    """
    This creates two twist joints between two selected joints
    """
    startTime = 1
    endTime = numJnts + 2
    jntRadius = cmds.getAttr(startJnt + ".radius")

    # Create locator
    tempLoc = cmds.spaceLocator(name="temp_insert_loc")

    # Get world space locations of start and end joints
    startPos = cmds.xform(startJnt, query=True, worldSpace=True, translation=True)
    endPos = cmds.xform(endJnt, query=True, worldSpace=True, translation=True)

    # Create curve based on positions
    tempCurve = cmds.curve(name="temp_insert_crv", degree=1, point=(startPos, endPos))

    # Attach locator to twist curve via motion path
    cmds.select(tempCurve, tempLoc, replace=True)
    tempPath = cmds.pathAnimation(startTimeU=startTime, endTimeU=endTime)

    # Make animation linear
    cmds.selectKey(
        tempPath + "_uValue", add=True, keyframe=True, time=(startTime, endTime)
    )
    cmds.keyTangent(inTangentType="linear", outTangentType="linear")

    # Create new temp locators for x number of joints with their world positions
    i = 2
    insertLocs = []
    allNewJnts = []
    while i < endTime:
        if i == 2:
            print(str(i))
            cmds.currentTime(i)
            loc = cmds.spaceLocator(name="temp_insert_loc_" + str(i - 1))[0]
            cmds.delete(cmds.parentConstraint(tempLoc, loc, maintainOffset=False))
            pos = cmds.xform(loc, query=True, worldSpace=True, translation=True)
            insertLocs.append(loc)

            # Insert new joint
            cmds.select(startJnt, replace=True)
            newJnt = cmds.insertJoint(startJnt)
            cmds.joint(newJnt, edit=True, component=True, position=(pos), absolute=True)
            cmds.setAttr(newJnt + ".radius", jntRadius)

            allNewJnts.append(newJnt)

            i += 1

        else:
            print(str(i))
            cmds.currentTime(i)
            loc = cmds.spaceLocator(name="temp_insert_loc_" + str(i - 1))[0]
            cmds.delete(cmds.parentConstraint(tempLoc, loc, maintainOffset=False))
            pos = cmds.xform(loc, query=True, worldSpace=True, translation=True)
            insertLocs.append(loc)

            # Insert new joint
            cmds.select(allNewJnts[i - 3], replace=True)
            newJnt = cmds.insertJoint(insertLocs[i - 2])
            cmds.joint(newJnt, edit=True, component=True, position=(pos), absolute=True)
            cmds.setAttr(newJnt + ".radius", jntRadius)

            allNewJnts.append(newJnt)

            i += 1

    # Scene cleanup
    cmds.delete(tempLoc, tempCurve, tempPath, insertLocs)

    # Rename new joints
    r = 1
    for jnt in allNewJnts:
        if not r >= 10:
            cmds.rename(jnt, startJnt + "_mid_0" + str(r))
            r += 1

        else:
            cmds.rename(jnt, startJnt + "_mid_" + str(r))
            r += 1


def insertJnts2(numJnts):
    """
    This creates two twist joints between two selected joints
    """
    print(str(numJnts))
    sel = cmds.ls(selection=True)
    if len(sel) > 2:
        cmds.error("Please select only two joints as your start and end joints.")

    startJnt = sel[0]
    endJnt = sel[1]

    startTime = 1
    endTime = numJnts + 2
    jntRadius = cmds.getAttr(startJnt + ".radius")

    # Create locator
    tempLoc = cmds.spaceLocator(name="temp_insert_loc")

    # Get world space locations of start and end joints
    startPos = cmds.xform(startJnt, query=True, worldSpace=True, translation=True)
    endPos = cmds.xform(endJnt, query=True, worldSpace=True, translation=True)

    # Create curve based on positions
    tempCurve = cmds.curve(name="temp_insert_crv", degree=1, point=(startPos, endPos))

    # Attach locator to twist curve via motion path
    cmds.select(tempCurve, tempLoc, replace=True)
    tempPath = cmds.pathAnimation(startTimeU=startTime, endTimeU=endTime)

    # Make animation linear
    cmds.selectKey(
        tempPath + "_uValue", add=True, keyframe=True, time=(startTime, endTime)
    )
    cmds.keyTangent(inTangentType="linear", outTangentType="linear")

    # Create new temp locators for x number of joints with their world positions
    i = 2
    insertLocs = []
    allNewJnts = []
    while i < endTime:
        if i == 2:
            print(str(i))
            cmds.currentTime(i)
            loc = cmds.spaceLocator(name="temp_insert_loc_" + str(i - 1))[0]
            cmds.delete(cmds.parentConstraint(tempLoc, loc, maintainOffset=False))
            pos = cmds.xform(loc, query=True, worldSpace=True, translation=True)
            insertLocs.append(loc)

            # Insert new joint
            cmds.select(startJnt, replace=True)
            newJnt = cmds.insertJoint(startJnt)
            cmds.joint(newJnt, edit=True, component=True, position=(pos), absolute=True)
            cmds.setAttr(newJnt + ".radius", jntRadius)

            allNewJnts.append(newJnt)

            i += 1

        else:
            print(str(i))
            cmds.currentTime(i)
            loc = cmds.spaceLocator(name="temp_insert_loc_" + str(i - 1))[0]
            cmds.delete(cmds.parentConstraint(tempLoc, loc, maintainOffset=False))
            pos = cmds.xform(loc, query=True, worldSpace=True, translation=True)
            insertLocs.append(loc)

            # Insert new joint
            cmds.select(allNewJnts[i - 3], replace=True)
            newJnt = cmds.insertJoint(insertLocs[i - 2])
            cmds.joint(newJnt, edit=True, component=True, position=(pos), absolute=True)
            cmds.setAttr(newJnt + ".radius", jntRadius)

            allNewJnts.append(newJnt)

            i += 1

    # Scene cleanup
    cmds.delete(tempLoc, tempCurve, tempPath, insertLocs)

    # Rename new joints
    r = 1
    for jnt in allNewJnts:
        if not r >= 10:
            cmds.rename(jnt, startJnt + "_mid_0" + str(r))
            r += 1

        else:
            cmds.rename(jnt, startJnt + "_mid_" + str(r))
            r += 1


####################################################################################################################
####################################################################################################################
def displayLocalRotationAxis(state):
    sel = cmds.ls(selection=True)

    for item in sel:
        if cmds.objExists(item + ".displayLocalAxis"):
            cmds.setAttr(item + ".displayLocalAxis", state)


####################################################################################################################
####################################################################################################################
def toggleVisConstraints(state):
    # Toggles visibility of all constraints in the outliner
    constTypes = [
        "parentConstraint",
        "pointConstraint",
        "orientConstraint",
        "scaleConstraint",
        "aimConstraint",
        "poleVectorConstraint",
    ]
    # Get all constraints
    allConstraints = cmds.ls(type=constTypes)

    if state:
        # If constraints are going to be hidden in outliner, create a group node in world to remind user they are hidden
        if cmds.objExists("CONSTRAINTS_ARE_HIDDEN"):
            cmds.delete("CONSTRAINTS_ARE_HIDDEN")

        reminder = cmds.group(empty=True, name="CONSTRAINTS_ARE_HIDDEN")
        cmds.reorder(reminder, front=True)

    else:
        cmds.delete("CONSTRAINTS_ARE_HIDDEN")

    for const in allConstraints:
        cmds.setAttr(const + ".hiddenInOutliner", state)

    mel.eval("AEdagNodeCommonRefreshOutliners()")


####################################################################################################################
####################################################################################################################
def createLocAtCenter(sel):
    """
    This will create a locator at the center of the bounding box of your selection. Can select vertices for this function
    """
    # sel = cmds.ls(selection=True)
    bbx = cmds.xform(sel, query=True, boundingBox=True, worldSpace=True)  # world space
    centerX = (bbx[0] + bbx[3]) / 2.0
    centerY = (bbx[1] + bbx[4]) / 2.0
    centerZ = (bbx[2] + bbx[5]) / 2.0

    loc = cmds.spaceLocator(name="deleteMe_loc")

    cmds.xform(loc, worldSpace=True, translation=[centerX, centerY, centerZ])

    return loc


####################################################################################################################
####################################################################################################################
def mirrorDupCtrl():
    """
    Duplicates and mirrors control from +x to -x
    """
    # Get joint that needs the mirrored control
    mirrorJnt = cmds.ls(sl=True)[0]
    # Get control to be mirrored
    ctrl = cmds.ls(sl=True)[1]

    # Duplicate controller and parent to world
    newCtrl = cmds.duplicate(ctrl, renameChildren=True)[0]
    cmds.parent(newCtrl, world=True)
    ctrlShapes = cmds.listRelatives(newCtrl, shapes=True)

    totalCvs = 0
    for shape in ctrlShapes:
        # Get number of cvs for selected control
        degs = cmds.getAttr(shape + ".degree")
        spans = cmds.getAttr(shape + ".spans")
        numCvs = degs + spans
        # Mirror cvs in world space; check to see if number of cvs is odd or even and mirror appropriately
        if not numCvs % 2:
            i = 0
            while i < numCvs:
                pos = cmds.xform(
                    "%s.cv[%s]" % (shape, i),
                    query=True,
                    translation=True,
                    worldSpace=True,
                )
                cmds.xform(
                    "%s.cv[%s]" % (shape, i),
                    translation=[pos[0] * -1, pos[1], pos[2]],
                    worldSpace=True,
                )
                i += 1
        else:
            i = 0
            while i <= numCvs:
                pos = cmds.xform(
                    "%s.cv[%s]" % (shape, i),
                    query=True,
                    translation=True,
                    worldSpace=True,
                )
                cmds.xform(
                    "%s.cv[%s]" % (shape, i),
                    translation=[pos[0] * -1, pos[1], pos[2]],
                    worldSpace=True,
                )
                i += 1

    # Create new group node for mirrored control and snap to new joint
    newOffset = cmds.group(empty=True, world=True)
    cmds.delete(cmds.parentConstraint(mirrorJnt, newOffset, maintainOffset=False))

    # Copy pivot of new offset to new controller
    cmds.select(newOffset, newCtrl, replace=True)
    mutil.copyPivot()

    # Parent new controller under new offset
    cmds.parent(newCtrl, newOffset)


####################################################################################################################
####################################################################################################################
def mirrorCtrlShapes():
    """
    Mirrors the source control cv locations to the target control cv locations without changing the pivots.
    Works on multiple shape nodes. Mirrors across the YZ plane in either direction.
    """
    # Get joint that needs the mirrored control
    sourceCtrl = cmds.ls(sl=True)[0]
    # Get control to be mirrored
    targetCtrl = cmds.ls(sl=True)[1]
    # Get shape nodes of source ctrl and target ctrl
    sourceShapes = cmds.listRelatives(sourceCtrl, shapes=True)
    targetShapes = cmds.listRelatives(targetCtrl, shapes=True)

    totalCvs = 0
    r = 0
    for shape in sourceShapes:
        # Get number of cvs for selected control
        degs = cmds.getAttr(shape + ".degree")
        spans = cmds.getAttr(shape + ".spans")
        numCvs = degs + spans
        # Mirror cvs in world space across the YZ plane; check to see if number of cvs is odd or even and mirror appropriately
        if not numCvs % 2:
            i = 0
            while i < numCvs:
                pos = cmds.xform(
                    "%s.cv[%s]" % (shape, i),
                    query=True,
                    translation=True,
                    worldSpace=True,
                )
                for cv in targetShapes[r]:
                    cmds.xform(
                        "%s.cv[%s]" % (targetShapes[r], i),
                        translation=[pos[0] * -1, pos[1], pos[2]],
                        worldSpace=True,
                    )
                i += 1
        else:
            i = 0
            while i <= numCvs:
                pos = cmds.xform(
                    "%s.cv[%s]" % (shape, i),
                    query=True,
                    translation=True,
                    worldSpace=True,
                )
                for cv in targetShapes[r]:
                    cmds.xform(
                        "%s.cv[%s]" % (targetShapes[r], i),
                        translation=[pos[0] * -1, pos[1], pos[2]],
                        worldSpace=True,
                    )
                i += 1
        r += 1


####################################################################################################################
####################################################################################################################
def parentSnap(parentObj, childObj):
    """
    Parents object and zeroes out transforms
    """
    allAttr = [".tx", ".ty", ".tz", ".rx", ".ry", ".rz"]
    cmds.parent(childObj, parentObj)
    for attr in allAttr:
        cmds.setAttr(childObj + attr, 0)


####################################################################################################################
####################################################################################################################
def selectConstraintDriver():
    sel = cmds.ls(selection=True)[0]

    chanAttr = [".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz"]

    # Check to see if any of the channel box attributes of selected item is being driven by anything
    for attr in chanAttr:
        # If attribute has a connection...
        if cmds.connectionInfo(sel + attr, isDestination=True):
            # Get source node of connection
            const = cmds.connectionInfo(sel + attr, sourceFromDestination=True)
            newConst = const.split(".")[0]

            # The attribute type will determine which constraint attribute to query for the driver of the constraint
            if "t" in attr:
                obj = cmds.connectionInfo(
                    newConst + ".target[0].targetTranslate", sourceFromDestination=True
                )
                driver = obj.split(".")[0]

                cmds.select(driver, replace=True)

            elif "r" in attr:
                obj = cmds.connectionInfo(
                    newConst + ".target[0].targetRotate", sourceFromDestination=True
                )
                driver = obj.split(".")[0]

                cmds.select(driver, replace=True)

            elif "s" in attr:
                obj = cmds.connectionInfo(
                    newConst + ".target[0].targetScale", sourceFromDestination=True
                )
                driver = obj.split(".")[0]

                cmds.select(driver, replace=True)

            break

    return driver


####################################################################################################################
####################################################################################################################
def dupJointChain(startJnt, endJnt, includeTwistJnts=False):
    """
    Duplicates joint hierarchy given the start and end joints in chain.
    """
    # Check to delete twist joints if desired
    if not includeTwistJnts:
        allChildren = cmds.listRelatives(startJnt, allDescendents=True)
        for child in allChildren:
            if "twist" in child or "Twist" in child:
                cmds.delete(child)

    # Pickwalk down starting from the startJnt until it reaches the end joint,
    # storing each joint in a list on the way
    i = 0
    newJnts = [startJnt]
    cmds.select(startJnt, replace=True)
    while i < 99:
        # Pick walk and store each new joint down hierarchy
        curJnt = cmds.pickWalk(direction="down")[0]
        if endJnt in curJnt:
            # If the endJnt is equal to the current joint during pick walking, append to list and break loop
            newJnts.append(curJnt)
            break
        else:
            newJnts.append(curJnt)
        i += 1

    # Duplicate new joint list hierarchy
    dupJnts = cmds.duplicate(newJnts, parentOnly=True, renameChildren=True)
    # Parent to world space
    LOG.info("DUPLICATE JOINTS: %s", dupJnts[0])
    cmds.parent(dupJnts[0], world=True)

    LOG.info("test")

    return dupJnts


####################################################################################################################
####################################################################################################################
def getJointHierarchy(startJnt, endJnt):
    i = 0
    newJnts = [startJnt]
    cmds.select(startJnt, replace=True)
    while i < 99:
        # Pick walk and store each new joint down hierarchy
        curJnt = cmds.pickWalk(direction="down")[0]
        if endJnt in curJnt:
            # If the endJnt is equal to the current joint during pick walking, append to list and break loop
            newJnts.append(curJnt)
            break
        else:
            newJnts.append(curJnt)
        i += 1

    return newJnts


####################################################################################################################
####################################################################################################################
def createBendVolumizer():
    """
    This will create a node network to help preserve volume around bend joints.
    First you have to create the helper joints near the bend joint in the orientation you want.
    Then select your bend joint first, then the two helper joints
    """
    cmds.undoInfo(chunkName="createBendVolumizer_chunk", openChunk=True)

    bendJnt = cmds.ls(selection=True)[0]
    volumeJnts = cmds.ls(selection=True)[1:]

    for jnt in volumeJnts:
        if "Inner" in jnt:
            # Create custom multiplier attribute for bend joint
            cmds.addAttr(
                bendJnt, longName="innerMult", attributeType="double", defaultValue=0
            )
            cmds.setAttr(bendJnt + ".innerMult", edit=True, keyable=True)
            # Create group offset node for corrective joint
            parentJnt = cmds.listRelatives(bendJnt, parent=True, type="joint")
            offset = cmds.group(
                name=jnt.replace("_JNT", "Offset_GRP"), world=True, empty=True
            )
            cmds.delete(cmds.parentConstraint(bendJnt, offset, maintainOffset=False))
            cmds.parent(jnt, offset)
            cmds.pointConstraint(bendJnt, offset, maintainOffset=True)
            cmds.orientConstraint(parentJnt, bendJnt, offset, maintainOffset=False)
            # Create utility nodes for volume preservation network
            innerMult = cmds.shadingNode(
                "multDoubleLinear",
                name=bendJnt + "_innerMultiplier_MDL",
                asUtility=True,
            )
            rotateMult = cmds.shadingNode(
                "multDoubleLinear",
                name=bendJnt + "_innerRotateMult_MDL",
                asUtility=True,
            )
            reverseMult = cmds.shadingNode(
                "multDoubleLinear",
                name=bendJnt + "_innerReverseMult_MDL",
                asUtility=True,
            )
            volumeCondition = cmds.shadingNode(
                "condition", name=bendJnt + "_innerAbsolute_CND", asUtility=True
            )
            finalAdd = cmds.shadingNode(
                "addDoubleLinear", name=bendJnt + "_innerCrt_ADL", asUtility=True
            )
            # Set attribute values for all nodes
            cmds.setAttr(innerMult + ".input2", 0.003)
            cmds.setAttr(reverseMult + ".input2", -1)
            cmds.setAttr(volumeCondition + ".operation", 4)
            cmds.setAttr(finalAdd + ".input2", 0.150)
            # Make all connections between nodes
            cmds.connectAttr(bendJnt + ".innerMult", innerMult + ".input1")
            cmds.connectAttr(innerMult + ".output", rotateMult + ".input2")
            cmds.connectAttr(bendJnt + ".rotateX", rotateMult + ".input1")
            cmds.connectAttr(rotateMult + ".output", reverseMult + ".input1")
            cmds.connectAttr(rotateMult + ".output", volumeCondition + ".firstTerm")
            cmds.connectAttr(reverseMult + ".output", volumeCondition + ".colorIfTrueR")
            cmds.connectAttr(rotateMult + ".output", volumeCondition + ".colorIfFalseR")
            cmds.connectAttr(volumeCondition + ".outColorR", finalAdd + ".input1")
            # Final connection into volume corrective joint
            cmds.connectAttr(finalAdd + ".output", jnt + ".translateZ")

        # If current item is outer joint
        else:
            # Create custom multiplier attribute for bend joint
            cmds.addAttr(
                bendJnt, longName="outerMult", attributeType="double", defaultValue=0
            )
            cmds.setAttr(bendJnt + ".outerMult", edit=True, keyable=True)
            # Create group offset node for corrective joint
            parentJnt = cmds.listRelatives(bendJnt, parent=True, type="joint")
            offset = cmds.group(
                name=jnt.replace("_JNT", "Offset_GRP"), world=True, empty=True
            )
            cmds.delete(cmds.parentConstraint(bendJnt, offset, maintainOffset=False))
            cmds.parent(jnt, offset)
            cmds.pointConstraint(bendJnt, offset, maintainOffset=True)
            cmds.orientConstraint(parentJnt, bendJnt, offset, maintainOffset=False)
            # Create utility nodes for volume preservation network
            outerMult = cmds.shadingNode(
                "multDoubleLinear",
                name=bendJnt + "_outerMultiplier_MDL",
                asUtility=True,
            )
            rotateMult = cmds.shadingNode(
                "multDoubleLinear",
                name=bendJnt + "_outerRotateMult_MDL",
                asUtility=True,
            )
            reverseMult = cmds.shadingNode(
                "multDoubleLinear",
                name=bendJnt + "_outerReverseMult_MDL",
                asUtility=True,
            )
            volumeCondition = cmds.shadingNode(
                "condition", name=bendJnt + "_outerAbsolute_CND", asUtility=True
            )
            finalAdd = cmds.shadingNode(
                "addDoubleLinear", name=bendJnt + "_outerCrt_ADL", asUtility=True
            )
            # Set attribute values for all nodes
            cmds.setAttr(outerMult + ".input2", 0.003)
            cmds.setAttr(reverseMult + ".input2", -1)
            cmds.setAttr(volumeCondition + ".operation", 2)
            cmds.setAttr(finalAdd + ".input2", -0.1)
            # Make all connections between nodes
            cmds.connectAttr(bendJnt + ".outerMult", outerMult + ".input1")
            cmds.connectAttr(outerMult + ".output", rotateMult + ".input2")
            cmds.connectAttr(bendJnt + ".rotateX", rotateMult + ".input1")
            cmds.connectAttr(rotateMult + ".output", reverseMult + ".input1")
            cmds.connectAttr(rotateMult + ".output", volumeCondition + ".firstTerm")
            cmds.connectAttr(reverseMult + ".output", volumeCondition + ".colorIfTrueR")
            cmds.connectAttr(rotateMult + ".output", volumeCondition + ".colorIfFalseR")
            cmds.connectAttr(volumeCondition + ".outColorR", finalAdd + ".input1")
            # Final connection into volume corrective joint
            cmds.connectAttr(finalAdd + ".output", jnt + ".translateZ")

    cmds.undoInfo(chunkName="createBendVolumizer_chunk", closeChunk=True)


####################################################################################################################
####################################################################################################################
def insertTwistJoints(numJnts):
    """
    This will insert the number of twist joints you want from the UI parenting the twist joints under the start joint
    """
    cmds.undoInfo(chunkName="addTwist_chunk", openChunk=True)

    startJnt = cmds.ls(selection=True)[0]
    endJnt = cmds.ls(selection=True)[-1]
    # Get start and end joint world positions
    startPos = cmds.xform(startJnt, query=True, worldSpace=True, translation=True)
    endPos = cmds.xform(endJnt, query=True, worldSpace=True, translation=True)

    if numJnts == 2:
        # Create curve based on those positions
        tempCurve = cmds.curve(
            name="temp_insert_crv", degree=1, point=(startPos, endPos)
        )
        # Rebuild curve so that there are only two cvs in the middle of the curve
        cmds.rebuildCurve(
            tempCurve,
            constructionHistory=False,
            replaceOriginal=True,
            rebuildType=0,
            endKnots=1,
            keepRange=0,
            keepControlPoints=False,
            keepEndPoints=True,
            keepTangents=False,
            spans=3,
            degree=1,
            tolerance=0.01,
        )
        # Create 3 joints with the last one at the end joint selection (used for joint orient)
        # Get curve cv point world positions
        crvTwist01 = cmds.xform(
            "%s.cv[%s]" % (tempCurve, 1), query=True, worldSpace=True, translation=True
        )
        crvTwist02 = cmds.xform(
            "%s.cv[%s]" % (tempCurve, 2), query=True, worldSpace=True, translation=True
        )
        crvTwistEnd = cmds.xform(
            "%s.cv[%s]" % (tempCurve, -1), query=True, worldSpace=True, translation=True
        )

        cmds.select(clear=True)
        newTwistJnt1 = cmds.insertJoint(startJnt)
        twistJnt1 = cmds.rename(newTwistJnt1, startJnt.replace("_JNT", "Twist01_JNT"))
        cmds.joint(
            name=twistJnt1,
            edit=True,
            component=True,
            absolute=True,
            position=(crvTwist01[0], crvTwist01[1], crvTwist01[2]),
        )
        wristJnt = cmds.listRelatives(twistJnt1, children=True, type="joint")[0]

        cmds.select(clear=True)
        newTwistJnt2 = cmds.insertJoint(startJnt)
        twistJnt2 = cmds.rename(newTwistJnt2, startJnt.replace("_JNT", "Twist02_JNT"))
        cmds.joint(
            name=twistJnt2,
            edit=True,
            component=True,
            absolute=True,
            position=(crvTwist02[0], crvTwist02[1], crvTwist02[2]),
        )

        cmds.select(clear=True)
        newTwistJntEnd = cmds.insertJoint(startJnt)
        twistJntEnd = cmds.rename(
            newTwistJntEnd, startJnt.replace("_JNT", "TwistEnd_JNT")
        )
        cmds.joint(
            twistJntEnd,
            edit=True,
            component=True,
            absolute=True,
            position=(endPos[0], endPos[1], endPos[2]),
        )

        cmds.parent(twistJnt1, twistJnt2, wristJnt, startJnt)

        # Cleanup
        cmds.delete(twistJntEnd, tempCurve)

    else:
        # Just kidding, but this tool would need to be updated if you wanted more than 2 twist joints
        print("Too many twist Joints!!!")

    cmds.undoInfo(chunkName="addTwist_chunk", closeChunk=True)


#################################################################################
# Create twist node network after creating twist joints
def createTwistNetwork(lineIkElbow, lineWrist, linePointerJnt, lineMultiTwistJoints):
    """
    Creates the node network for a regular twist setup that doesn't require the shoulder stabilization method.
    IMPORTANT!!! This needs one more joint as a child of the end joint i.e. a pointer joint.
    """
    cmds.undoInfo(chunkName="twistNetwork_chunk", openChunk=True)
    # Twist joints should be on the main rig, not the control rig
    # Get clavicle bind joint and the shoulder bind joint
    elbowJnt = lineIkElbow.text()
    wristJnt = lineWrist.text()
    pointerJnt = linePointerJnt.text()
    allTwistJnts = lineMultiTwistJoints.text()
    twistJnts = allTwistJnts.split(",")

    # Get side of body prefix and color choice for controls
    sidePrefix = elbowJnt[:2]

    # Create stabilizer groups: L_arm_STABLE, L_arm_ANGLE_OFF, L_arm_ANGLE
    stableGrp = cmds.group(name="%sTwist_STABLE" % elbowJnt, empty=True, world=True)
    angleOffGrp = cmds.group(
        name="%sTwist_ANGLE_OFF" % elbowJnt, empty=True, parent=stableGrp
    )
    angleGrp = cmds.group(
        name="%sTwist_ANGLE" % elbowJnt, empty=True, parent=angleOffGrp
    )

    # Parent STABLE group under clavicle bind joint and snap to shoulder IK joint
    cmds.parent(stableGrp, elbowJnt)
    cmds.delete(cmds.parentConstraint(wristJnt, stableGrp, maintainOffset=False))

    # Aim constrain the STABLE group to IK elbow joint with:
    # aim = X
    # up = -Y
    # type = object up
    # object = locator
    # stableAimCon = cmds.aimConstraint(elbowJnt, stableGrp, aimVector=(1,0,0), upVector=(0,-1,0), worldUpType="object",
    # 	worldUpObject=stabLoc)

    # Aim constrain the ANGLE group to IK elbow joint with:
    # aim = X
    # up = -Y
    # type = object rotation up
    # vector = -Y
    # object = shoulder IK joint
    # stableAimCon = cmds.aimConstraint(elbowJnt, angleGrp, aimVector=(1,0,0), upVector=(0,-1,0), worldUpType="objectrotation",
    # 	worldUpVector=(0,-1,0), worldUpObject=shoulderJnt)
    if sidePrefix == "L_":
        stableAimCon = cmds.aimConstraint(
            pointerJnt,
            angleGrp,
            aimVector=(1, 0, 0),
            upVector=(0, -1, 0),
            worldUpType="objectrotation",
            worldUpVector=(0, -1, 0),
            worldUpObject=wristJnt,
        )
    elif sidePrefix == "R_":
        stableAimCon = cmds.aimConstraint(
            pointerJnt,
            angleGrp,
            aimVector=(-1, 0, 0),
            upVector=(0, 1, 0),
            worldUpType="objectrotation",
            worldUpVector=(0, 1, 0),
            worldUpObject=wristJnt,
        )

    # Create multDiv node and connect the rotateX into multDiv's inputs
    multDiv = cmds.shadingNode(
        "multiplyDivide", name="%sTwist_MLT" % elbowJnt, asUtility=True
    )
    cmds.connectAttr(angleGrp + ".rotateX", multDiv + ".input1X")
    cmds.connectAttr(angleGrp + ".rotateX", multDiv + ".input1Y")

    # Set multDiv input 2's to distribute rotation amounts i.e. 0.666, .333 for two twist joints
    cmds.setAttr(multDiv + ".input2X", 0.333333)
    cmds.setAttr(multDiv + ".input2Y", 0.666666)

    # Connect the multDiv's outputs to the corresponding twist joint rotations, in this case, rotateX
    cmds.connectAttr(multDiv + ".outputX", "%s.rotateX" % twistJnts[0])
    cmds.connectAttr(multDiv + ".outputY", "%s.rotateX" % twistJnts[1])

    cmds.undoInfo(chunkName="twistNetwork_chunk", closeChunk=True)

    print("Twist network is created.")


####################################################################################################################
####################################################################################################################
def finalizeRig(lineRigName):
    """
    Create final group nodes for organization. Parent and scale constrain all module organization nodes to an orient controller.
    Select the top rig joint and then select the rest of the modules.
    """
    rigName = lineRigName.text()

    rigJoints = cmds.ls(selection=True)[0]
    allModules = cmds.ls(selection=True)[1:]
    if not cmds.objectType(rigJoints, isType="joint"):
        cmds.error("Please select your rig hierarchy first then all other rig modules.")
    # Create orient controller
    orientCtrl = rc.createCircleCtrl("orient_CTL")

    # Create final rig organization nodes
    rigGrp = cmds.group(empty=True, name="%s_RIG" % rigName)
    rigJointsGrp = cmds.group(empty=True, name="JOINTS_GRP", parent=rigGrp)
    rigControlsGrp = cmds.group(empty=True, name="CONTROLS_GRP", parent=rigGrp)
    rigGutsGrp = cmds.group(empty=True, name="GUTS_GRP", parent=rigGrp)
    rigModulesGrp = cmds.group(empty=True, name="MODULES_GRP", parent=rigGrp)
    # Parent orient to rig controls group; parent rig joint hierarchy to rig joint group
    cmds.parent(orientCtrl, rigControlsGrp)
    cmds.parent(rigJoints, rigJointsGrp)
    # Parent and scale constrain all module subGroups to orient control and parent modules to rig modules group
    for mod in allModules:
        modGrps = cmds.listRelatives(mod, children=True)
        for child in modGrps:
            if not "GUTS" in child:
                cmds.parentConstraint(orientCtrl, child, maintainOffset=True)
                cmds.scaleConstraint(orientCtrl, child, maintainOffset=True)
        cmds.parent(mod, rigModulesGrp)


def lockAndHideAttrs(obj, attrs):
    """
    Locks and hides the given attributes
    """
    for attr in attrs:
        cmds.setAttr(obj + attr, lock=True, keyable=False, channelBox=False)


####################################################################################################################
####################################################################################################################
def selectAllNonEndJoints():
    """
    This will select all joints of a hierarchy excluding any joints with "End" in the name.
    Select the top joint selection
    """
    sel = cmds.ls(selection=True)

    if cmds.objectType(sel, isType="joint"):
        allJntChildren = cmds.listRelatives(sel, allDescendents=True, type="joint")

        nonEndJnts = []
        for jnt in allJntChildren:
            if not "End" in jnt:
                nonEndJnts.append(jnt)

        cmds.select(nonEndJnts, sel, replace=True)

    else:
        cmds.warning("Please select only one top joint.")


####################################################################################################################
####################################################################################################################

####################################################################################################################
####################################################################################################################
