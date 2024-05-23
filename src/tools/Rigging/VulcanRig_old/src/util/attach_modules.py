"""Attach functions."""

try:
    reload  # Python 2.7
except NameError:
    try:
        from importlib import reload  # Python 3.4+
    except ImportError:
        from imp import reload  # Python 3.0 - 3.3

import os

import maya.cmds as cmds

from . import vulcan_utils as vutil

reload(vutil)


def attachModules():
    """
    This will attach all arm, leg, and neck modules to the spine module.
    Do this after adding your space switches!
    To use: Select all top group nodes of all modules, including the spine
    """
    # Get all modules selected
    allModules = cmds.ls(selection=True)
    spineIndex = allModules.index("C_spine_GRP")
    spineMod = allModules[spineIndex]
    #####################################################################################################
    # Get necessary spine nodes for attaching
    spineChildren = cmds.listRelatives(spineMod, allDescendents=True)
    bindJnts = []
    for node in spineChildren:
        if "chest_CTL" in node:
            chestCtrl = node
        elif "pelvis_CTL" in node:
            pelvisCtrl = node

        # Get all spine bind joint
        if "Bind" in node:
            bindJnts.append(node)

    bindJnts.sort()
    lastSpineJnt = bindJnts[-1]
    print("joe")
    #####################################################################################################
    # Attach arm modules
    # Get all nodes under clavicle module
    clavModules = []
    for md in allModules:
        if "clavicle" in md:
            clavModules.append(md)

    # For each side module, attach to last spine bind joint
    for side in clavModules:
        clavChildren = cmds.listRelatives(side, allDescendents=True)

        # Get clavicle control offset and parent constrain to chest control
        for node in clavChildren:
            if "clavicleOffset" in node:
                cmds.parentConstraint(lastSpineJnt, node, maintainOffset=True)
    print("sarah")
    #####################################################################################################
    # Attach leg modules
    legModules = []
    for md in allModules:
        if "leg" in md:
            legModules.append(md)

    for side in legModules:
        legChildren = cmds.listRelatives(side, allDescendents=True)
        for node in legChildren:
            if "legIK" in node:
                legIkJnt = node
            elif "legBind" in node:
                legBindJnt = node
            elif "legFK_CTL" in node:
                legFKCtrl = node
                legFKOffset = cmds.listRelatives(
                    legFKCtrl, parent=True, type="transform"
                )
        # Parent constrain IK top joint to pelvis control
        cmds.parentConstraint(pelvisCtrl, legIkJnt, maintainOffset=True)
        # Point constrain top Bind joint to the leg FK controller
        cmds.pointConstraint(legFKCtrl, legBindJnt, maintainOffset=True)
        # Parent constrain FK control offset to the pelvis control
        cmds.parentConstraint(pelvisCtrl, legFKOffset, maintainOffset=True)

    #####################################################################################################
    # Attach neck modules
    neckModules = []
    for md in allModules:
        if "neckHead" in md:
            neckModules.append(md)

    for neck in neckModules:
        neckChildren = cmds.listRelatives(neck, allDescendents=True)
        for node in neckChildren:
            if "FKOffset" in node:
                neckOffset = node

        cmds.parentConstraint(lastSpineJnt, neckOffset, maintainOffset=True)

    print("Modules attached to Spine!")
