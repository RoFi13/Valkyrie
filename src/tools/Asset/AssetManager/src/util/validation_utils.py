# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""Various validation checks and utility functions."""
# Can't find PySide2 modules pylint: disable=I1101

import logging
import os
import re

from PySide6.QtWidgets import QMainWindow

from Core.util import project_util_tools as prj
from Core.ui.UIUtilTools.src import maya_ui_util_tools as mui

from maya import cmds

# from PySide2.QtWidgets import QMainWindow

LOG = logging.getLogger(os.path.basename(__file__))

PROJECT_CONFIGS = prj.get_project_configs()


def validate_asset_details(asset_details: dict, tool_object: QMainWindow = None):
    """Validate the APB build UI details to meet project naming convention standards.

    Args:
        asset_details (dict): Asset details data in following format:
        {
            "asset_category" (str): "Name of Asset Category,
            "asset_name" (str): Name of Asset,
            "asset_variant" (str): Name of Asset Variant,
            "file_path" (str): File path if chosen. Otherwise is None
        }
        tool_object (QMainWindow): Main tool window object.

    Returns:
        bool: True if all APB UI details are valid. Otherwise, return False.
    """
    is_valid = True

    if validate_valid_file(asset_details) is False:
        is_valid = False

    if validate_name(asset_details["asset_name"], "Asset Name") is False:
        is_valid = False

    if validate_name(asset_details["asset_variant"], "Asset Variant") is False:
        is_valid = False

    if tool_object is not None:
        if validate_publish_preview(tool_object) is False:
            is_valid = False

    return is_valid


def validate_name(name: str, name_part: str = "Asset Name"):
    """Validate name for asset parts based on naming convention pattern.

    Args:
        name (str): Name to check.
        name_part (str, optional): Whether the part to check is either the Asset Name
            or Asset Variant. Defaults to "Asset Name".

    Returns:
        bool: Return True if name is valid for project naming conventions. Otherwise,
            False.
    """
    if len(name) < 2:
        LOG.warning("Text is too short for %s", name_part)
        return False

    name_regex = PROJECT_CONFIGS["asset_name_regex"]
    if name_part == "Asset Variant":
        name_regex = PROJECT_CONFIGS["asset_variant_regex"]

    if re.match(name_regex, name) is None:
        LOG.warning(
            "%s doesn't match project naming convention for %s.", name, name_part
        )
        return False

    return True


def validate_valid_file(asset_details: dict):
    """Verify that file to be created from exists.

    Args:
        asset_details (dict): Asset details data in following format:
        {
            "asset_category" (str): "Name of Asset Category,
            "asset_name" (str): Name of Asset,
            "asset_variant" (str): Name of Asset Variant,
            "file_path" (str): File path if chosen. Otherwise is None
        }

    Returns:
        bool: Return True if file path is valid. Otherwise, return False.
    """
    if asset_details["file_path"] is None:
        return True

    if os.path.exists(asset_details["file_path"]) is False:
        LOG.warning("Failed to find file at path: %s", asset_details["file_path"])
        return False

    return True


def validate_publish_preview(tool_object: QMainWindow):
    """Validate publish preview image is not the default one.

    User must use the snipping tool to create a new valid image for the Asset preview.

    Args:
        tool_object (QMainWindow): Main tool window object.

    Returns:
        bool: Return False if the default snipping tool image is the preview image.
            Otherwise, return True.
    """
    # Get grab preview qlabel widget
    grab_preview_widget = tool_object.root.publish_section_HL.itemAt(0).widget()

    # Preview image is default. User must grab a preview of the asset before publishing
    if "Snapshot_Default" in grab_preview_widget.current_image_path:
        cmds.confirmDialog(
            title="No Preview Image",
            message="Please create a preview image of the asset.",
            button=["Ok"],
            defaultButton="Ok",
            cancelButton="Ok",
            dismissString="Ok",
        )
        return False

    return True


def confirm_publish_details(asset_details: dict, publish_details: dict):
    """Confirm with user about publish details.

    Args:
        asset_details (dict): Asset details data in following format:
        {
            "asset_category" (str): "Name of Asset Category,
            "asset_name" (str): Name of Asset,
            "asset_variant" (str): Name of Asset Variant,
            "file_path" (str): File path if chosen. Otherwise is None
        },
        publish_details (dict): Publish details data in following format:
        {
            "version": Version string i.e. "v001",
            "file_path": Final maya file path name,
            "textures_directory": Publish textures version directory
                i.e. Publish/v001/Textures
        }
    """
    confirm_msg = (
        "Publishing Asset with the following information:\n"
        "--------------------------------------------------\n"
        f"Asset Category: {asset_details['asset_category']}\n"
        f"Asset Name: {asset_details['asset_name']}\n"
        f"Asset Variant: {asset_details['asset_variant']}\n"
        f"Publish Version: {publish_details['version']}\n"
        "--------------------------------------------------\n"
        "Are these publish details correct?"
    )
    result = mui.display_confirm_dialog(
        "Confirm Publish", confirm_msg, ["Publish", "Cancel"], "Cancel"
    )
    if result == "Cancel":
        return False

    return True
