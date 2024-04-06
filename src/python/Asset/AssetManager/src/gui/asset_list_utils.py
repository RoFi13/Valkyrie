# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""Asset Manager grid utility functions."""
# Can't find PySide2 modules pylint: disable=I1101

from functools import partial
import logging
import os

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow

from Core import core_paths as cpath
from Core.ui.UIUtilTools.src import pyside_util_tools as put
from Core.util import file_util_tools as fut

from Asset.AssetManager.src.util import asset_manager_utils as amu

from . import asset_widget_item as awi
from . import file_widget_item as fwi

from importlib import reload

reload(fut)
reload(fwi)
reload(awi)
reload(fwi)
reload(amu)

LOADER = QUiLoader()

# Main paths
MAIN_PATHS = cpath.core_paths()

# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 2)}"

# Full path to where resource files are stored
RSRC_PATH = f"{MODULE_PATH}/resources"
ASSET_WIDGET_UI_PATH = f"{RSRC_PATH}/ui/asset_widget.ui"

LOG = logging.getLogger(os.path.basename(__file__))


def update_asset_list(
    tool_object: QMainWindow, *args
):  # Unsure what pylint: disable=unused-argument
    """Update main asset list items.

    Args:
        tool_object (QMainWindow): Main tool window object.
        args: Any extra arguments.
    """
    LOG.debug("Project Assets root directory: %s", tool_object.asset_root_directory)

    tool_object.root.list_asset_previews.clear()

    asset_root_directory = tool_object.asset_root_directory
    asset_category = tool_object.root.cbo_categories.currentText()
    asset_category_path = f"{asset_root_directory}/{asset_category}"

    # Get asset folder names
    asset_names = fut.get_files_or_folders(
        asset_category_path, False, False, "^[a-zA-Z0-9]+$"
    )

    if asset_names is None:
        LOG.warning("No asset folders found in: %s", asset_category_path)
        return

    for asset in asset_names:
        asset_details = {
            "asset_name": None,
            "asset_path": None,
            "asset_preview": None,
            "asset_metadata": None,
            "asset_variations": {},
        }

        asset_details["asset_name"] = asset
        # Get asset path
        asset_path = f"{asset_category_path}/{asset}"
        asset_details["asset_path"] = asset_path
        # Get asset preview
        asset_details["asset_preview"] = amu.get_asset_preview(asset_path, asset)

        amu.get_asset_variations(asset_details)

        add_asset_widget(tool_object, asset_details)


def add_asset_widget(tool_object: QMainWindow, asset_details: dict):
    """Add Asset as widget to main asset list widget.

    Args:
        tool_object (QMainWindow): Asset Manager tool object.
        asset_details (dict): Asset detailed information in the following format:
        {
            "asset_name": (str) Asset Name,
            "asset_path": (str) Path to root of Asset folder,
            "asset_preview": (str) Path to asset jpg preview image,
            "asset_metadata": (str) Path to asset metadata JSON file,
            "asset_variations": {
                "<variation_name>": {
                    "published_versions": {
                        "<version>": {
                            "maya_file": "/path/to/published_maya_file.mb",
                            "version_preview": "path/to/published_preview_image.jpg"
                        }
                    },
                    "apb_versions": (list(str)) Paths to all wip/apb maya files for
                        variation.
                    }
                }
            }
        }

    Returns:
        QListWidgetItem: New list widget item for Asset.
    """
    asset_widget_path = tool_object.ui_settings["asset_widget"]

    # Add widget to list widget
    LOG.info("Adding new shot widget...")
    asset_main_widget = LOADER.load(asset_widget_path, tool_object)
    # Add new item to list widget
    new_asset_item = awi.AssetWidgetItem(
        tool_object.root.list_asset_previews, asset_details, tool_object
    )
    # Set vertical size of new item
    new_asset_item.setSizeHint(QtCore.QSize(128, 144))

    # Add new widget
    tool_object.root.list_asset_previews.addItem(new_asset_item)
    tool_object.root.list_asset_previews.setItemWidget(
        new_asset_item, asset_main_widget
    )

    # Set text and images for new widget
    asset_pixmap = QtGui.QPixmap(asset_details["asset_preview"])
    asset_main_widget.lbl_asset_preview.setPixmap(asset_pixmap)
    asset_main_widget.lbl_asset_preview.setScaledContents(True)

    # Set asset name
    asset_main_widget.lbl_asset_name.setText(asset_details["asset_name"])

    return new_asset_item


def add_file_widget(
    selected_asset_item: QtWidgets.QListWidgetItem,
    version_details: dict,
    is_published_asset: bool = False,
):
    """Add file widget item to specific list widget.

    Args:
        selected_asset_item (QtWidgets.QListWidgetItem): Selected Asset Widget item.
        version_details (dict): Version details of either Published or APB versions.
            {
                "<version>":{
                    "maya_file": "../Path/to/published_maya_file.mb"
                    "version_preview": "../Path/to/published_preview.jpg"
                }
            }
        is_published_asset (bool, optional): _description_. Defaults to False.
    """
    file_widget_path = selected_asset_item.tool_object.ui_settings["file_widget"]
    maya_filename = version_details["maya_file"].split("/")[-1].split(".")[0]

    list_to_populate = selected_asset_item.tool_object.root.list_published_files
    if is_published_asset is False:
        LOG.info("Adding maya file to APB list widget...")
        list_to_populate = selected_asset_item.tool_object.root.list_apb_files

    # Add widget to list widget
    LOG.info("Adding new file widget...")
    file_main_widget = LOADER.load(file_widget_path, selected_asset_item.tool_object)
    # Add new item to list widget
    new_asset_item = fwi.FileWidgetItem(
        list_to_populate, selected_asset_item, version_details, maya_filename
    )

    # Set vertical size of new item
    new_asset_item.setSizeHint(QtCore.QSize(128, 39))

    # Add new widget
    LOG.debug("Updating LIST WIDGET: %s", list_to_populate)
    list_to_populate.addItem(new_asset_item)
    list_to_populate.setItemWidget(new_asset_item, file_main_widget)

    # Set asset name
    file_main_widget.lbl_file_name.setText(maya_filename)

    # Set up signals for file widget
    file_main_widget.btn_open.clicked.connect(partial(new_asset_item.open_file))
    file_main_widget.btn_pre_build.clicked.connect(
        partial(new_asset_item.fill_pre_build_details)
    )


def update_variation_preview(selected_item: fwi.FileWidgetItem):
    """Update variation preview image.

    Args:
        selected_item (fwi.FileWidgetItem): File Widget selected.
    """
    put.set_label_pixmap(
        selected_item.root_object.lbl_variation_preview, selected_item.version_preview
    )


def asset_selection_changed(selected_item: awi.AssetWidgetItem):
    """Update Published and APB list widgets based on Asset Widget selection.

    Args:
        selected_item (awi.AssetWidgetItem): Asset Widget selected.
    """
    # Update variations combobox options
    amu.update_variation_options(selected_item)
    # Clear preview image
    put.set_label_pixmap(
        selected_item.root_object.lbl_variation_preview,
        f"{RSRC_PATH}/images/Select_file_preview.png",
    )
    # Update variation preview path
    selected_item.tool_object.current_variation_preview = (
        f"{RSRC_PATH}/images/Select_file_preview.png"
    )


def asset_variation_changed(tool_object: QMainWindow, selected_variation: str):
    """Update publish and APB file versions in their respective lists.

    Args:
        tool_object (QMainWindow): Main tool window object.
        selected_variation (str): Selected variation text.
    """
    LOG.info("Selected variation: %s", selected_variation)

    selected_item = tool_object.root.list_asset_previews.selectedItems()[0]

    # Update published versions
    amu.update_publish_file_list(selected_item)

    # Update apb/wip versions
    amu.update_apb_versions(selected_item)


def publish_selection_changed(selected_item: fwi.FileWidgetItem):
    """Execute when selection changes on Publish File Widget.

    Args:
        selected_item (fwi.FileWidgetItem): File widget selected.
    """
    update_variation_preview(selected_item)
    # Update variation preview path
    selected_item.tool_object.current_variation_preview = selected_item.version_preview