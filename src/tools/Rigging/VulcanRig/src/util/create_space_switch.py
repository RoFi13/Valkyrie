"""Create Space Switch."""

try:
    reload  # Python 2.7
except NameError:
    try:
        from importlib import reload  # Python 3.4+
    except ImportError:
        from imp import reload  # Python 3.0 - 3.3

import maya.cmds as cmds

from . import vulcan_utils as vutil

reload(vutil)


def createSpaceSwitch(localSpaceJnt, spaceSwitchCtrl, spaceSwitcherCtrl, rigModule):
    """
    Creates a space switch for arms and/or leg modules.
    IMPORTANT: USE AFTER CREATING THE ARM OR LEG MODULE
    """
    # Get UI field names
    # Local joint should be the pelvis joint created by the spine module
    localSpaceJntName = localSpaceJnt.text()
    # This should be the controller animators will use to switch between local and world space
    spaceSwitchCtrlName = spaceSwitchCtrl.text()
    # Same as space switcher ctrl
    switcherCtrlName = spaceSwitcherCtrl.text()
    # Select the top group node of the module for the space switch
    rigModuleName = rigModule.text()
    # Create space switch transform nodes
    localSpaceGrp = cmds.group(
        empty=True,
        world=True,
        name=rigModuleName.split("_GRP")[0] + "SpaceSwitch_local_GRP",
    )
    worldSpaceGrp = cmds.group(
        empty=True,
        world=True,
        name=rigModuleName.split("_GRP")[0] + "SpaceSwitch_world_GRP",
    )
    # Parent and match transforms for local space group node
    vutil.parentSnap(localSpaceJntName, localSpaceGrp)
    # Get GUTS group node in module and parent the world space group node under it
    moduleChildren = cmds.listRelatives(rigModuleName, children=True)
    for child in moduleChildren:
        if "GUTS" in child:
            cmds.parent(worldSpaceGrp, child)
    # Check to see if attribute "space" already exists on switcher controller
    # If not, create attribute on switcher controller
    if cmds.attributeQuery("local", node=switcherCtrlName, exists=True) == True:
        cmds.deleteAttr(switcherCtrlName + ".ikLocal")
    if cmds.attributeQuery("world", node=switcherCtrlName, exists=True) == True:
        cmds.deleteAttr(switcherCtrlName + ".ikWorld")
    # Create space attributes
    cmds.addAttr(
        switcherCtrlName,
        longName="ikLocal",
        attributeType="float",
        minValue=0,
        maxValue=1,
    )
    cmds.setAttr(switcherCtrlName + ".ikLocal", edit=True, keyable=True)
    cmds.addAttr(
        switcherCtrlName,
        longName="ikWorld",
        attributeType="float",
        minValue=0,
        maxValue=1,
    )
    cmds.setAttr(switcherCtrlName + ".ikWorld", edit=True, keyable=True)
    # Get offset node of controller being constrained to different spaces
    ctrlOffset = cmds.listRelatives(spaceSwitchCtrlName, parent=True)
    # Create space switch parent constraint and condition nodes
    parentCon = cmds.parentConstraint(
        localSpaceGrp, worldSpaceGrp, ctrlOffset, maintainOffset=True
    )[0]
    condA = cmds.createNode("condition", name=localSpaceGrp.split("_GRP")[0] + "_CND")
    condB = cmds.createNode("condition", name=worldSpaceGrp.split("_GRP")[0] + "_CND")
    # Attach controller attribute to condition nodes first term and set condition nodes value results
    for each in [condA, condB]:
        if "local" in each:
            cmds.connectAttr(
                switcherCtrlName + ".ikLocal", each + ".firstTerm", force=True
            )
            cmds.setAttr(each + ".colorIfTrueR", 1)
            cmds.setAttr(each + ".colorIfFalseR", 0)
        else:
            cmds.connectAttr(
                switcherCtrlName + ".ikWorld", each + ".firstTerm", force=True
            )
            cmds.setAttr(each + ".colorIfTrueR", 1)
            cmds.setAttr(each + ".colorIfFalseR", 0)

    cmds.setAttr(condA + ".secondTerm", 1)
    cmds.setAttr(condB + ".secondTerm", 1)
    # Connect condition nodes results to parent constraint weights
    cmds.connectAttr(condA + ".outColorR", parentCon + "." + localSpaceGrp + "W0")
    cmds.connectAttr(condB + ".outColorR", parentCon + "." + worldSpaceGrp + "W1")
    # Set Local space to be on by default
    cmds.setAttr(switcherCtrlName + ".ikLocal", 1)

    print("Space Switch was created!")


#################################################################################
#################################################################################
def attachToSpaceSwitch():
    """
    This creates a new constraint and attaches the existing condition nodes for the module to switch between spaces.
    Select the controller with the space switch attributes first, then the controller you want to add second.
    NOTE: This tool grabs the offset node above the controller you are adding to the space switch as the constrained object
    """
    switcher = cmds.ls(selection=True)[0]
    attachObj = cmds.ls(selection=True)[-1]
    attachObjOffset = cmds.listRelatives(attachObj, parent=True)
    # Get both condition nodes attached to the switcher controller
    cndNodes = cmds.listConnections(switcher, type="condition")
    for cnd in cndNodes:
        if "local" in cnd:
            localCnd = cnd
        else:
            worldCnd = cnd
    # Get constraint attached to condition nodes
    cndConstraint = cmds.listConnections(cndNodes[0], type="parentConstraint")[0]
    # Get world and local group node space switch nodes
    constraintDrivers = cmds.parentConstraint(
        cndConstraint, query=True, targetList=True
    )
    # Parent Constraint new object to space drivers
    newCon = cmds.parentConstraint(
        constraintDrivers[0], constraintDrivers[1], attachObjOffset, maintainOffset=True
    )[0]
    # Get weight attributes on constraint
    allConAttrs = cmds.attributeInfo(newCon, allAttributes=True)
    for attr in allConAttrs:
        if "SpaceSwitch_local" in attr:
            localWeightAttr = attr
        elif "SpaceSwitch_world" in attr:
            worldWeightAttr = attr
    # Attach condition nodes to new constraint weights
    cmds.connectAttr(
        localCnd + ".outColorR", newCon + "." + localWeightAttr, force=True
    )
    cmds.connectAttr(
        worldCnd + ".outColorR", newCon + "." + worldWeightAttr, force=True
    )
