# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""Custom Asset Widget QListWidgetItem class."""
# Can't find PySide2 modules pylint: disable=I1101

import logging
import os

from PySide6 import QtWidgets
from PySide6.QtWidgets import QMainWindow

from Core import core_paths as cpath

from Asset.AssetManager.src.util import valkyrie_asset as val

# Main paths
MAIN_PATHS = cpath.core_paths()

# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 2)}"

# Full path to where resource files are stored
RSRC_PATH = f"{MODULE_PATH}/resources"

LOG = logging.getLogger(os.path.basename(__file__))


class AssetWidgetItem(QtWidgets.QListWidgetItem):
    """Tool for custom asset list item."""

    def __init__(
        self,
        parent_object: QtWidgets.QListWidget,
        asset_object: val.ValkyrieAsset,
        tool_object: QMainWindow,
    ):
        super().__init__(parent_object)
        self.parent_object = parent_object
        self.tool_object = tool_object
        self.root_object = tool_object.root

        self._valkyrie_asset = asset_object
        self.asset_name: str
        self.asset_path: str
        self.asset_preview: str
        self.asset_metadata: str
        self.asset_variations: dict

        self.set_asset_details()

    def set_valkyrie_asset(self, new_asset_object: val.ValkyrieAsset):
        self._valkyrie_asset = new_asset_object

    def get_valkyrie_asset(self):
        return self._valkyrie_asset

    def set_asset_details(self):
        """Set list widget item's asset details."""
        self.asset_name = self._valkyrie_asset.get_asset_name()
        self.asset_path = self._valkyrie_asset.get_asset_path()
        self.asset_preview = self._valkyrie_asset.get_asset_preview_path()
        self.asset_metadata = self._valkyrie_asset.get_asset_metadata_path()
        self.asset_variations = self._valkyrie_asset.get_all_asset_variants()

    def get_variation_names(self):
        """Get asset variation names.

        Returns:
            list(str): List of variation names.
        """
        return self.asset_variations.keys()

    def get_published_maya_files(self, variation: str):
        """Get dict of published maya asset file paths.

        Args:
            variation (str): Asset variation to find published versions.

        Returns:
            dict: Dictionary of published maya file paths with versions and version
                previews in the following format:
                {
                    "<version>":{
                        "maya_file": "../Path/to/published_maya_file.mb"
                        "version_preview": "../Path/to/published_preview.jpg"
                    }
                }
        """
        if len(self.asset_variations) == 0:
            LOG.warning("Asset Item '%s' has no valid variations.", self.asset_name)
            return {}

        published_versions = self.asset_variations[variation].get_published_versions()
        maya_file_details = {}
        for version, version_details in published_versions.items():
            LOG.info(
                "Getting %s variation published maya file for version: %s...",
                variation,
                version,
            )
            maya_file_details[version] = {
                "maya_file": version_details["maya_file"],
                "version_preview": version_details["version_preview"],
            }

        return maya_file_details

    def get_apb_maya_files(self, variation: str):
        """Get dict of apb/wip maya asset file paths.

        Args:
            variation (str): Asset variation to find apb/wip versions.

        Returns:
            dict: Dictionary of apb/wip maya file paths with versions and version
                previews in the following format:
                {
                    "<version>":{
                        "maya_file": "../Path/to/published_maya_file.mb"
                        "version_preview": "../Path/to/published_preview.jpg"
                    }
                }
        """
        maya_file_details = {}
        for version, version_details in self.asset_variations[variation][
            "published_versions"
        ].items():
            LOG.info(
                "Getting %s variation published maya file for version: %s...",
                variation,
                version,
            )
            maya_file_details[version] = {
                "maya_file": version_details["maya_file"],
                "version_preview": version_details["version_preview"],
            }

        return maya_file_details
