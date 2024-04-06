# Copyright (C) 2023 DNEG - All Rights Reserved.
"""This module sets FBX export options."""

import logging

from maya import cmds, mel

LOG = logging.getLogger("fbx_export_settings")


def set_fbx_export_options(export_options=-1):
    """
    Set the export settings for specific object type i.e. cam or rig.

    Args:
        export_options (int):
            0: Export Skeletal Mesh Rig
            1: Export Static Mesh
            2: Export Camera
            3: Export Skeletal Mesh Rig with Animation
    """
    LOG.info("Export settings: %s", str(export_options))
    if export_options == -1:
        LOG.warning("Please enter an integer between 0-3 as a parameter.")
        return

    if export_options == 0:
        # Export a skeletal mesh rig no animation
        set_options_rig()
    elif export_options == 1:
        # Exporting just static mesh
        set_options_static_mesh()
    elif export_options == 2:
        # Exporting the camera animation
        set_options_camera()
    elif export_options == 3:
        # Export Skeletal mesh rig with animation
        set_options_rig_with_anim()


def set_options_rig():
    """Set options to export the skeletal mesh and rig with no animation."""
    LOG.info("Setting FBX Export settings for Skeletal Mesh with no animation...")
    mel.eval("FBXExportTriangulate -v false")
    # Mesh
    mel.eval("FBXExportSmoothingGroups -v true")
    mel.eval("FBXExportHardEdges -v false")
    mel.eval("FBXExportTangents -v true")
    mel.eval("FBXExportInstances -v false")
    mel.eval("FBXExportInAscii -v false")
    mel.eval("FBXExportSmoothMesh -v false")
    # Animation
    mel.eval("FBXExportAnimationOnly -v false")
    mel.eval("FBXExportReferencedAssetsContent -v true")
    mel.eval("FBXExportUseSceneName -v false")
    mel.eval("FBXExportQuaternion -v quaternion")
    mel.eval("FBXExportShapes -v true")
    mel.eval("FBXExportSkins -v true")
    mel.eval("FBXExportQuaternion -v resample")
    mel.eval("FBXExportUpAxis y")
    # FBX version
    mel.eval("FBXExportFileVersion -v FBX201800")
    # Constraints
    mel.eval("FBXExportConstraints -v false")
    # Cameras
    mel.eval("FBXExportCameras -v false")
    # Lights
    mel.eval("FBXExportLights -v false")
    # Embed Media
    mel.eval("FBXExportEmbeddedTextures -v false")
    # Connections
    mel.eval("FBXExportInputConnections -v false")


def set_options_static_mesh():
    """Set options to export the static mesh."""
    LOG.info("Setting FBX Export settings for Static Mesh...")
    mel.eval("FBXExportTriangulate -v true")
    # Mesh
    mel.eval("FBXExportSmoothingGroups -v true")
    mel.eval("FBXExportHardEdges -v false")
    mel.eval("FBXExportTangents -v false")
    mel.eval("FBXExportInstances -v false")
    mel.eval("FBXExportInAscii -v false")
    mel.eval("FBXExportSmoothMesh -v true")
    # Animation
    mel.eval("FBXExportAnimationOnly -v false")
    mel.eval("FBXExportReferencedAssetsContent -v true")
    mel.eval("FBXExportUseSceneName -v false")
    mel.eval("FBXExportShapes -v true")
    mel.eval("FBXExportSkins -v true")
    mel.eval("FBXExportQuaternion -v resample")
    mel.eval("FBXExportUpAxis y")
    # FBX version
    mel.eval("FBXExportFileVersion -v FBX201800")
    # Constraints
    mel.eval("FBXExportConstraints -v false")
    # Cameras
    mel.eval("FBXExportCameras -v false")
    # Lights
    mel.eval("FBXExportLights -v false")
    # Embed Media
    mel.eval("FBXExportEmbeddedTextures -v false")
    # Connections
    mel.eval("FBXExportInputConnections -v false")


def set_options_camera():
    """Set options to export camera animation."""
    LOG.info("Setting FBX Export settings for Camera Animation...")
    mel.eval("FBXExportTriangulate -v false")
    mel.eval("FBXExportSmoothingGroups -v false")
    mel.eval("FBXExportHardEdges -v false")
    mel.eval("FBXExportTangents -v false")
    mel.eval("FBXExportInstances -v false")
    mel.eval("FBXExportInAscii -v false")
    mel.eval("FBXExportSmoothMesh -v false")

    # Animation
    mel.eval("FBXExportBakeResampleAnimation -v true")
    mel.eval("FBXExportBakeComplexAnimation -v true")
    mel.eval(
        "FBXExportBakeComplexStart -v "
        + str(cmds.playbackOptions(minTime=True, query=True))
    )
    mel.eval(
        "FBXExportBakeComplexEnd -v "
        + str(cmds.playbackOptions(maxTime=True, query=True))
    )
    mel.eval("FBXExportReferencedAssetsContent -v false")
    mel.eval("FBXExportBakeComplexStep -v 1")
    mel.eval("FBXExportUseSceneName -v false")
    mel.eval("FBXExportShapes -v true")
    mel.eval("FBXExportSkins -v false")
    mel.eval("FBXExportQuaternion -v resample")
    mel.eval("FBXExportUpAxis y")
    # FBX version
    mel.eval("FBXExportFileVersion -v FBX201800")
    # Constraints
    mel.eval("FBXExportConstraints -v false")
    # Cameras
    mel.eval("FBXExportCameras -v true")
    # Lights
    mel.eval("FBXExportLights -v false")
    # Embed Media
    mel.eval("FBXExportEmbeddedTextures -v false")
    # Connections
    mel.eval("FBXExportInputConnections -v false")


def set_options_rig_with_anim():
    """Set options to export the skeletal mesh rig with its animation."""
    LOG.info("Setting FBX Export settings for Skeletal Mesh with animation...")
    mel.eval("FBXExportTriangulate -v false")
    # Mesh
    mel.eval("FBXExportSmoothingGroups -v true")
    mel.eval("FBXExportHardEdges -v false")
    mel.eval("FBXExportTangents -v true")
    mel.eval("FBXExportInstances -v false")
    mel.eval("FBXExportInAscii -v false")
    mel.eval("FBXExportSmoothMesh -v false")
    # Animation
    mel.eval("FBXExportBakeResampleAnimation -v true")
    mel.eval("FBXExportBakeComplexAnimation -v true")
    mel.eval(
        "FBXExportBakeComplexStart -v "
        + str(cmds.playbackOptions(minTime=True, query=True))
    )
    mel.eval(
        "FBXExportBakeComplexEnd -v "
        + str(cmds.playbackOptions(maxTime=True, query=True) + 1)
    )
    mel.eval("FBXExportReferencedAssetsContent -v true")
    mel.eval("FBXExportBakeComplexStep -v 1")
    mel.eval("FBXExportUseSceneName -v false")
    mel.eval("FBXExportQuaternion -v quaternion")
    mel.eval("FBXExportShapes -v true")
    mel.eval("FBXExportSkins -v true")
    mel.eval("FBXExportQuaternion -v resample")
    mel.eval("FBXExportUpAxis y")
    # FBX version
    mel.eval("FBXExportFileVersion -v FBX201800")
    # Constraints
    mel.eval("FBXExportConstraints -v false")
    # Cameras
    mel.eval("FBXExportCameras -v false")
    # Lights
    mel.eval("FBXExportLights -v false")
    # Embed Media
    mel.eval("FBXExportEmbeddedTextures -v false")
    # Connections
    mel.eval("FBXExportInputConnections -v false")
