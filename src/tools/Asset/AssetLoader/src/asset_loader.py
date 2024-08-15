"""Tool for importing/referencing published project assets into Maya scenes."""

# Can't find PySide6 modules pylint: disable=I1101

__version__ = "1.0.0"

from functools import partial
import logging
import os
import re

from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader

from Core import core_paths as cpath
from Core import maya_start as ms
from Core.ui.UIUtilTools.src import pyside_util_tools as put
from Core.util import project_util_tools as prj

from .gui import asset_loader_utils
from .gui import asset_selection_utils as asu

from .handlers import asset_loading_handler

LOADER = QUiLoader()

# Window title and object names
WINDOW_TITLE = "Asset Loader"
WINDOW_OBJECT = "asset_loader_window"

# Maya-specific
DOCK_WITH_MAYA_UI = False

# Main paths
MAIN_PATHS = cpath.core_paths()

# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 1)}"

# Full path to where .ui files are stored
RSRC_PATH = f"{MODULE_PATH}/resources"

LOG = logging.getLogger(os.path.basename(__file__))


class AssetLoader(QtWidgets.QMainWindow):
    """Asset Manager tool for navigating to asset files and creating new files."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        # Set up default UI settings
        self.ui_settings = {
            "main_ui_file": f"{RSRC_PATH}/ui/asset_loader.ui",
            "asset_widget": f"{RSRC_PATH}/ui/asset_widget.ui",
            "min_size": [],
            "max_size": [],
        }

        self.root = put.setup_class_ui(
            self, WINDOW_OBJECT, WINDOW_TITLE, self.ui_settings
        )

        if self.get_asset_configs() is False:
            self.close()
            return

        self.asset_root_directory = f"{self.current_cg_project_path}/assets"

        self.setup_ui()
        self.setup_signals()

    def get_asset_configs(self) -> bool:
        self.project_configs = prj.get_project_configs()
        self.current_project = self.project_configs["project_name"]

        if len(self.project_configs) == 0:
            return False

        # Asset regex's
        self.asset_name_regex = re.compile(self.project_configs["asset_name_regex"])
        self.asset_variant_regex = re.compile(
            self.project_configs["asset_variant_regex"]
        )
        self.version_regex = re.compile(self.project_configs["default_version_regex"])
        self.publish_preview_regex = re.compile(
            self.project_configs["asset_publish_preview_regex"]
        )

        # Other important information
        self.current_cg_project_path = MAIN_PATHS["cg_path"]

        return True

    def setup_ui(self) -> None:
        # Update version and current project
        self.root.lbl_current_project.setText((self.current_project).upper())
        self.root.lbl_tool_version.setText(__version__)
        # Load asset previews into list
        asset_loader_utils.refresh_assets_list(self)

    def setup_signals(self) -> None:
        self.root.cbo_categories.currentTextChanged.connect(
            partial(asu.on_category_change, self)
        )
        self.root.list_asset_previews.itemClicked.connect(
            partial(asu.on_asset_selection, self)
        )
        self.root.cbo_variations.currentTextChanged.connect(
            partial(asu.on_variation_change, self)
        )
        self.root.cbo_versions.currentTextChanged.connect(
            partial(asu.on_version_change, self)
        )
        self.root.btn_load_asset.clicked.connect(self.load_asset)

    def closeEvent(self) -> None:  # Qt Override pylint:disable=C0103
        self.deleteLater()

    def load_asset(self) -> bool:
        selected_item = asu.get_selected_asset_widget_item(
            self.root.list_asset_previews
        )
        selected_variant = self.root.cbo_variations.currentText()
        selected_version = self.root.cbo_versions.currentText()
        asset_namespace = selected_item.get_valkyrie_asset().get_asset_name().upper()

        published_file_path = selected_item.get_published_maya_files(selected_variant)[
            selected_version
        ]["maya_file"]

        if not os.path.exists(published_file_path):
            LOG.error("No valid published file found at path: %s", published_file_path)
            return False

        load_success = False
        if self.root.radio_reference.isChecked():
            load_success = asset_loading_handler.reference_asset(
                selected_item.get_valkyrie_asset().get_asset_category(),
                published_file_path,
                asset_namespace,
                self.root.spin_load_count.value(),
                True,
            )
        else:
            load_success = asset_loading_handler.import_asset(
                selected_item.get_valkyrie_asset().get_asset_category(),
                published_file_path,
                asset_namespace,
                self.root.spin_load_count.value(),
                True,
            )

        if not load_success:
            LOG.error("Failed to load assets. See log for details.")
            return False

        return True


def run_maya() -> AssetLoader:
    """Run tool in maya."""
    result = ms.run_maya(AssetLoader, WINDOW_OBJECT, WINDOW_TITLE, DOCK_WITH_MAYA_UI)
    return result
