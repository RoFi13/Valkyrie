"""Asset Loader GUI utility functions."""

# Can't find PySide6 modules pylint: disable=I1101

from __future__ import annotations
import logging
import os
from typing import TYPE_CHECKING

from PySide6.QtCore import QSize

from Core import core_paths as cpath

from Asset.AssetManager.src.gui import asset_list_utils as alu

from . import asset_selection_utils

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


def refresh_assets_list(asset_loader: AssetLoader):
    asset_selection_utils.block_selection_signals(asset_loader)
    asset_loader.root.list_asset_previews.clear()
    asset_loader.root.cbo_variations.clear()
    asset_loader.root.cbo_versions.clear()
    alu.update_asset_list(asset_loader, asset_item_size=QSize(128, 80))
    asset_selection_utils.block_selection_signals(asset_loader, False)
