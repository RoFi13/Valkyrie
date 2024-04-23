# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""Custom File Widget QListWidgetItem class."""

# Can't find PySide2 modules pylint: disable=I1101

import logging
import os

from PySide6 import QtWidgets

from Core import core_paths as cpath
from Core.util import maya_file_util_tools as mut

from . import asset_widget_item as awi

# Main paths
MAIN_PATHS = cpath.core_paths()

# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 2)}"

# Full path to where resource files are stored
RSRC_PATH = f"{MODULE_PATH}/resources"

LOG = logging.getLogger(os.path.basename(__file__))


class FileWidgetItem(QtWidgets.QListWidgetItem):
    """Tool for custom file widget list item."""

    def __init__(
        self,
        parent_object: QtWidgets.QListWidget,
        asset_widget: awi.AssetWidgetItem,
        version_details: dict,
        maya_filename: str,
    ):
        super().__init__(parent_object)
        LOG.debug("FILE WIDGET VERSION DETAILS: %s", version_details)
        self.parent_object = parent_object
        self.asset_widget = asset_widget
        self.tool_object = self.asset_widget.tool_object
        self.root_object = self.tool_object.root

        self.maya_file = version_details["maya_file"]
        self.version_preview = version_details["version_preview"]

        self.asset_name = maya_filename.split("_")[2]
        self.asset_variant = maya_filename.split("_")[3]
        self.asset_version = maya_filename.split("_")[-1]

    def get_published_preview_image(self):
        """Retrieve Published Asset's preview image path.

        Returns:
            str: Path to jpg image file.
        """
        return self.asset_widget.get_published_preview_image(
            self.root_object.cbo_variations.currentText()
        )

    def open_file(self):
        """Open widget's maya file."""
        mut.open_maya_file(self.maya_file)

    def fill_pre_build_details(self):
        """Fill in APB UI details with this asset's data."""
        self.root_object.cbo_apb_asset_type.setCurrentText(
            self.root_object.cbo_categories.currentText()
        )
        self.root_object.line_apb_asset_name.setText(self.asset_name)
        self.root_object.line_apb_variation.setText(self.asset_variant)
        self.root_object.cbo_apb_create_from.setCurrentText("File")
        self.root_object.line_apb_file_path.setText(self.maya_file)

        # Set the tab to the APB tab
        self.root_object.tab_builds.setCurrentIndex(0)
