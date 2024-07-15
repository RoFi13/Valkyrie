# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""Various functions to move and orient selected objects in Maya."""

import logging
import os
from typing import List

from maya import cmds

LOG = logging.getLogger(os.path.basename(__file__))


def snap_object(
    driver: str = None,
    driven: str = None,
    match_position: bool = True,
    match_rotation: bool = True,
):
    """Move second selected object to the first selected object.

    Moves and orients rotation of second object to the first selected object.
    """
    if driver is None and driven is None:
        selection = cmds.ls(selection=True)
        if not len(selection) == 2:
            raise IndexError("User must select two objects in scene.")
        driver = selection[0]
        driven = selection[1]

    # Check if driven object has connections already
    for attribute in ["tx", "ty", "tz", "rx", "ry", "rz"]:
        if check_for_existing_connection(driven, attribute):
            raise RuntimeError("Second selected object already has connection.")
    # Create constraint to move second object to first object's location
    # and rotation
    try:
        if match_position and match_rotation:
            new_constraint = cmds.parentConstraint(
                driver, driven, maintainOffset=False
            )[0]
        if match_position and not match_rotation:
            new_constraint = cmds.pointConstraint(driver, driven, maintainOffset=False)[
                0
            ]
        if not match_position and match_rotation:
            new_constraint = cmds.orientConstraint(
                driver, driven, maintainOffset=False
            )[0]

    except RuntimeError as exc:
        raise RuntimeError(
            "Driven object transforms locked. Failed to constrain."
        ) from exc

    # Check that the constraint was made successfully
    cmds.delete(new_constraint)


def world_space_snap():
    """Move second selected object to the first selected object.

    Like a parent constraint, but uses a world space locator with a child locator
    that is up 10 units in the Y axis acting as the object to orient the
    driven object to via aim constraint. Aim constraint aim axis is positive Y.
    """
    selection = cmds.ls(selection=True)

    logging.debug("Selection number: %s", len(selection))
    if not len(selection) == 2:
        raise IndexError("User must select two objects in scene.")

        # Check if driven object has connections already
    for attribute in ["tx", "ty", "tz", "rx", "ry", "rz"]:
        if check_for_existing_connection(selection[1], attribute):
            raise RuntimeError("Second selected object already has connection.")

    # Create locator setup
    locator_parent = cmds.spaceLocator()[0]
    locator_child = cmds.spaceLocator()[0]
    cmds.parent(locator_child, locator_parent)
    cmds.xform(locator_child, relative=True, translation=(0, 10, 0))

    # Move locator rig to driver object's position and rotation
    try:
        new_constraint = cmds.parentConstraint(
            selection[0], locator_parent, maintainOffset=False
        )[0]
    except RuntimeError as exc:
        raise RuntimeError(
            "Driven object transforms locked. Failed to constrain."
        ) from exc

    cmds.delete(new_constraint)

    # Get world space position of locator parent
    locator_position = []
    locator_position.append(cmds.getAttr(f"{locator_parent}.tx"))
    locator_position.append(cmds.getAttr(f"{locator_parent}.ty"))
    locator_position.append(cmds.getAttr(f"{locator_parent}.tz"))

    # Move driven object to locator position
    cmds.xform(selection[1], worldSpace=True, translation=locator_position)
    # Orient driven object to locator child's position
    try:
        aim_constraint = cmds.aimConstraint(
            locator_child,
            selection[1],
            aimVector=(0, 1, 0),
            upVector=(1, 0, 0),
            worldUpType="scene",
            offset=(0, 0, 0),
            weight=1,
        )
    except RuntimeError as exc:
        raise RuntimeError(
            "Driven object transforms locked. Failed to constrain."
        ) from exc

    # Scene cleanup
    cmds.delete(aim_constraint, locator_child, locator_parent)


def group_snap():
    """Create a group and snap it to the location of the object."""
    selection = cmds.ls(selection=True)

    if not len(selection) == 1:
        raise IndexError("User must select one object in the scene.")

    if cmds.referenceQuery(selection, isNodeReferenced=True):
        raise RuntimeError("Unable to parent a reference node.")

    result = cmds.confirmDialog(
        title="Match Rotation?",
        message="Do you want to match rotation?",
        button=["Yes", "No", "Cancel"],
        defaultButton="Yes",
        cancelButton="Cancel",
        dismissString="Cancel",
    )
    if result == "Cancel":
        logging.info("User cancelled operation.")
        raise RuntimeError("User cancelled operation.")

    parent_object = cmds.listRelatives(selection[0], parent=True)
    group_node = cmds.createNode("transform", name=(f"{selection[0]}_offset"))

    # If None, means object has no parent
    if parent_object is not None:
        cmds.parent(group_node, parent_object)

    # Move group node to the location of selection
    if result == "Yes":
        cmds.delete(
            cmds.parentConstraint(selection[0], group_node, maintainOffset=False)
        )
    else:
        cmds.delete(
            cmds.pointConstraint(selection[0], group_node, maintainOffset=False)
        )

    # Parent selection under the group node
    cmds.parent(selection[0], group_node)

    logging.info("Group snap was successful!")


def locator_snap():
    """Create a locator that matches the world space translate and rotate."""
    selection = cmds.ls(selection=True)

    # If nothing is selected, create a locator at the origin.
    if len(selection) == 0:
        cmds.spaceLocator()
        return

    if len(selection) > 1:
        raise IndexError("Please select only one object to snap the locator to.")

    # Ask user if they would like to match the rotation
    result = cmds.confirmDialog(
        title="Match Rotation?",
        message="Do you want to match rotation?",
        button=["Yes", "No", "Cancel"],
        defaultButton="Yes",
        cancelButton="Cancel",
        dismissString="Cancel",
    )

    locator_object = cmds.spaceLocator(name=selection[0] + "_loc")[0]
    # Get rotation order of selected object
    rotation_order = cmds.getAttr(selection[0] + ".rotateOrder")
    # Set the rotate order for the locator
    cmds.setAttr(locator_object + ".rotateOrder", rotation_order)

    if result == "Yes":
        # Move and match rotation
        cmds.delete(
            cmds.parentConstraint(selection, locator_object, maintainOffset=False)
        )
        return

    # Move but don't match rotation
    cmds.delete(cmds.pointConstraint(selection, locator_object, maintainOffset=False))


def check_for_existing_connection(object_name, transform_attribute="tx"):
    """Check to see if object already has a transform constraint.

    Args:
        object_name (str): Name of maya object to check for constraint.
        transform_attribute (str): Attribute to check for connection.
            Valid tranforms: "tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"

    Return:
        bool: True if object has a connection. Otherwise, False.
    """
    # If attribute has a connection...
    if cmds.connectionInfo(f"{object_name}.{transform_attribute}", isDestination=True):
        return True

    return False
