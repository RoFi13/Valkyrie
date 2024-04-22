# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""Custom Maya Asset object commonly used in Asset Manager."""

import logging
import os

LOG = logging.getLogger(os.path.basename(__file__))


class ValkyrieAssetVariant:
    def __init__(self, variant_name: str):
        self._variant_name: str
        self._published_versions = {}
        self._apb_versions = []

        self.set_variant_name(variant_name)

    def set_variant_name(self, new_name: str):
        self._variant_name = new_name

    def get_variant_name(self):
        return self._variant_name

    def add_published_version(
        self, version_to_add: str, maya_file_path: str, variant_preview_path: str
    ):
        if version_to_add in self._published_versions:
            LOG.error("Variant Version '%s' already exists!", version_to_add)
            return

        self._published_versions[version_to_add] = {
            "maya_file": maya_file_path,
            "version_preview": variant_preview_path,
        }

    def remove_published_version(self, version_to_remove: str):
        if not version_to_remove in self._published_versions:
            LOG.error("Variant Version %s doesn't exist.", version_to_remove)
            return

        del self._published_versions[version_to_remove]

    def add_apb_version(self, apb_maya_file_path: str):
        if apb_maya_file_path in self._apb_versions:
            LOG.error("APB Version '%s' already exists!", apb_maya_file_path)
            return

        self._apb_versions.append(apb_maya_file_path)

    def remove_apb_version(self, version_to_remove: str):
        if not version_to_remove in self._apb_versions:
            LOG.error("APB Version %s doesn't exist.", version_to_remove)
            return

        self._apb_versions.remove(version_to_remove)


class ValkyrieAsset:
    def __init__(self, asset_name: str, asset_path: str):
        self._asset_name = asset_name
        self._asset_path = asset_path

        self._asset_preview_path: str
        self._asset_metadata_path: str
        self._asset_variations = {}

    def set_asset_name(self, new_name: str):
        self._asset_name = new_name

    def get_asset_name(self):
        return self._asset_name

    def set_asset_path(self, new_path: str):
        self._asset_path = new_path

    def get_asset_path(self):
        return self._asset_path

    def set_asset_preview_path(self, preview_path: str):
        self._asset_preview_path = preview_path

    def get_asset_preview_path(self):
        return self._asset_preview_path

    def add_asset_variant(self, variant_name: str):
        if variant_name in self._asset_variations:
            LOG.error("Asset Variant %s already exists!", variant_name)
            return

        self._asset_variations[variant_name] = ValkyrieAssetVariant(variant_name)

    def remove_asset_variant(self, variant_name: str):
        if not variant_name in self._asset_variations:
            LOG.error("Asset Variant %s doesn't exist!", variant_name)
            return

        del self._asset_variations[variant_name]

    def get_asset_variant(self, variant_name: str):
        if not variant_name in self._asset_variations:
            LOG.error("Asset Variant %s doesn't exist!", variant_name)
            return

        return self._asset_variations[variant_name]

        # {
        #     "asset_name": "AssetName",
        #     "asset_path": "../Path/to/asset/root/folder,
        #     "asset_preview": "../Path/to/asset/root/preview.jpg,
        #     "asset_metadata": "../Path/to/asset/root/AssetName_metadata.json,
        #     "asset_variations": {
        #         "<variationName>": {
        #             "published_versions": {
        #                 "<version>": {
        #                     "maya_file": "../Path/to/published_maya_file.mb",
        #                     "version_preview": "../Path/to/published_preview_image.jpg"
        #                 }
        #             }
        #             "apb_versions": [
        #                 "../Path/to/apb_file_v001.mb",
        #                 "../Path/to/apb_file_v002.mb"
        #             ]
        #         }
        #     }
        # }
