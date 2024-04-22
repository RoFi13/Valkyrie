# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""Various Asset Manager Gui Utility functions."""
# Can't find PySide2 modules pylint: disable=I1101

import logging
import os
import shutil

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QMainWindow

from Core.util import project_util_tools as prj
from Core.ui.UIUtilTools.src import maya_ui_util_tools as mui

from . import asset_list_utils as alu

LOG = logging.getLogger(os.path.basename(__file__))


def set_asset_naming_validators(root_object: QtWidgets.QWidget):
    """Set the asset name and variation line edit object's text validators.

    Args:
        root_object (QtWidgets.QWidget): Main tool window object.
    """
    # asset_name_regex = QtCore.QRegExp(prj.get_project_config_item("asset_name_regex"))
    asset_name_regex = QtCore.QRegularExpression(
        prj.get_project_config_item("asset_name_regex")
    )
    asset_name_text_validator = QtGui.QRegularExpressionValidator(asset_name_regex)

    asset_variant_regex = QtCore.QRegularExpression(
        prj.get_project_config_item("asset_variant_regex")
    )
    asset_variant_text_validator = QtGui.QRegularExpressionValidator(
        asset_variant_regex
    )

    # Assign text validators
    # APB Section
    root_object.line_apb_asset_name.setValidator(asset_name_text_validator)
    root_object.line_apb_variation.setValidator(asset_variant_text_validator)
    # Publish Section
    root_object.line_publish_asset_name.setValidator(asset_name_text_validator)
    root_object.line_publish_variation.setValidator(asset_variant_text_validator)


def set_asset_naming_tooltips(root_object: QtWidgets.QWidget):
    """Set asset and variation line edit's tooltip texts.

    Args:
        root_object (QtWidgets.QWidget): Main tool window object.
    """
    # Asset Prebuild Asset Name
    placeholder_text = "Hover mouse to see valid example..."
    root_object.line_apb_asset_name.setPlaceholderText(placeholder_text)
    root_object.line_apb_variation.setPlaceholderText(placeholder_text)

    asset_name_tooltip = (
        f"Example: "
        f"{prj.get_project_config_item('asset_name_example')}\n"
        f"Invalid Example: "
        f"{prj.get_project_config_item('asset_name_invalid_example')}\n"
        f"First letter must be capitalized. Allowed Characters: "
        f"{prj.get_project_config_item('asset_name_acceptable_characters')}"
    )
    root_object.line_apb_asset_name.setToolTip(asset_name_tooltip)

    # Asset Prebuild Variant Name

    asset_variant_tooltip = (
        f"Example: "
        f"{prj.get_project_config_item('asset_variant_example')}\n"
        f"Invalid Example: "
        f"{prj.get_project_config_item('asset_variant_invalid_example')}\n"
        f"First letter must be capitalized. Allowed Characters: "
        f"{prj.get_project_config_item('asset_variant_acceptable_characters')}"
    )
    # root_object.line_apb_variation.setToolTip(
    #     "Example: Casual\nInvalid Example: Casual_A\n"
    #     "First letter must be capitalized. Allowed Characters: a-z A-Z 0-9"
    # )
    root_object.line_apb_variation.setToolTip(asset_variant_tooltip)

    # Publish section tooltips and placeholder texts
    root_object.line_publish_asset_name.setPlaceholderText(placeholder_text)
    root_object.line_publish_variation.setPlaceholderText(placeholder_text)

    root_object.line_publish_asset_name.setToolTip(asset_name_tooltip)
    root_object.line_publish_variation.setToolTip(asset_variant_tooltip)


def save_qlabel_pixmap_to_disk(label: QtWidgets.QLabel, save_path: str):
    """Save QLabel's pixmap to disk.

    Saves image as .jpg format.

    Args:
        label (QtWidgets.QLabel): QLabel object with pixmap.
        save_path (str): Save path of jpeg image.
    """
    LOG.debug("SAVING QLABEL PIXMAP TO: %s", save_path)
    label.pixmap().save(save_path, "JPG")


def publish_ui_reset(tool_object: QMainWindow):
    """Reset Publish section of the UI to default state.

    Does the following reset:

    1. Reset Publish preview snipping image to default image.
    2. Set check state to unchecked for the Make Image Main Preview.
    3. Clears text for Publish Asset Name field.
    4. Clears text for Publish Asset Variant field.

    Args:
        tool_object (QMainWindow): Main tool window object.
    """
    # Note that publish_preview_widget is created on instantiation and not part of
    # the .ui file.
    tool_object.publish_preview_widget.reset_preview_widget()
    tool_object.root.chk_make_main_preview.setCheckState(QtCore.Qt.CheckState.Unchecked)
    tool_object.root.line_publish_asset_name.setText("")
    tool_object.root.line_publish_variation.setText("")


def set_asset_main_preview(tool_object: QMainWindow):
    """Set the main selected Asset's preview image.

    This deletes the existing asset main preview image and then copies the selected
    publish image displayed on the variation preview.

    Args:
        tool_object (QMainWindow): Main tool window object.mro

    Returns:
        bool: True if successful. Otherwise, False.
    """
    LOG.info("Updating main asset preview...")
    current_selected_asset_name = (
        tool_object.root.list_asset_previews.currentItem().asset_name
    )

    current_variation = tool_object.root.cbo_variations.currentText()

    current_publish_maya_file = (
        tool_object.root.list_published_files.currentItem().maya_file
    )
    current_publish_file_name = current_publish_maya_file.split("/")[-1].split(".")[0]

    if "Select_file_preview" in tool_object.current_variation_preview:
        mui.display_confirm_dialog(
            "Invalid Preview Image",
            (
                "Preview image is invalid. Please select a published version below to "
                "choose a different main preview image."
            ),
        )
        return False

    # Build path to main asset preview
    main_preview_path = tool_object.root.list_asset_previews.currentItem().asset_preview

    if os.access(main_preview_path, os.W_OK) is False:
        mui.display_confirm_dialog(
            "Access Denied",
            (
                "Current Asset Preview is read only. Please unlock file via "
                "version control system or in file properties. File Path:\n\n"
                f"{main_preview_path}"
            ),
        )
        return False

    # Copy the published image to the main asset preview location with new name
    os.remove(main_preview_path)
    shutil.copy2(tool_object.current_variation_preview, main_preview_path)

    # Update asset pixmap
    tool_object.root.list_published_files.blockSignals(True)
    alu.update_asset_list(tool_object)
    tool_object.root.list_published_files.blockSignals(False)

    # Select new/existing asset again to refresh other parts of the UI
    LOG.debug("RE-SELECTING PREVIOUS UI SELECTIONS...")
    for asset in tool_object.root.list_asset_previews.findItems(
        "", QtCore.Qt.MatchRegExp
    ):
        if asset.asset_name != current_selected_asset_name:
            continue
        tool_object.root.list_asset_previews.setCurrentItem(asset)
        tool_object.root.list_asset_previews.itemClicked.emit(asset)
        tool_object.root.cbo_variations.setCurrentText(current_variation)
        tool_object.root.cbo_variations.currentTextChanged.emit(current_variation)
        break

    # Loop through all publish files to find the one that matches the previous
    # selection before switching the asset's main preview image
    for publish in tool_object.root.list_published_files.findItems(
        "", QtCore.Qt.MatchRegExp
    ):
        if publish.maya_file.split("/")[-1].split(".")[0] != current_publish_file_name:
            continue
        tool_object.root.list_published_files.setCurrentItem(publish)
        tool_object.root.list_published_files.itemClicked.emit(publish)
        break

    return True
