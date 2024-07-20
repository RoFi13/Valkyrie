"""Put tool description and usage in here."""

import json
import logging
import os
import re
import shutil

# Import maya modules
from maya import cmds
from maya import mel
from maya import utils as util

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QPoint, Qt
from PySide6.QtUiTools import QUiLoader

from Core import core_paths as cpath
from Core import maya_start as ms

# These can be utilized if you wish
from Core.ui.UIUtilTools.src import maya_ui_util_tools as mui
from Core.ui.UIUtilTools.src import pyside_util_tools as put
from Core.util import maya_file_util_tools as mfut
from Core.util import project_util_tools as prj
from Core.util import file_util_tools as fut

from .gui import shot_gui_utils

from importlib import reload

reload(shot_gui_utils)

# Window title and object names
WINDOW_TITLE = "Shot Builder"
WINDOW_OBJECT = "shot_builder_window"

# Maya-specific
DOCK_WITH_MAYA_UI = False

# Main paths
MAIN_PATHS = cpath.core_paths()

# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 1)}"

# Full path to where .ui files are stored
RSRC_PATH = f"{MODULE_PATH}/resources"


LOG = logging.getLogger(os.path.basename(__file__))


class ShotBuilder(QtWidgets.QMainWindow):
    """Tool description/docstring here."""

    def __init__(self, parent=None):
        """Initialize instance of tool.

        Set up the default UI state.

        Args:
            parent (None, optional): Optional parent object to init from.
        """
        super().__init__(parent)

        # Instance Variables Examples
        self.project_configs = ""
        self.current_project = ""
        self.asset_wip_maya_regex = ""
        self.current_project = ""
        self.current_cg_project_path = ""

        # Set up default UI settings
        self.ui_settings = {
            "main_ui_file": f"{RSRC_PATH}/ui/shot_builder.ui",
            "min_size": [],
            "max_size": [],
        }

        self.root = put.setup_class_ui(
            self, WINDOW_OBJECT, WINDOW_TITLE, self.ui_settings
        )

        if self.get_configs() is False:
            self.close()
            return

        # Final Setup for UI
        self.setup_ui()
        self.setup_signals()

    def get_configs(self):
        """Load JSON data from Project Config file.

        Grabs asset data from ProjectConfig.json file.

        Returns:
            bool: True if valid project config data was gathered. Otherwise, False.
        """
        self.project_configs = prj.get_project_configs()
        self.current_project = self.project_configs["project_name"]

        if len(self.project_configs) == 0:
            return False

        # Example getting the Asset regex's
        self.asset_wip_maya_regex = re.compile(
            self.project_configs["asset_pre_build_maya_file_regex"]
        )

        # Other important information
        self.current_project = self.project_configs["project_name"]
        self.current_cg_project_path = MAIN_PATHS["cg_path"]

        # PETAR CHANGES
        self.current_cinematics_path = (
            f"{self.current_cg_project_path}/animation/cinematics"
        )
        self.sequence_name_regex = self.project_configs["final_anim_sequence_regex"]
        self.shot_name_regex = self.project_configs["final_anim_shot_name_regex"]
        # PETAR CHANGES

        return True

    def setup_ui(self):
        """Set up UI elements.

        Store widgets as simplifed name and sets up starting state of UI
        """

        # PETAR CHANGES

        # self.set_cbox_validator(
        #     self.root.cbox_choose_sequence, self.sequence_name_regex
        # )
        # self.set_cbox_validator(self.root.cbox_choose_shot, self.shot_name_regex)

        sequence_folders = fut.get_files_or_folders(self.current_cinematics_path)
        self.add_cbox_items(self.root.cbox_choose_sequence, sequence_folders)

        self.add_shot_cbox_items()  # NW

        # PETAR CHANGES

        # LOG.info

        # # Update current show qLabel text
        # self.root.lbl_current_project.setText((self.current_project).upper())
        # # Update default variation preview image
        # put.set_label_pixmap(
        #     self.root.lbl_variation_preview,
        #     f"{RSRC_PATH}/images/Select_file_preview.png",
        # )

        # TODO: Petar, check out this file I created and function as an example of
        # how to validate and prevent user from typing special characters and conform
        # what they type to the project naming conventions for sequences and shots
        # shot_gui_utils.set_asset_naming_validators()

    def setup_signals(self):
        """Connect signals to methods."""
        # self.root.list_asset_previews.itemClicked.connect(alu.asset_selection_changed)

        # self.root.list_published_files.itemClicked.connect(
        #     alu.publish_selection_changed
        # )

        # PETAR CHANGES
        # if the sequence item gets changed, it updates the shot folders that belong to that sequence
        self.root.cbox_choose_sequence.currentIndexChanged.connect(
            self.add_shot_cbox_items
        )
        self.root.btn_build_shot.clicked.connect(self.build_shot)

        # PETAR CHANGES

        # self.root.btn_build.clicked.connect(db.create_db_task)

    # PETAR CHANGES
    def set_cbox_validator(self, textfield, regex):
        validator = QtGui.QRegExpValidator(regex)
        textfield.lineEdit().setValidator(validator)

    def get_folders_in_directory(self, directory):
        return os.listdir(directory)

    def check_if_path_exists(self, directory):
        return os.path.exists(directory)

    def add_cbox_items(self, cbox, folders):
        if folders is None:
            return
        cbox.addItems(folders)

    def get_current_cbox_item(self, cbox):
        return cbox.currentText()

    def add_shot_cbox_items(self):  # NW
        self.root.cbox_choose_shot.clear()
        current_sequence_item = self.get_current_cbox_item(
            self.root.cbox_choose_sequence
        )
        current_sequence_path = (
            f"{self.current_cinematics_path}/{current_sequence_item}"
        )
        LOG.warning("item: %s", current_sequence_item)
        does_path_exist = self.check_if_path_exists(current_sequence_path)
        if does_path_exist:
            # shot_folders = self.get_folders_in_directory(current_sequence_path)
            shot_folders = fut.get_files_or_folders(current_sequence_path)

            if shot_folders is None:
                return
            self.root.cbox_choose_shot.addItems(shot_folders)

    def create_folder_structure(self, directory):  # NW
        for state in ["storyboard", "previs", "final"]:
            os.makedirs(f"{directory}/{state}")

    def create_file(self, directory, file_name):
        open(f"{directory}/{file_name}", "w")

    def check_if_string_matches_regex(self, pattern, string):
        return True if re.match(pattern, string) else False

    def get_state_short_name(self, string):
        return "fa" if string == "final" else "pvs"

    def form_file_path(self, *components):
        print(*components)
        return os.path.join(self.current_cinematics_path, *components)

    def get_scene_name(self, directory, sequence_name, shot_name, state_sn):  # NW
        scene_name = f"{sequence_name}_{shot_name}_{state_sn}_v001.mb"
        diretory_folders = os.listdir(directory)
        if len(diretory_folders) == 0:
            return scene_name
        else:
            latest_scene = max(os.listdir(directory))
            new_version_number = int(latest_scene[-1 - 5 :][:-3]) + 1
            latest_version = str(new_version_number).zfill(3)

            scene_name = f"{sequence_name}_{shot_name}_{state_sn}_v{latest_version}.mb"
            return scene_name

    def check_if_cbox_item_exists(self, cbox, item):
        if cbox.findText(item) == -1:
            self.add_cbox_items(cbox, item)

    def build_shot(self):  # NW
        sequence_name = self.get_current_cbox_item(self.root.cbox_choose_sequence)
        shot_name = self.get_current_cbox_item(self.root.cbox_choose_shot)
        state = self.get_current_cbox_item(self.root.cbox_choose_state)
        state_sn = self.get_state_short_name(state)

        final_directory = self.form_file_path(sequence_name, shot_name, state)
        shot_directory = self.form_file_path(sequence_name, shot_name)

        # WE'RE DOING THIS EXTRA CHECK INCASE THE PERSON DIDN'T HIT ENTER TO VALIDATE HIS INPUT, SO THE SCRIPT WOULD OTHERWISE TAKE IN WRONG INPUTS, DESPITE THE VALIDATOR
        # EXAMPLE. THEY CAN TYPE "TE" FOR THE SEQUENCE, SO WE'RE DOING AN EXTRA CHECK AFTER THE VALIDATOR
        is_sequence_accurate = self.check_if_string_matches_regex(
            self.sequence_name_regex, sequence_name
        )
        is_shot_accurate = self.check_if_string_matches_regex(
            self.shot_name_regex, shot_name
        )
        if is_sequence_accurate and is_shot_accurate:
            print(final_directory)
            print(shot_directory)
            if self.check_if_path_exists(final_directory) == False:
                self.create_folder_structure(shot_directory)

            scene_name = self.get_scene_name(
                final_directory, sequence_name, shot_name, state_sn
            )
            print(scene_name)
            self.create_file(final_directory, scene_name)

            # IF THE PERSON DIDN'T HIT ENTER TO COMMIT THEIR INPUT, THIS STEP MAKES SURE THE INPUT GETS ADDED TO THE LSIT OF ITEMS.
            # EVEN THOUGH THE LIST WILL UPDATEW ON RESTART, THIS MAKES SURE IT GETS UPDATED FOR THE CURRENT SESSION
            # self.check_if_cbox_item_exists(
            #     self.root.cbox_choose_sequence, [sequence_name]
            # )
            # self.check_if_cbox_item_exists(self.root.cbox_choose_shot, [shot_name])

        else:
            print("you've entered incorrect strings")

    # PETAR CHANGES

    def close_event(self):
        """Delete UI widget."""
        self.deleteLater()


def run_maya():
    """Run tool in maya."""
    result = ms.run_maya(ShotBuilder, WINDOW_OBJECT, WINDOW_TITLE, DOCK_WITH_MAYA_UI)
    return result
