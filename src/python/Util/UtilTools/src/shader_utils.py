# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""Various maya shader utility functions."""
# Can't find PySide2 modules pylint: disable=I1101

import logging
import os

from maya import cmds

LOG = logging.getLogger(os.path.basename(__file__))


def select_shader(action="Select"):
    """Select the shader or get selected object's shader.

    Args:
        action (str):   What to return. Options are "Select" and "Get".

    Return:
        Return True if shader was selected. Otherwise, return the shader node.
    """
    # Get selection; first selection is the object shader you want to share,
    # second object is where the shader is going to be applied.
    selection = cmds.ls(selection=True)

    if len(selection) > 1:
        LOG.error("Please select only one object.")
        return False

    # Get shapes of selection:
    driver_shape_node = cmds.ls(selection, dagObjects=1, objectsOnly=1, shapes=1)
    # Get shading groups from shapes:
    driver_shading_groups = cmds.listConnections(
        driver_shape_node, type="shadingEngine"
    )
    # Get the shaders:
    driver_shaders = cmds.ls(
        cmds.listConnections(driver_shading_groups), materials=True
    )

    if driver_shaders:
        driver_shader = driver_shaders[0]
    else:
        driver_shader = None

    if action == "Get":
        return driver_shader

    cmds.select(driver_shader, replace=True)
    return True


def share_shader():
    """Assign selected object's shader to second selected object."""
    # Get selection; first selection is the object shader you want to share,
    # second object is where the shader is going to be applied.
    selection = cmds.ls(selection=True)

    if len(selection) < 2:
        LOG.error("Please select at least two objects.")
        return

    # Get the shading engine of the driver object
    driver_shape_node = cmds.ls(
        selection[0], dagObjects=True, objectsOnly=True, shapes=True
    )
    driver_shading_group = cmds.listConnections(
        driver_shape_node, type="shadingEngine"
    )[0]

    # Get the shader assigned to the driver object
    driver_shader = cmds.listConnections(driver_shading_group + ".surfaceShader")[0]

    # Assign the shader to the remaining objects
    for node in selection[1:]:
        cmds.select(node, replace=True)
        shading_group = cmds.sets(
            renderable=True, noSurfaceShader=True, empty=True, name=node + "SG"
        )
        cmds.connectAttr(
            driver_shader + ".outColor", shading_group + ".surfaceShader", force=True
        )
        cmds.sets(node, edit=True, forceElement=shading_group)
