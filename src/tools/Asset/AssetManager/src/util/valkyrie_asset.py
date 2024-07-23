# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""Custom Maya Asset Python object commonly used in Asset Manager."""

import logging
import os
from pathlib import PurePath
import re

from Core import core_paths as cpath
from Core.util import file_util_tools as fut
from Core.util import project_util_tools as prj


LOG = logging.getLogger(os.path.basename(__file__))

# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 2)}"

# Full path to where resource files are stored
RSRC_PATH = f"{MODULE_PATH}/resources"
NO_PREVIEW_IMAGE_PATH = f"{RSRC_PATH}/images/Select_file_preview.png"

PROJECT_CONFIGS = prj.get_project_configs()


class ValkyrieAssetVariant:
    """Custom Maya Asset Variant python object for use with Asset Manager."""

    def __init__(self, variant_name: str, variant_path: str):
        """Initialize Asset Variant instance.

        Args:
            variant_name (str): New Asset Variant Name.
            variant_path (str): New Asset Variant directory path.
        """
        self._variant_name: str
        self._variant_path: str
        self._published_versions = {}
        self._apb_versions = []

        self.set_variant_name(variant_name)
        self.set_variant_path(variant_path)

        self.refresh_versions()

    def set_variant_name(self, new_name: str):
        """Set the Variant Asset's name.

        Args:
            new_name (str): New name for variant.
        """
        self._variant_name = new_name

    def get_variant_name(self):
        """Get the current Variant's asset name.

        Returns:
            str: Variant name.
        """
        return self._variant_name

    def set_variant_path(self, new_path: str):
        """Set the Variant's asset directory path.

        Args:
            new_path (str): New directory location.
        """
        self._variant_path = new_path

    def get_variant_path(self):
        """Get the Variant's asset directory path.

        Returns:
            str: Variant's asset directory path.
        """
        return self._variant_path

    def get_published_versions(self):
        """Get all published version information.

        Returns:
            dict: Published versions data including maya file and preview image paths.
        """
        return self._published_versions

    def add_published_version(
        self, version_to_add: str, maya_file_path: str, variant_preview_path: str
    ):
        """Add new Published version to variant.

        Args:
            version_to_add (str): Version of the new asset. Should follow version
                naming convention e.g. 'v###'.
            maya_file_path (str): Version's maya file path.
            variant_preview_path (str): Version's preview file path.
        """
        if version_to_add in self._published_versions:
            LOG.error("Variant Version '%s' already exists!", version_to_add)
            return

        self._published_versions[version_to_add] = {
            "maya_file": maya_file_path,
            "version_preview": variant_preview_path,
        }

    def remove_published_version(self, version_to_remove: str):
        """Remove published version from Variant.

        Args:
            version_to_remove (str): Version to remove. Should follow version naming
                convention e.g. 'v###'.
        """
        if not version_to_remove in self._published_versions:
            LOG.error("Variant Version %s doesn't exist.", version_to_remove)
            return

        del self._published_versions[version_to_remove]

    def get_apb_versions(self):
        """Get all APB/wip file paths.

        Returns:
            list(str): List of file paths to APB files.
        """
        return self._apb_versions

    def add_apb_version(self, apb_maya_file_path: str):
        """Add new APB/wip file to variant.

        Args:
            apb_maya_file_path (str): Path to new APB/wip file.
        """
        if apb_maya_file_path in self._apb_versions:
            LOG.error("APB Version '%s' already exists!", apb_maya_file_path)
            return

        self._apb_versions.append(apb_maya_file_path)

    def remove_apb_version(self, version_to_remove: str):
        """Remove APB/wip file path from variant.

        Args:
            version_to_remove (str): Version to remove. Should follow version naming
                convention e.g. 'v###'.
        """
        if not version_to_remove in self._apb_versions:
            LOG.error("APB Version %s doesn't exist.", version_to_remove)
            return

        self._apb_versions.remove(version_to_remove)

    def refresh_versions(self):
        """Refresh this variant's published and APB/wip data."""
        self._populate_published_versions()
        self._populate_apb_versions()

    def _populate_published_versions(self):
        """Get published maya file and preview paths.

        Args:
            variation_path (str): Root asset directory path.
        """
        LOG.info("Retrieving published versions...")
        self._published_versions = {}

        if not os.path.exists(f"{self._variant_path}/Publish"):
            LOG.error(
                "Invalid Asset Path! Asset Folder structure may not be "
                "compatible or built with Asset Manager. Please check path at: %s",
                f"{self._variant_path}/Publish",
            )
            return

        # Get published version folders for variation
        asset_versions = fut.get_files_or_folders(
            f"{self._variant_path}/Publish", False, True, "v[0-9]{3,4}"
        )

        if not asset_versions:
            return

        for version_path in asset_versions:
            version = version_path.split("/")[-1]
            self._published_versions[version] = {
                "maya_file": str,
                "version_preview": str,
            }
            for item in os.listdir(version_path):
                item_path = f"{version_path}/{item}"
                LOG.debug("ITEM NAME: %s", item)
                if re.match(PROJECT_CONFIGS["asset_publish_preview_regex"], item):
                    LOG.debug("FOUND VERSION PREVIEW")
                    self._published_versions[version]["version_preview"] = item_path

                if re.match(PROJECT_CONFIGS["asset_published_regex"], item):
                    self._published_versions[version]["maya_file"] = item_path

    def _populate_apb_versions(self):
        """Get APB/wip maya file paths.

        Returns:
            list(str): List of paths to apb/wip maya files for variation.
        """
        LOG.info("Retrieving apb versions...")
        if not os.path.exists(f"{self._variant_path}/APB/Maya"):
            LOG.error(
                "Invalid Asset Path! Asset Folder structure may not be "
                "compatible or built with Asset Manager. Please check path at: %s",
                f"{self._variant_path}/APB/Maya",
            )
            return

        # Get published version folders for variation
        asset_versions = fut.get_files_or_folders(
            f"{self._variant_path}/APB/Maya",
            True,
            True,
            PROJECT_CONFIGS["asset_pre_build_maya_file_regex"],
        )

        if not asset_versions:
            self._apb_versions = []

        self._apb_versions = asset_versions


class ValkyrieAsset:
    """Custom Maya Asset python object for use with Asset Manager."""

    def __init__(self, asset_name: str, asset_path: str):
        """Initialize Asset instance.

        Args:
            asset_name (str): New Asset name.
            asset_path (str): New Asset root directory path.
        """
        self._asset_category: str
        self._asset_name: str
        self._asset_path: str

        self._asset_preview_path: str
        self._asset_metadata_path: str
        self._asset_variations = {}

        self.set_asset_category(
            cpath.get_parent_directory(asset_path, return_full_path=False)
        )
        self.set_asset_name(asset_name)
        self.set_asset_path(asset_path)
        self.set_asset_metadata_path(
            PurePath(asset_path, f"{asset_name}_metadata.json")
        )
        self.set_asset_preview_path(NO_PREVIEW_IMAGE_PATH)

    def set_asset_category(self, new_category: str) -> None:
        self._asset_category = new_category

    def get_asset_category(self) -> str:
        return self._asset_category

    def set_asset_name(self, new_name: str):
        """Set Asset's name.

        Args:
            new_name (str): New Asset Name.
        """
        self._asset_name = new_name

    def get_asset_name(self):
        """Get the current Asset's name.

        Returns:
            str: Current Asset's name.
        """
        return self._asset_name

    def set_asset_path(self, new_path: str):
        """Set the Asset's root directory path.

        Args:
            new_path (str): New Asset root directory path.
        """
        self._asset_path = new_path

    def get_asset_path(self):
        """Get the Asset's current root directory path.

        Returns:
            str: Current Asset's root directory path.
        """
        return self._asset_path

    def set_asset_preview_path(self, new_preview_path: str):
        """Set the Asset's current preview image path.

        Args:
            new_preview_path (str): New preview image path.
        """
        self._asset_preview_path = new_preview_path

    def get_asset_preview_path(self):
        """Get Asset's current preview image path.

        Returns:
            str: Current preview image path.
        """
        return self._asset_preview_path

    def set_asset_metadata_path(self, new_metadata_path: str):
        """Set the Asset's current metadata JSON file path.

        Args:
            new_metadata_path (str): New metadata path.

        TODO:
            * This currently isn't implemented with the Asset Manager yet.
        """
        self._asset_metadata_path = new_metadata_path

    def get_asset_metadata_path(self):
        """Get Asset's current metadata path.

        Returns:
            str: Path to Asset's metadata JSON file.

        TODO:
            * This currently isn't implemented with the Asset Manager yet.
        """
        return self._asset_metadata_path

    def add_asset_variant(self, variant_name: str, variant_path: str):
        """Add new Asset Variant object to this Asset.

        Args:
            variant_name (str): New Variant name.
            variant_path (str): New Variant root directory path.

        Returns:
            ValkyrieAssetVariant: Returns newly created Asset Variant object if
                successfully created. Otherwise, returns None.
        """
        if variant_name in self._asset_variations:
            LOG.error("Asset Variant %s already exists!", variant_name)
            return None

        new_variant = ValkyrieAssetVariant(variant_name, variant_path)

        self._asset_variations[variant_name] = new_variant

        return new_variant

    def remove_asset_variant(self, variant_to_remove: str):
        """Remove Asset Variant from this Asset.

        Args:
            variant_to_remove (str): Name of Variant to remove.
        """
        if not variant_to_remove in self._asset_variations:
            LOG.error("Asset Variant %s doesn't exist!", variant_to_remove)
            return

        del self._asset_variations[variant_to_remove]

    def get_all_asset_variants(self):
        """Get all Asset Variant python objects.

        Returns:
            list(ValkyrieAssetVariant): List of all Variant objects.
        """
        if len(self._asset_variations) == 0:
            LOG.error("No Asset Variants found.")
            return None

        return self._asset_variations

    def get_asset_variant(self, variant_name: str):
        """Get specific Asset Variant object.

        Args:
            variant_name (str): Variant object to get.

        Returns:
            ValkyrieAssetVariant: Returns Variant object if found. Otherwise, returns
                None
        """
        if not variant_name in self._asset_variations:
            LOG.error("Asset Variant %s doesn't exist!", variant_name)
            return None

        return self._asset_variations[variant_name]
