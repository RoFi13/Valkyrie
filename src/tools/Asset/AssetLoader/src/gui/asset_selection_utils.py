"""Asset Loader GUI element selection utility functions."""

# Can't find PySide6 modules pylint: disable=I1101

from __future__ import annotations
import logging
import os
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QComboBox, QListWidget

from Core import core_paths as cpath
from Core.ui.UIUtilTools.src import pyside_util_tools as put

from Asset.AssetManager.src.gui import asset_widget_item as awi
from Asset.AssetManager.src.util import valkyrie_asset

from . import asset_loader_utils

if TYPE_CHECKING:
    from Asset.AssetLoader.src.asset_loader import AssetLoader

# Main paths
MAIN_PATHS = cpath.core_paths()

# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 2)}"

# Full path to where resource files are stored
RSRC_PATH = f"{MODULE_PATH}/resources"
NO_PREVIEW_IMAGE_PATH = f"{RSRC_PATH}/images/No_preview.png"
ASSET_WIDGET_UI_PATH = f"{RSRC_PATH}/ui/asset_widget.ui"

LOG = logging.getLogger(os.path.basename(__file__))


def on_category_change(tool_object: AssetLoader, selected_category: str) -> None:
    LOG.debug("Selected Asset category: %s", selected_category)
    asset_loader_utils.refresh_assets_list(tool_object)


def on_asset_selection(
    tool_object: AssetLoader, selected_asset: awi.AssetWidgetItem
) -> None:
    tool_object.root.cbo_variations.blockSignals(True)
    update_asset_variants(
        tool_object.root.cbo_variations, selected_asset.get_variation_names()
    )
    tool_object.root.cbo_variations.blockSignals(False)
    update_asset_versions(
        tool_object.root.cbo_versions,
        tool_object.root.cbo_variations.currentText(),
        selected_asset,
    )


def on_variation_change(tool_object: AssetLoader, selected_variant: str) -> None:
    selected_item = tool_object.root.list_asset_previews.selectedItems()[0]
    if selected_item is None:
        return
    update_asset_versions(
        tool_object.root.cbo_versions, selected_variant, selected_item
    )


def on_version_change(tool_object: AssetLoader, selected_version: str) -> None:
    selected_item = tool_object.root.list_asset_previews.selectedItems()[0]
    if selected_item is None:
        return
    selected_variant = tool_object.root.cbo_variations.currentText()
    update_asset_preview(selected_variant, selected_version, selected_item)


def update_asset_variants(variants_combobox: QComboBox, variant_names: list) -> None:
    variants_combobox.clear()
    for variant in variant_names:
        variants_combobox.addItem(variant)

    if "Base" in variant_names:
        variants_combobox.setCurrentText("Base")


def update_asset_versions(
    versions_combobox: QComboBox,
    selected_variant: str,
    selected_asset_item: awi.AssetWidgetItem,
) -> None:
    versions_combobox.clear()
    published_versions = selected_asset_item.get_published_maya_files(selected_variant)
    reverse_sorted_versions = reversed(sorted(published_versions.keys()))
    for version in reverse_sorted_versions:
        versions_combobox.addItem(version)


def update_asset_preview(
    selected_variant: str,
    selected_version: str,
    selected_asset_item: awi.AssetWidgetItem,
) -> None:
    preview_path = NO_PREVIEW_IMAGE_PATH
    if len(selected_version) > 0:
        published_versions = selected_asset_item.get_published_maya_files(
            selected_variant
        )
        if len(published_versions) > 0:
            preview_path = published_versions[selected_version]["version_preview"]

    put.set_label_pixmap(
        selected_asset_item.root_object.lbl_variation_preview, preview_path
    )


def block_selection_signals(asset_loader: AssetLoader, block: bool = True) -> None:
    asset_loader.root.list_asset_previews.blockSignals(block)
    asset_loader.root.cbo_variations.blockSignals(block)
    asset_loader.root.cbo_versions.blockSignals(block)


def get_selected_valkyrie_item(
    list_widget: QListWidget,
) -> valkyrie_asset.ValkyrieAsset:
    selected_item = list_widget.selectedItems()[0]
    if not isinstance(selected_item, awi.AssetWidgetItem):
        return None
    return selected_item.get_valkyrie_asset()


def get_selected_asset_widget_item(list_widget: QListWidget) -> awi.AssetWidgetItem:
    selected_item = list_widget.selectedItems()[0]
    if not isinstance(selected_item, awi.AssetWidgetItem):
        return None
    return selected_item
