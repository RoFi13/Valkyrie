# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""
This module is to create both a APB/wip (asset pre-build) or a Published Maya
file.
"""
# Can't find PySide6 modules pylint: disable=I1101

__version__ = "1.0.1"

from functools import partial
import logging
import os
import re

from PySide6 import QtCore, QtWidgets
from PySide6.QtUiTools import QUiLoader

from Core import core_paths as cpath
from Core import maya_start as ms
from Core.ui.UIUtilTools.src import maya_ui_util_tools as mui
from Core.ui.UIUtilTools.src import pyside_util_tools as put
from Core.ui.UIUtilTools.src import snipping_widget as snip
from Core.util import file_util_tools as fut
from Core.util import maya_file_util_tools as mfut
from Core.util import project_util_tools as prj
from Core.util import string_util_tools as sut

from Util.UtilTools.src import util_tools as utt

from .gui import asset_gui_utils as agu
from .gui import asset_list_utils as alu
from .util import asset_manager_utils as amu
from .util import validation_utils as vu

# Import maya modules
from maya import cmds

LOADER = QUiLoader()

# Window title and object names
WINDOW_TITLE = "Asset Manager"
WINDOW_OBJECT = "assetManagerObject"

# Maya-specific
DOCK_WITH_MAYA_UI = False

# Main paths
MAIN_PATHS = cpath.core_paths()

# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 1)}"

# Full path to where .ui files are stored
RSRC_PATH = f"{MODULE_PATH}/resources"

LOG = logging.getLogger(os.path.basename(__file__))


class AssetManager(QtWidgets.QMainWindow):
    """Asset Manager tool for navigating to asset files and creating new files."""

    def __init__(self, parent=None):
        """Initialize instance of tool.

        Set up the default UI state.

        Args:
            parent (None, optional): Optional parent object to init from.
        """
        super().__init__(parent)

        # Instance variables
        self.asset_root_directory: str = ""
        self.publish_type: str = "model"
        self.asset_folder_tree = {
            "Design": ["Sketch", "Concepts", "Bibles", "Ref"],
            "Publish": [],
            "APB": ["Blend", "AE", "Zbrush", "SPaint", "SDesign", "PS", "Maya"],
            "VFX": [],
            "Anim": [],
            "Shared": ["VFX", "Sound", "Anim"],
        }
        self.publish_preview_widget = None
        self.current_variation_preview: str = ""

        # Set up default UI settings
        self.ui_settings = {
            "main_ui_file": f"{RSRC_PATH}/ui/asset_manager.ui",
            "asset_widget": f"{RSRC_PATH}/ui/asset_widget.ui",
            "file_widget": f"{RSRC_PATH}/ui/file_widget.ui",
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

        # Final Setup for UI
        self.setup_ui()
        self.setup_signals()

        # Change asset type selection
        # self.combo_asset_type.setCurrentIndex(1)

    # Title string in Editor pylint: disable=pointless-string-statement
    """
    888b     d888        d8888 8888888 888b    888      8888888888 888     888 888b    888  .d8888b.   .d8888b.
    8888b   d8888       d88888   888   8888b   888      888        888     888 8888b   888 d88P  Y88b d88P  Y88b
    88888b.d88888      d88P888   888   88888b  888      888        888     888 88888b  888 888    888 Y88b.
    888Y88888P888     d88P 888   888   888Y88b 888      8888888    888     888 888Y88b 888 888         "Y888b.
    888 Y888P 888    d88P  888   888   888 Y88b888      888        888     888 888 Y88b888 888            "Y88b.
    888  Y8P  888   d88P   888   888   888  Y88888      888        888     888 888  Y88888 888    888       "888
    888   "   888  d8888888888   888   888   Y8888      888        Y88b. .d88P 888   Y8888 Y88b  d88P Y88b  d88P
    888       888 d88P     888 8888888 888    Y888      888         "Y88888P"  888    Y888  "Y8888P"   "Y8888P"
    """

    # pylint: enable=pointless-string-statement

    def get_asset_configs(self):
        """Load JSON data from Project Config file.

        Grabs asset data from ProjectConfig.json file.

        Returns:
            bool: True if valid project config data was gathered. Otherwise, False.
        """
        self.project_configs = prj.get_project_configs()
        self.current_project = self.project_configs["project_name"]

        if len(self.project_configs) == 0:
            return False

        # Asset regex's
        self.asset_wip_maya_regex = re.compile(
            self.project_configs["asset_pre_build_maya_file_regex"]
        )

        # Other important information
        self.current_project = self.project_configs["project_name"]
        self.current_cg_project_path = MAIN_PATHS["cg_path"]

        return True

    def setup_ui(self):
        """Set up UI elements.

        Store widgets as simplifed name and sets up starting state of UI
        """
        # Update current show qLabel text and tool version
        self.root.lbl_current_project.setText((self.current_project).upper())
        self.root.lbl_tool_version.setText(__version__)

        # Update default variation preview image
        put.set_label_pixmap(
            self.root.lbl_variation_preview,
            f"{RSRC_PATH}/images/Select_file_preview.png",
        )
        self.current_variation_preview = f"{RSRC_PATH}/images/Select_file_preview.png"

        self.refresh_ui()

        # Regular expression, all alphanumeric characters
        agu.set_asset_naming_validators(self.root)

        # Set placeholder text
        agu.set_asset_naming_tooltips(self.root)

        # Create custom preview button in publish section
        self.root.publish_section_HL.insertWidget(0, snip.CustomPreviewButton(self))
        self.publish_preview_widget = self.root.publish_section_HL.itemAt(0).widget()

    # pylint: disable=pointless-string-statement
    """TODO: When publishing asset, try to auto fill for artist the used
    zbrush and substance files associated with the publish. Save these paths with
    the published metadata. This way we can look at which substance and zbrush files
    were used with that published version more easily."""
    # pylint: enable=pointless-string-statement

    def setup_signals(self):
        """Connect signals to methods."""
        self.root.cbo_categories.currentTextChanged.connect(self.refresh_ui)

        self.root.list_asset_previews.itemClicked.connect(alu.asset_selection_changed)

        self.root.btn_make_main_preview.clicked.connect(
            partial(agu.set_asset_main_preview, self)
        )

        self.root.cbo_variations.currentTextChanged.connect(
            partial(alu.asset_variation_changed, self)
        )

        self.root.list_published_files.itemClicked.connect(
            alu.publish_selection_changed
        )

        # APB Pre-build section
        self.root.cbo_apb_create_from.currentTextChanged.connect(
            partial(amu.update_create_from_type, self)
        )

        self.root.btn_build.clicked.connect(self.build_apb_asset)

        # Publish section
        self.root.btn_publish.clicked.connect(self.publish_asset)

    def refresh_ui(self):
        self.root.list_asset_previews.clear()
        self.root.list_published_files.clear()
        self.root.list_apb_files.clear()
        self.root.cbo_variations.clear()

        alu.update_asset_list(self)

    def build_apb_asset(self):
        """Build APB (wip) asset from user choices."""
        LOG.info("Build APB Asset...")
        asset_details = amu.get_asset_creation_details(self)

        if vu.validate_asset_details(asset_details) is False:
            LOG.error("Asset details are invalid. See log above for more details.")
            return

        # Build asset folders if they don't already exist
        asset_variant_path = self.build_asset_folders(asset_details)

        # Save scene into new location with new name
        apb_file_details = self.build_apb_file_details(
            asset_variant_path, asset_details
        )

        if self.root.cbo_apb_create_from.currentText() == "Current Scene":
            if os.access(cmds.file(query=True, sceneName=True), os.W_OK) is False:
                mui.display_confirm_dialog(
                    "Access Denied",
                    (
                        "Current open file is read only. Please unlock file via "
                        "version control system or in file properties."
                    ),
                )
                return

            mfut.create_from_current_scene(apb_file_details["file_path"])

        if self.root.cbo_apb_create_from.currentText() == "New Scene":
            mfut.create_from_new_scene(apb_file_details["file_path"])

        if self.root.cbo_apb_create_from.currentText() == "File":
            mfut.create_from_file(
                asset_details["file_path"], apb_file_details["file_path"]
            )

        # Copy and repath textures to new APB location
        mfut.repath_textures(apb_file_details["textures_directory"], self)

        # Refresh UI
        self.refresh_ui()

        # Select new/existing asset again to refresh other parts of the UI
        for asset in self.root.list_asset_previews.findItems("", QtCore.Qt.MatchRegExp):
            if asset.asset_name != asset_details["asset_name"]:
                continue
            self.root.list_asset_previews.setCurrentItem(asset)
            self.root.list_asset_previews.itemClicked.emit(asset)
            self.root.cbo_variations.setCurrentText(asset_details["asset_variant"])

        # Final save of file to save texture repathing changes
        cmds.file(force=True, save=True, options="v=0;", type="mayaBinary")

        LOG.info("APB Asset built!")

    def publish_asset(self):
        """Publish the current maya scene."""
        LOG.info("Publishing scene...")
        asset_details = amu.get_asset_creation_details(self, True)

        if vu.validate_asset_details(asset_details, self) is False:
            LOG.error("Asset details are invalid. See log above for more details.")
            return

        # Build asset folders if they don't already exist
        asset_variant_path = self.build_asset_folders(asset_details)

        publish_file_details = self.build_publish_file_details(
            asset_variant_path, asset_details
        )
        LOG.debug("PUBLISH FILE DETAILS: %s", publish_file_details)

        if vu.confirm_publish_details(asset_details, publish_file_details) is False:
            LOG.warning("User cancelled operation.")
            return

        # Checking if current scene is locked
        has_write_access = True
        if os.access(cmds.file(query=True, sceneName=True), os.W_OK) is False:
            mui.display_confirm_dialog(
                "Access Denied",
                (
                    "Current open file is read only. Please unlock file via "
                    "version control system or in file properties. File path:\n\n"
                    f"{cmds.file(query=True, sceneName=True)}"
                ),
            )
            has_write_access = False

        if (
            os.path.exists(publish_file_details["main_asset_preview_path"]) is True
            and os.access(publish_file_details["main_asset_preview_path"], os.W_OK)
            is False
        ):
            mui.display_confirm_dialog(
                "Access Denied",
                (
                    "Main Asset Preview image is read-only. Please unlock file via "
                    "version control system or in file properties. File path:\n\n"
                    f"{publish_file_details['main_asset_preview_path']}"
                ),
            )
            has_write_access = False

        if has_write_access is False:
            return

        LOG.info("Passed validations. Creating publish...")
        # Save scene into new location with new name
        mfut.create_from_current_scene(publish_file_details["file_path"])

        # Copy and repath textures to new APB location
        mfut.repath_textures(publish_file_details["textures_directory"], self)

        # Save preview image to publish directory
        agu.save_qlabel_pixmap_to_disk(
            self.publish_preview_widget, publish_file_details["variant_preview_path"]
        )
        # If main asset preview doesn't exist, make one
        if os.path.exists(publish_file_details["main_asset_preview_path"]) is False:
            agu.save_qlabel_pixmap_to_disk(
                self.publish_preview_widget,
                publish_file_details["main_asset_preview_path"],
            )
        # If user wishes to overwrite the main asset preview...
        if self.root.chk_make_main_preview.isChecked() is True:
            agu.save_qlabel_pixmap_to_disk(
                self.publish_preview_widget,
                publish_file_details["main_asset_preview_path"],
            )

        # Final save of file to save texture repathing changes
        cmds.file(force=True, save=True, options="v=0;", type="mayaBinary")

        # Refresh UI
        self.refresh_ui()

        # Select new/existing asset again to refresh other parts of the UI
        for asset in self.root.list_asset_previews.findItems("", QtCore.Qt.MatchRegExp):
            if asset.asset_name != asset_details["asset_name"]:
                continue
            self.root.list_asset_previews.setCurrentItem(asset)
            self.root.list_asset_previews.itemClicked.emit(asset)
            self.root.cbo_variations.setCurrentText(asset_details["asset_variant"])

        agu.publish_ui_reset(self)

        LOG.info("Asset Successfully Published!")

    def build_asset_folders(self, asset_details: dict):
        """Create all asset folders if they don't exist.

        Args:
            asset_details (dict): Asset details data as follows:
                "asset_category" (str): "Name of Asset Category,
                "asset_name" (str): Name of Asset,
                "asset_variant" (str): Name of Asset Variant,
                "file_path" (str): File path if chosen. Otherwise is None

        Returns:
            str: Path to newly created asset's variant root folder.
        """
        root_asset_path = (
            f"{MAIN_PATHS['cg_path']}/assets/"
            f"{asset_details['asset_category']}/{asset_details['asset_name']}"
        )
        asset_variant_directory = f"{root_asset_path}/{asset_details['asset_variant']}"

        # Create variant
        fut.create_directory(asset_variant_directory)

        LOG.debug("Creating directories: %s", self.asset_folder_tree)
        for directory, sub_directories in self.asset_folder_tree.items():
            if len(sub_directories) == 0:
                fut.create_directory(f"{asset_variant_directory}/{directory}")
                continue

            for sub_dir in sub_directories:
                fut.create_directory(f"{asset_variant_directory}/{directory}/{sub_dir}")

        LOG.info("Created Asset sub-directories!")

        return asset_variant_directory

    def build_apb_file_details(self, asset_variant_path: str, asset_details: dict):
        """Build the new maya APB filename that is +1 from latest version found.

        Args:
            asset_variant_path (str): Asset variant path.
            asset_details (dict): Asset variant details.

        Returns:
            dict: Return the final maya file details in the following format:
                "version": Version string i.e. "v001",
                "file_path": Final maya file path name,
                "textures_directory": APB textures version directory
                i.e. Maya/Textures/v001
        """
        apb_maya_directory = f"{asset_variant_path}/APB/Maya"
        apb_files = fut.get_files_or_folders(
            apb_maya_directory,
            True,
            True,
            self.project_configs["asset_pre_build_maya_file_regex"],
        )

        shortened_asset_type = amu.shorten_category_name(
            asset_details["asset_category"]
        )

        if not apb_files:
            final_file_details = {
                "version": "v001",
                "file_path": (
                    f"{apb_maya_directory}/APB_{shortened_asset_type}_"
                    f"{asset_details['asset_name']}_"
                    f"{asset_details['asset_variant']}_v001.mb"
                ),
                "textures_directory": f"{apb_maya_directory}/Textures/v001",
            }
            LOG.debug("APB FILE DETAILS: %s", final_file_details)
            return final_file_details

        apb_files.sort()
        LOG.debug("LATEST VERSION: %s", apb_files[-1])
        version_search_string = sut.find_version_string(apb_files[-1])
        version_number = int(
            apb_files[-1][
                version_search_string.start() : version_search_string.end()
            ].split("v")[-1]
        )

        versioned_up_file_path = sut.replace_version_string(
            apb_files[-1], version_number + 1
        )

        new_version_string = f"v{str(version_number + 1).rjust(3, '0')}"
        versioned_up_file_details = {
            "version": new_version_string,
            "file_path": versioned_up_file_path,
            "textures_directory": f"{apb_maya_directory}/Textures/{new_version_string}",
        }

        LOG.debug("APB FILE DETAILS: %s", versioned_up_file_details)

        return versioned_up_file_details

    def build_publish_file_details(self, asset_variant_path: str, asset_details: dict):
        """Build the new maya Publish filename that is +1 from latest version found.

        Args:
            asset_variant_path (str): Asset variant path.
            asset_details (dict): Asset variant details.

        Returns:
            dict: Return the final maya file details in the following format:
                "version": Version string i.e. "v001",
                "file_path": Final maya file path name,
                "textures_directory": Publish textures version directory
                i.e. Publish/v001/Textures
        """
        asset_structure = "MDL"
        if utt.check_scene_for_joints() is True:
            asset_structure = "RIG"

        publish_root_directory = f"{asset_variant_path}/Publish"

        published_directories = fut.get_files_or_folders(
            publish_root_directory, False, False, "v[0-9]{3,3}"
        )

        shortened_asset_type = amu.shorten_category_name(
            asset_details["asset_category"]
        )

        if not published_directories:
            final_file_details = {
                "version": "v001",
                "file_path": (
                    f"{publish_root_directory}/v001/{asset_structure}_"
                    f"{shortened_asset_type}_"
                    f"{asset_details['asset_name']}_"
                    f"{asset_details['asset_variant']}_v001.mb"
                ),
                "textures_directory": f"{publish_root_directory}/v001/Textures",
                "variant_preview_path": (
                    f"{publish_root_directory}/v001/"
                    f"{asset_structure}_"
                    f"{shortened_asset_type}_"
                    f"{asset_details['asset_name']}_"
                    f"{asset_details['asset_variant']}_v001.jpg"
                ),
                "main_asset_preview_path": (
                    f"{cpath.get_parent_directory(asset_variant_path, 0)}/"
                    f"{asset_details['asset_name']}_preview.jpg"
                ),
            }
            LOG.debug("PUBLISH FILE DETAILS: %s", final_file_details)
            return final_file_details

        # If publish version directories already exist...
        published_directories.sort()
        LOG.debug("LATEST VERSION: %s", published_directories[-1])

        version_search_string = sut.find_version_string(published_directories[-1])
        version_number = int(
            published_directories[-1][
                version_search_string.start() : version_search_string.end()
            ].split("v")[-1]
        )

        new_version_string = sut.replace_version_string(
            published_directories[-1], version_number + 1
        )

        versioned_up_file_path = (
            f"{publish_root_directory}/{new_version_string}/{asset_structure}_"
            f"{shortened_asset_type}_"
            f"{asset_details['asset_name']}_"
            f"{asset_details['asset_variant']}_{new_version_string}.mb"
        )
        versioned_up_file_details = {
            "version": new_version_string,
            "file_path": versioned_up_file_path,
            "textures_directory": (
                f"{publish_root_directory}/{new_version_string}/" "Textures"
            ),
            "variant_preview_path": (
                f"{publish_root_directory}/{new_version_string}/"
                f"{asset_structure}_"
                f"{shortened_asset_type}_"
                f"{asset_details['asset_name']}_"
                f"{asset_details['asset_variant']}_{new_version_string}.jpg"
            ),
            "main_asset_preview_path": (
                f"{cpath.get_parent_directory(asset_variant_path, 0)}/"
                f"{asset_details['asset_name']}_preview.jpg"
            ),
        }

        LOG.debug("PUBLISH FILE DETAILS: %s", versioned_up_file_details)

        return versioned_up_file_details

    def closeEvent(self):  # Qt Override pylint:disable=C0103
        """Delete UI widget."""
        # Get grab preview qlabel widget
        grab_preview_widg = self.root.center_content_HL.itemAt(0).widget()
        grab_preview_widg.deleteLater()
        self.deleteLater()


def run_maya():
    """Run tool in maya."""
    result = ms.run_maya(AssetManager, WINDOW_OBJECT, WINDOW_TITLE, DOCK_WITH_MAYA_UI)
    return result
