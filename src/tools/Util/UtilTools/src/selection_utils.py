# Copyright Robert Wiese 2024 - All Rights Reserved.
"""Functions for various selection operations."""

import logging
import os

from maya import cmds

LOG = logging.getLogger(os.path.basename(__file__))


def select_children(all_children: bool = False, mesh_only: bool = False):
    """Select children of selected object.

    Args:
        all_children (bool, optional): Whether to select all descendants. Defaults
            to False.
        mesh_only (bool, optional): Whether to select only meshes. Defaults to False.

    Raises:
        IndexError: If no objects are selected.
        IndexError: If no geometry children are found.
    """
    try:
        selection = cmds.ls(selection=True)[0]
    except IndexError as exc:
        raise IndexError("User must select one object in scene.") from exc

    children = []
    if not mesh_only:
        children = cmds.listRelatives(selection, allDescendents=all_children)
        if children is not None:
            cmds.select(children, replace=True)
            return

    children = cmds.listRelatives(selection, children=all_children)
    all_geometry_transforms = find_meshes(children)

    if len(all_geometry_transforms) == 0:
        raise IndexError("No geometry children found.")

    cmds.select(all_geometry_transforms, replace=True)


def find_meshes(selection: list):
    """Find transform nodes that have mesh children.

    Args:
        selection (list): Maya objects to check.

    Returns:
        list: Return list of transform nodes that have mesh children. Otherwise,
            return an empty list.
    """
    objects_with_meshes = []
    for obj in selection:
        object_children = cmds.listRelatives(obj, children=True, type="mesh")
        if object_children is not None:
            objects_with_meshes.append(obj)

    return objects_with_meshes


def toggle_mesh_select():
    """Toggle mesh select."""
    if cmds.selectType(query=True, polymesh=True):
        cmds.selectType(
            polymesh=False, plane=False, nurbsSurface=False, byName=["gpuCache", False]
        )
    else:
        cmds.selectType(
            polymesh=True, plane=True, nurbsSurface=True, byName=["gpuCache", True]
        )


def select_constraint_driver():
    """Select the constraint driver of a selected item if one exists."""
    # Check that selection is of 1 and only 1 object.
    channel_attribute = [".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz"]
    selected = cmds.ls(selection=True)
    if len(selected) != 1:
        LOG.warning(
            "constraint_mod: Function expects 1 object to be selected, but "
            "%s objects were selected. Please select one object.",
            len(selected),
        )
        return
    selected = selected[0]

    # Check to see if any of the channel box attributes of selected item is
    # being driven by anything
    for attribute in channel_attribute:
        # If attribute has a connection...
        if cmds.connectionInfo(selected + attribute, isDestination=True):
            # Get source node of connection
            const = cmds.connectionInfo(
                selected + attribute, sourceFromDestination=True
            )
            new_const = const.split(".")[0]

            # The attribute type will determine which constraint attribute to
            # query for the driver of the constraint
            if "t" in attribute:
                obj = cmds.connectionInfo(
                    new_const + ".target[0].targetTranslate", sourceFromDestination=True
                )
                driver = obj.split(".")[0]

                cmds.select(driver, replace=True)

            elif "r" in attribute:
                obj = cmds.connectionInfo(
                    new_const + ".target[0].targetRotate", sourceFromDestination=True
                )
                driver = obj.split(".")[0]

                cmds.select(driver, replace=True)

            elif "s" in attribute:
                obj = cmds.connectionInfo(
                    new_const + ".target[0].targetScale", sourceFromDestination=True
                )
                driver = obj.split(".")[0]

                cmds.select(driver, replace=True)

            break
