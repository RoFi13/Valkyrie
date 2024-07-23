"""Asset Loader GUI utility functions."""

# Can't find PySide6 modules pylint: disable=I1101

from __future__ import annotations
from functools import partial
import logging
import os
from typing import TYPE_CHECKING

from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import Qt, QSize
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QComboBox, QMainWindow

from Core import core_paths as cpath
from Core.ui.UIUtilTools.src import pyside_util_tools as put
from Core.util import file_util_tools as fut

from Asset.AssetManager.src.gui import asset_list_utils as alu
from Asset.AssetManager.src.gui import asset_widget_item as awi
from Asset.AssetManager.src.util import asset_manager_utils as amu
from Asset.AssetManager.src.util import valkyrie_asset as val

from . import asset_selection_utils

from importlib import reload

reload(awi)
reload(asset_selection_utils)

# from . import file_widget_item as fwi

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
