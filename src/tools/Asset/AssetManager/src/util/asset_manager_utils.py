# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""Asset Manager general utility functions."""
# Can't find PySide2 modules pylint: disable=I1101

import logging
import os

from PySide6 import QtGui
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow

from Core.util import file_util_tools as fut
from Core.util import project_util_tools as prj

from Asset.AssetManager.src.gui import asset_list_utils as alu
from Asset.AssetManager.src.gui import asset_widget_item as awi
from Asset.AssetManager.src.gui import file_widget_item as fwi
from Asset.AssetManager.src.util import valkyrie_asset as val

LOADER = QUiLoader()

LOG = logging.getLogger(os.path.basename(__file__))

PROJECT_CONFIGS = prj.get_project_configs()


def get_asset_preview(asset_path: str, asset_name: str):
    """Get main Asset preview image.

    Args:
        asset_path (str): Path to Asset root folder.
        asset_name (str): Asset Name.

    Returns:
        str: Path to main asset preview image.
    """
    asset_preview_path = f"{asset_path}/{asset_name}_preview.jpg"
    LOG.debug("MAIN ASSET PREVIEW PATH: %s", asset_preview_path)
    if os.path.exists(asset_preview_path) is False:
        LOG.warning("No asset preview image found at path: %s", asset_preview_path)
        return None

    return asset_preview_path


def get_asset_variations(asset_object: val.ValkyrieAsset):
    """Get all variations of a specific Asset.

    Args:
        asset_object (dict): Asset dictionary to be modified with gathered data.
    """
    LOG.debug("ASSET PATH TO GET VARIATIONS: %s", asset_object.get_asset_path())
    variations = fut.get_files_or_folders(
        asset_object.get_asset_path(), False, True, "[a-zA-Z]+"
    )
    if not variations:
        return

    for variation_path in variations:
        LOG.debug("VARIATION PATH: %s", variation_path)
        variation_name = variation_path.split("/")[-1]

        asset_object.add_asset_variant(variation_name, variation_path)


def update_variation_options(item_selected: awi.AssetWidgetItem):
    """Update variations combobox with Asset variations.

    Args:
        item_selected (awi.AssetWidgetItem): Custom QListWidgetItem object.
    """
    LOG.info("Updating variation options...")
    # Temporarily block the signals being sent. Key error pops up after clearing combo.
    item_selected.root_object.cbo_variations.blockSignals(True)
    item_selected.root_object.cbo_variations.clear()
    item_selected.root_object.cbo_variations.blockSignals(False)

    for variation in item_selected.get_variation_names():
        LOG.debug("Variation chosen: %s", variation)
        item_selected.root_object.cbo_variations.addItem(variation)

    item_selected.root_object.cbo_variations.setCurrentIndex(0)


def update_publish_file_list(item_selected: awi.AssetWidgetItem):
    """Update list of published file widgets.

    Args:
        item_selected (awi.AssetWidgetItem): Asset widget selected to grab details from.
    """
    item_selected.root_object.list_published_files.clear()

    variation = item_selected.root_object.cbo_variations.currentText()
    for version, version_details in item_selected.get_published_maya_files(
        variation
    ).items():
        LOG.info(
            "Adding file widget for %s version of maya file: %s",
            version,
            version_details["maya_file"],
        )
        alu.add_file_widget(item_selected, version_details, True)


def update_apb_versions(item_selected: awi.AssetWidgetItem):
    """Update APB versions list of widgets.

    Args:
        item_selected (awi.AssetWidgetItem): Asset widget selected to grab details from.
    """
    item_selected.root_object.list_apb_files.clear()

    variation = item_selected.root_object.cbo_variations.currentText()
    for maya_file_path in item_selected.asset_variations[variation].get_apb_versions():
        LOG.debug("APB Maya file: %s", maya_file_path)
        version_details = {"maya_file": maya_file_path, "version_preview": ""}
        alu.add_file_widget(item_selected, version_details, False)


def update_variation_preview(item_selected: fwi.FileWidgetItem):
    """Update Variation Preview QLabel image.

    Args:
        item_selected (fwi.FileWidgetItem): File widget to grab image details from.
    """
    LOG.info("Updating variation preview...")
    variation_preview_path = item_selected.get_published_preview_image(
        item_selected.root_object.cbo_variations.currentText()
    )
    LOG.info("Variation preview path: %s", variation_preview_path)
    variation_pixmap = QtGui.QPixmap(variation_preview_path)
    item_selected.root_object.lbl_variation_preview.setPixmap(variation_pixmap)
    item_selected.root_object.lbl_variation_preview.setScaledContents(True)


def update_create_from_type(tool_object: QMainWindow, selected_text: str):
    """Toggle enabled for custom file path UI elements.

    Args:
        tool_object (QMainWindow): Main tool window object.
        selected_text (str): New Combobox selected text.
    """
    if selected_text == "File":
        tool_object.root.lbl_apb_file.setEnabled(True)
        tool_object.root.line_apb_file_path.setEnabled(True)
        tool_object.root.btn_apb_browse.setEnabled(True)
        return

    tool_object.root.lbl_apb_file.setEnabled(False)
    tool_object.root.line_apb_file_path.setEnabled(False)
    tool_object.root.btn_apb_browse.setEnabled(False)


def get_asset_creation_details(tool_object: QMainWindow, is_publish: bool = False):
    """Get UI APB asset details.

    Args:
        tool_object (QMainWindow): Tool object window.
        is_publish (bool): Whether to get APB UI details or Publish UI details.

    Returns:
        dict: Asset details as follows:
            {"asset_category" (str): Name of Asset Category,
            "asset_name" (str): Name of Asset,
            "asset_variant" (str): Name of Asset Variant,
            "file_path" (str): File path if chosen. Otherwise is None.}
    """
    asset_details = {
        "asset_category": tool_object.root.cbo_apb_asset_type.currentText(),
        "asset_name": tool_object.root.line_apb_asset_name.text(),
        "asset_variant": tool_object.root.line_apb_variation.text(),
        "file_path": None,
    }

    if tool_object.root.cbo_apb_create_from.currentText() == "File":
        asset_details["file_path"] = tool_object.root.line_apb_file_path.text()

    if is_publish is True:
        asset_details = {
            "asset_category": tool_object.root.cbo_publish_asset_type.currentText(),
            "asset_name": tool_object.root.line_publish_asset_name.text(),
            "asset_variant": tool_object.root.line_publish_variation.text(),
            "file_path": None,
        }

    return asset_details


def shorten_category_name(long_name: str):
    """Get shortened asset category name.

    Args:
        long_name (str): Long category name.

    Returns:
        str: Shortened category name i.e. characters -> chr
    """
    LOG.debug("Shortening category name for: %s", long_name)
    if long_name == "assembled":
        short_name = "asb"
    if long_name == "characters":
        short_name = "chr"
    if long_name == "creatures":
        short_name = "cre"
    if long_name == "environments":
        short_name = "env"
    if long_name == "gami":
        short_name = "gam"
    if long_name == "props":
        short_name = "prp"
    if long_name == "vehicles":
        short_name = "veh"

    return short_name
