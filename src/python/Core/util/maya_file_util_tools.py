# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""Various file utility functions for use in Maya."""
# Can't find PySide2 modules pylint: disable=I1101

import logging
import os
import shutil
import stat

from Core import core_paths as cpath
from Core.ui.UIUtilTools.src import pyside_util_tools as put
from . import file_util_tools as fut

from PySide6 import QtCore, QtWidgets

from maya import cmds

LOG = logging.getLogger(os.path.basename(__file__))

from importlib import reload

reload(put)


def create_from_current_scene(save_file_path):
    """Create wip binary file from current scene open in maya.

    Args:
        save_file_path (str): Full path of asset's save location.
    """
    LOG.debug("SAVING FILE PATH: %s", save_file_path)
    # Make sure parent directory of destination file exists
    if os.path.exists(cpath.get_parent_directory(save_file_path, 0)) is False:
        fut.create_directory(cpath.get_parent_directory(save_file_path, 0))

    cmds.file(rename=save_file_path)
    cmds.file(force=True, save=True, options="v=0;", type="mayaBinary")


def create_from_file(source_path: str, destination_path: str):
    """Create wip binary file from file path in UI.

    Args:
        source_path (str): Full path of source file.
        destination_path (str): Full path of new file's location.
    """
    # Make sure parent directory of destination file exists
    if os.path.exists(cpath.get_parent_directory(destination_path, 0)) is False:
        fut.create_directory(cpath.get_parent_directory(destination_path, 0))

    # Copy source file with new shot name to new file location
    shutil.copy2(source_path, destination_path)
    # Make file writable if it's controlled by version control
    os.chmod(destination_path, stat.S_IWRITE)

    # Open new file
    cmds.scriptEditorInfo(suppressWarnings=True, suppressInfo=True, suppressErrors=True)
    cmds.file(
        destination_path, open=True, force=True, options="v=0;", type="mayaBinary"
    )
    cmds.scriptEditorInfo(
        suppressWarnings=False, suppressInfo=False, suppressErrors=False
    )


def create_from_new_scene(save_file_path):
    """Create an empty wip binary file.

    Args:
        save_file_path (str): Full path of asset's save location.
    """
    # Make sure parent directory of destination file exists
    if os.path.exists(cpath.get_parent_directory(save_file_path, 0)) is False:
        fut.create_directory(cpath.get_parent_directory(save_file_path, 0))
    cmds.file(force=True, new=True)
    cmds.file(rename=save_file_path)
    cmds.file(force=True, save=True, options="v=0;", type="mayaBinary")


def open_maya_file(maya_file_path):
    """Open the selected item's maya file.

    Args:
        maya_file_path (str): Path to Maya file to open.
    """
    if not os.path.exists(maya_file_path):
        LOG.warning("Maya file could not be found: %s".self.maya_file_path)
        return

    file_check_state = cmds.file(query=True, modified=True)
    result = "No"
    if file_check_state:
        result = cmds.confirmDialog(
            title="Unsaved Changes",
            message=("There are unsaved changes to the file. Do you want to save?"),
            button=["Yes", "No", "Cancel"],
            defaultButton="Yes",
            cancelButton="Cancel",
            dismissString="Cancel",
        )

    if result == "Cancel":
        return

    if result == "Yes":
        cmds.file(save=True)
        cmds.file(maya_file_path, open=True)
        return

    cmds.file(maya_file_path, open=True, force=True)


def repath_textures(save_directory_path: str, parent_ui_object: QtWidgets.QWidget):
    """Copy and repath the current scenes texture files.

    Copy the current scenes texture files to the destination directory textures
    folder and then repaths the scenes file nodes to the new textures folder paths.

    Args:
        save_directory_path (str): Path to directory where textures will be copied to.
        parent_ui_object (QtWidgets.QWidget): Parent widget object.
    """
    if os.path.exists(save_directory_path) is False:
        fut.create_directory(save_directory_path)

    # Get all file texture nodes
    file_texture_nodes = cmds.ls(type="file")

    num_operations = len(file_texture_nodes)

    texture_progress_bar = put.create_progress_bar(
        "Copying textures...", "Copying textures...", num_operations, parent_ui_object
    )
    QtCore.QCoreApplication.processEvents()
    prog_num = 1

    for texture_node in file_texture_nodes:
        # Get current texture file path
        current_texture_path = cmds.getAttr(texture_node + ".fileTextureName")
        put.update_progress_bar(
            texture_progress_bar,
            f"Copying {prog_num}/{num_operations} texture nodes...",
        )

        # Replace weird or extra slashes that maya generates
        current_texture_path = cleanup_path_slashes(current_texture_path)

        # Check if artist is using UDIM textures
        logging.info("File node: %s", texture_node)
        tiling_mode = cmds.getAttr(texture_node + ".uvTilingMode")

        if tiling_mode == 3:
            copy_udim_textures(
                current_texture_path,
                save_directory_path,
                texture_progress_bar,
                texture_node,
                texture_progress_bar,
            )

        # If not copying UDIM files...
        # If file path doesn't exist, skip...
        if not os.path.isfile(current_texture_path):
            continue

        # Create new texture file path string
        logging.info("Not a UDIM texture...")
        new_file_path = f"{save_directory_path}/{current_texture_path.split('/')[-1]}"

        # Copy file to new file path
        LOG.debug("Copying %s to:\n%s", current_texture_path, new_file_path)
        shutil.copy2(current_texture_path, new_file_path)

        # Make file writable if it's controlled by version control
        os.chmod(new_file_path, stat.S_IWRITE)

        # Repath texture on file node
        cmds.setAttr(texture_node + ".fileTextureName", new_file_path, type="string")
        prog_num += 1

    # Close current sequence shot progress bar
    texture_progress_bar.close()


def get_all_udim_texture_paths(texture_path: str):
    """Get all udim numbered textured paths.

    Args:
        texture_path (str): Path to udim texture

    Returns:
        List of all numbered udim texture paths.
    """
    texture_name = texture_path.split("/")[-1].split(".")[0]
    texture_directory = "/".join(texture_path.split("/")[:-1])
    texture_udim_paths = []
    for item in os.listdir(texture_directory):
        if texture_name in item and ".tx" not in item:
            texture_udim_paths.append(f"{texture_directory}/{item}")

    return texture_udim_paths


def copy_udim_textures(
    current_texture_path: str,
    save_directory_path: str,
    texture_progress_bar: QtWidgets.QProgressDialog,
    texture_node: str,
    parent_ui_object: QtWidgets.QWidget,
):
    """Copy all udim textures to textures folder.

    Args:
        current_texture_path (str): Path of udim texture.
        save_directory_path (str): Path to copy udim texture to.
        texture_progress_bar (QtWidgets.QProgressDialog): Progress
            bar widget texture copying progress.
        texture_node (str): File node.
        parent_ui_object (QtWidgets.QWidget): Parent widget object.
    """
    logging.info("Found UDIM textures...")
    all_udim_paths = get_all_udim_texture_paths(current_texture_path)

    # Start sub progress bar
    number_of_udim_textures = len(all_udim_paths)

    udim_progress_bar = put.create_progress_bar(
        "Found UDIM textures...",
        "Copying UDIM's...",
        number_of_udim_textures,
        parent_ui_object,
    )
    udim_progress_bar.move(
        texture_progress_bar.pos().x(), texture_progress_bar.pos().y() + 105
    )
    udim_num = 1
    QtCore.QCoreApplication.processEvents()

    # Copy each udim file
    for udim_path in all_udim_paths:
        if not os.path.isfile(udim_path):
            udim_num += 1
            continue

        put.update_progress_bar(
            udim_progress_bar,
            (
                f"Copying UDIM texture: {udim_num}/"
                f"{number_of_udim_textures}\n{udim_path.split('/')[-1]}"
            ),
        )

        # Create new texture file path string
        new_file_path = f"{save_directory_path}/{udim_path.split('/')[-1]}"
        # Copy file to new file path
        shutil.copy2(udim_path, new_file_path)
        # Make file writable if it's controlled by version control
        os.chmod(new_file_path, stat.S_IWRITE)

        udim_num += 1

    # Repath texture on UDIM file node
    texture_name = all_udim_paths[0].split("/")[-1].split(".")[0]
    texture_extension = all_udim_paths[0].split(".")[-1]
    new_file_path = f"{save_directory_path}/{texture_name}.<UDIM>.{texture_extension}"
    cmds.setAttr(texture_node + ".fileTextureName", new_file_path, type="string")


def cleanup_path_slashes(filepath: str):
    """Remove extra maya slashes from filepath.

    Maya sometimes returns a weird number of forward
    slashes sometimes. This function will attempt to clean
    them up.

    Args:
        filepath (str): File path string to clean up.

    Returns:
        Cleaned up filepath string.
    """
    if "\\\\" in filepath:
        logging.info("Replacing \\\\ with /")
        filepath = filepath.replace("\\\\", "/")
    elif "\\" in filepath:
        logging.info("Replacing \\ with /")
        filepath = filepath.replace("\\", "/")

    return filepath
