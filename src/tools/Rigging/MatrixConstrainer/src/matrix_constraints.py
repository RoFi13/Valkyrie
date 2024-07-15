# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""
Tool for creating and handling matrix constraints. Only works with constraints built
with this tool.
"""

import ast
import logging
import sys
import os
import platform
import json
from typing import Dict, List, TypedDict

# Imported modules should be put at the head of every tool
from maya import cmds
from maya import OpenMaya
from maya import OpenMayaMPx

# Import PySide modules
from PySide6.QtGui import QAction, QIcon, QPixmap
from PySide6.QtCore import QPoint, QSize, Qt
from PySide6.QtWidgets import QMainWindow, QMenu, QTreeWidgetItem
from PySide6.QtUiTools import QUiLoader

# Imported Custom Modules
from Core import core_paths as cpath
from Core import maya_start as ms
from Core.ui.UIUtilTools.src import pyside_util_tools as put

from . import matrix_constraints_commands as mcon

from importlib import reload

reload(mcon)


# Window title and object names
WINDOW_TITLE = "Matrix Constrainer"
WINDOW_OBJECT = "MatrixConstrainerObject"

LOADER = QUiLoader()

# Maya-specific
DOCK_WITH_MAYA_UI = False

# Main paths
MAIN_PATHS = cpath.core_paths()

# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 1)}"

# Full path to where .ui files are stored
RSRC_PATH = f"{MODULE_PATH}/resources"

LOG = logging.getLogger(os.path.basename(__file__))


class MatrixConstrainer(QMainWindow):
    """Matrix Constrainer utility tool."""

    def __init__(self, parent=None):
        """Initialize instance of tool.

        Set up the default UI state.

        Args:
            parent (None, optional): Optional parent object to init from.
        """
        super().__init__(parent)

        # Instance variables
        # UI commands must remain active inside instance or else UI signals will
        # be garbage collected.
        self.commands: Dict[mcon.ConstraintMethod, mcon.MatrixConstraintCommand] = {}

        # Final UI setup
        # Set up default UI settings
        self.ui_settings = {
            "main_ui_file": f"{RSRC_PATH}/ui/matrix_constrainer.ui",
            "min_size": [],
            "max_size": [],
        }

        self.root = put.setup_class_ui(
            self, WINDOW_OBJECT, WINDOW_TITLE, self.ui_settings
        )

        # Final Setup for UI
        self.setup_ui()
        self.setup_signals()

    def setup_ui(self):
        """Set up default UI elements."""
        for constraint_method in mcon.ConstraintMethod:
            self.commands[constraint_method] = mcon.MatrixConstraintCommand(
                constraint_method, self
            )

    def setup_signals(self):
        """Connect signals to methods."""
        self.root.btn_parent_offset.clicked.connect(
            self.commands[mcon.ConstraintMethod.PARENT_OFFSET].create_constraint
        )
        self.root.btn_parent_no_offset.clicked.connect(
            self.commands[mcon.ConstraintMethod.PARENT_NO_OFFSET].create_constraint
        )
        self.root.btn_point_offset.clicked.connect(
            self.commands[mcon.ConstraintMethod.POINT_OFFSET].create_constraint
        )
        self.root.btn_point_no_offset.clicked.connect(
            self.commands[mcon.ConstraintMethod.POINT_NO_OFFSET].create_constraint
        )
        # Remove constraint
        self.root.btn_remove_constraint.clicked.connect(
            self.commands[mcon.ConstraintMethod.REMOVE_CONSTRAINT].remove_constraint
        )

        # self.root.btn_head_module.clicked.connect(
        #     vulcan_window.commands[ModuleType.BIPED_HEAD].add_module_to_stack
        # )

        # # Core module
        # if ModuleType.ROOT not in self.commands:
        #     root_command = msu.AddModuleCommand(ModuleType.ROOT, self)
        #     self.commands[ModuleType.ROOT] = root_command

        # self.root.btn_root_module.clicked.connect(
        #     self.commands[ModuleType.ROOT].add_module_to_stack
        # )

        # self.tree_stack.itemClicked.connect(self.get_gui_module_details)

        # self.root.btn_ue_skeleton.clicked.connect(
        #     bind_proxy_module.create_unreal_bind_skeleton
        # )
        # self.root.btn_finalize_bpx.clicked.connect(
        #     bind_proxy_module.finalize_bind_skeleton
        # )
        # self.root.btn_dev_open_base_file.clicked.connect(
        #     lambda: self.dev_open_file(True)
        # )
        # self.root.btn_dev_open_wip_file.clicked.connect(
        #     lambda: self.dev_open_file(False)
        # )


def run_maya():
    # Run tool in maya
    ms.run_maya(MatrixConstrainer, WINDOW_OBJECT, WINDOW_TITLE, DOCK_WITH_MAYA_UI)
