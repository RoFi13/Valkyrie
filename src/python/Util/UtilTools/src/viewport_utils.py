# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""Various functions to move and orient selected objects in Maya."""

import logging
import os

from maya import cmds, mel

LOG = logging.getLogger(os.path.basename(__file__))


def toggle_isolate_selection():
    """Toggle the selected objects to be isolated or not in viewport."""
    main_model_panel = cmds.getPanel(withFocus=True)

    if cmds.isolateSelect(main_model_panel, query=True, state=True):
        mel.eval("enableIsolateSelect " + main_model_panel + " 0")
    else:
        mel.eval("enableIsolateSelect " + main_model_panel + " 1")


def viewport_polygons_main():
    """Set attributes for main visable polygons."""
    cmds.setAttr("hardwareRenderingGlobals.multiSampleEnable", 0)
    cmds.setAttr("hardwareRenderingGlobals.ssaoEnable", 0)
    cmds.modelEditor(
        "modelPanel4",
        edit=True,
        displayAppearance="smoothShaded",
        displayLights="default",
        displayTextures=True,
        polymeshes=True,
        headsUpDisplay=True,
        shadows=False,
        nurbsCurves=False,
        nurbsSurfaces=False,
        lights=False,
        cameras=False,
        grid=False,
        joints=False,
        ikHandles=False,
        locators=False,
        controlVertices=True,
        hulls=False,
        subdivSurfaces=False,
        planes=False,
        imagePlane=False,
        dynamics=True,
        fluids=False,
        hairSystems=False,
        follicles=False,
        nCloths=False,
        nParticles=True,
        nRigids=False,
        dynamicConstraints=False,
        dimensions=False,
        pivots=False,
        handles=False,
        textures=False,
        particleInstancers=True,
        strokes=False,
        motionTrails=False,
        clipGhosts=False,
        greasePencils=False,
        selectionHiliteDisplay=True,
        deformers=False,
    )
    cmds.selectType(
        nurbsSurface=True, plane=True, polymesh=True, byName=["gpuCache", True]
    )


def viewport_work_main():
    """Set attributes for main working environment."""
    cmds.setAttr("hardwareRenderingGlobals.multiSampleEnable", 0)
    cmds.setAttr("hardwareRenderingGlobals.ssaoEnable", 0)
    cmds.modelEditor(
        "modelPanel4",
        edit=True,
        displayAppearance="smoothShaded",
        displayLights="default",
        displayTextures=True,
        polymeshes=True,
        headsUpDisplay=True,
        shadows=False,
        nurbsCurves=True,
        nurbsSurfaces=False,
        lights=True,
        cameras=True,
        grid=True,
        joints=False,
        ikHandles=False,
        locators=True,
        controlVertices=True,
        hulls=False,
        subdivSurfaces=False,
        planes=False,
        imagePlane=False,
        dynamics=True,
        fluids=False,
        hairSystems=False,
        follicles=False,
        nCloths=False,
        nParticles=True,
        nRigids=False,
        dynamicConstraints=False,
        dimensions=False,
        pivots=True,
        handles=False,
        textures=False,
        particleInstancers=True,
        strokes=True,
        motionTrails=True,
        pluginShapes=False,
        clipGhosts=False,
        greasePencils=False,
        pluginObjects=("gpuCacheDisplayFilter", True),
        selectionHiliteDisplay=True,
        deformers=False,
    )
    cmds.selectType(
        nurbsSurface=False, plane=False, polymesh=False, byName=["gpuCache", False]
    )
