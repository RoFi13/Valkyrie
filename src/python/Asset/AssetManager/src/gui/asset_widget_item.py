# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""Custom Asset Widget QListWidgetItem class.

The asset_details dict often used in this file is of the following format:
{
    "asset_name": "AssetName",
    "asset_path": "../Path/to/asset/root/folder,
    "asset_preview": "../Path/to/asset/root/preview.jpg,
    "asset_metadata": "../Path/to/asset/root/AssetName_metadata.json,
    "asset_variations": {
        "<variationName>": {
            "published_versions": {
                "<version>": {
                    "maya_file": "../Path/to/published_maya_file.mb",
                    "version_preview": "../Path/to/published_preview_image.jpg"
                }
            }
            "apb_versions": [
                "../Path/to/apb_file_v001.mb",
                "../Path/to/apb_file_v002.mb"
            ]
        }
    }
}
"""
# Can't find PySide2 modules pylint: disable=I1101

import logging
import os
from importlib import reload

from PySide6 import QtWidgets
from PySide6.QtWidgets import QMainWindow

from Core import core_paths as cpath
from Core.util import file_util_tools as fut

from Asset.AssetManager.src.util import asset_manager_utils as amu

reload(fut)
reload(amu)

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
        asset_details: dict,
        tool_object: QMainWindow,
    ):
        super().__init__(parent_object)
        self.parent_object = parent_object
        self.tool_object = tool_object
        self.root_object = tool_object.root

        self.asset_details = asset_details
        self.asset_name: str
        self.asset_path: str
        self.asset_preview: str
        self.asset_metadata: str
        self.asset_variations: dict

        self.set_asset_details(self.asset_details)

    def set_asset_details(self, asset_details: dict):
        """Set list widget item's asset details.

        Args:
            asset_details (dict): Asset details which include the following:
                {
                    "asset_name": str,
                    "asset_path": str,
                    "asset_preview": str,
                    "asset_metadata": str,
                    "asset_variations" dict
                }
        """
        self.asset_name = asset_details["asset_name"]
        self.asset_path = asset_details["asset_path"]
        self.asset_preview = asset_details["asset_preview"]
        self.asset_metadata = asset_details["asset_metadata"]
        self.asset_variations = asset_details["asset_variations"]

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
        LOG.debug("Variation Dictionary: %s", self.asset_variations)
        if "published_versions" not in self.asset_variations[variation]:
            LOG.warning(
                "No published maya file versions found in: %s",
                self.asset_variations[variation],
            )
            return {}

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
