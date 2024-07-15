# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""Stack Module UI utility functions."""
# Can't find PySide2 modules pylint: disable=I1101

from __future__ import annotations
import ast
import logging
import os
from typing import TYPE_CHECKING

from maya import cmds

# Import PySide modules
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QMainWindow, QTreeWidget, QTreeWidgetItem

from Core import core_paths as cpath
from Core.ui.UIUtilTools.src import pyside_util_tools as put

from . import gui_rig_modules, stack_handler
from . import gui_factories
from ..data.module_types import ModuleType
from ..data import module_metadata, build_options
from ..util import vulcan_utils as vutil

if TYPE_CHECKING:
    from ..vulcan_rig import VulcanRig

from importlib import reload

reload(put)
reload(stack_handler)
reload(module_metadata)
reload(gui_factories)
reload(build_options)
reload(vutil)

# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 2)}"

# Full path to where .ui files are stored
RSRC_PATH = f"{MODULE_PATH}/resources"

LOG = logging.getLogger(os.path.basename(__file__))


class ModuleCommand:
    """Command interface"""

    def __init__(self, module_type: ModuleType, vulcan_window: VulcanRig):
        self._module_type = module_type
        self._vulcan_window = vulcan_window

    def add_module_to_stack(self):
        """Command execution."""
        raise NotImplementedError("You should implement this method")


class AddModuleCommand(ModuleCommand):
    """Concrete command to add a module"""

    def add_module_to_stack(self):
        # Logic to add the module to the module_stack
        LOG.info("Adding %s to Stack...", self._module_type)
        stack_handler.generate_module(self._module_type, self._vulcan_window)


def find_all_modules_of_type(
    stack_widget: QTreeWidget, search_type: ModuleType, return_modules: bool = False
):
    """Find all Modules of a specific type.

    Args:
        stack_widget (QTreeWidget): Tree widget to search through.
        search_type (ModuleType): Type of Module to find.

    Returns:
        list(gui_rig_modules.ModuleProduct): List of found Module Product objects.
    """
    if stack_widget.topLevelItemCount() == 0:
        return []

    found_module_objects = []
    for i in range(stack_widget.topLevelItemCount()):
        top_item = stack_widget.topLevelItem(i)
        iterate_tree_items(top_item, search_type, found_module_objects, return_modules)

    return found_module_objects


def iterate_tree_items(
    tree_item: QTreeWidgetItem,
    search_type: ModuleType,
    found_objects: list,
    return_modules: bool = False,
):
    """Recursively iterate over Tree items based on Module Type.

    Args:
        tree_item (QTreeWidgetItem): Tree Widget to search through.
        search_type (ModuleType): What type of Module to find.
        found_objects (list): List of all found objects.

    Returns:
        bool: True if successfully iterated over tree items. Otherwise, return False.
    """
    item_data = tree_item.data(0, QtCore.Qt.UserRole)

    if not isinstance(item_data, dict):
        LOG.error("Tree Item %s doesn't contain a Module data!", tree_item)
        return False

    if item_data["type"] == search_type:
        # Whether to return module class objects or QTreeWidgetItem objects.
        if return_modules:
            found_objects.append(item_data)
        else:
            found_objects.append(tree_item)

    # Recurse into children
    for i in range(tree_item.childCount()):
        child = tree_item.child(i)
        iterate_tree_items(child, search_type, found_objects)

    return True


def get_module_icon_path(module_type: ModuleType):
    module_icons = {
        ModuleType.ROOT: f"{RSRC_PATH}/icons/root_icons/root_icon.png",
        ModuleType.BIPED_SPINE: f"{RSRC_PATH}/icons/biped_icons/spine_icon.png",
        ModuleType.BIPED_HEAD: f"{RSRC_PATH}/icons/biped_icons/head_icon.png",
        ModuleType.BIPED_SHOULDER: f"{RSRC_PATH}/icons/biped_icons/shoulder_icon.png",
        ModuleType.BIPED_ARM: f"{RSRC_PATH}/icons/biped_icons/arm_icon.png",
        ModuleType.BIPED_HAND: f"{RSRC_PATH}/icons/biped_icons/hand_icon.png",
        ModuleType.BIPED_LEG: f"{RSRC_PATH}/icons/biped_icons/leg_icon.png",
        ModuleType.BIPED_FOOT: f"{RSRC_PATH}/icons/biped_icons/foot_icon.png",
    }
    return module_icons[module_type]


def add_biped_creation_modules(vulcan_window: QMainWindow):
    """Add Biped module buttons to UI.

    Args:
        vulcan_window (QtWidgets.QMainWindow): Main window object for Vulcan tool.
    """
    # Clear Members grid of other module buttons\
    put.clear_grid_layout(vulcan_window.root.grid_module_members)

    # Spine Module
    btn_spine_module = put.create_new_button(
        icon_path=f"{RSRC_PATH}/icons/biped_icons/spine_icon.png",
        icon_size=QtCore.QSize(64, 64),
        minimum_size=QtCore.QSize(64, 64),
        maximum_size=QtCore.QSize(64, 64),
    )
    if not ModuleType.BIPED_SPINE in vulcan_window.commands:
        vulcan_window.commands[ModuleType.BIPED_SPINE] = AddModuleCommand(
            ModuleType.BIPED_SPINE, vulcan_window
        )

    # Head Module
    btn_head_module = put.create_new_button(
        icon_path=f"{RSRC_PATH}/icons/biped_icons/head_icon.png",
        icon_size=QtCore.QSize(64, 64),
        minimum_size=QtCore.QSize(64, 64),
        maximum_size=QtCore.QSize(64, 64),
    )
    if not ModuleType.BIPED_HEAD in vulcan_window.commands:
        vulcan_window.commands[ModuleType.BIPED_HEAD] = AddModuleCommand(
            ModuleType.BIPED_HEAD, vulcan_window
        )

    # Shoulder Module
    btn_shoulder_module = put.create_new_button(
        icon_path=f"{RSRC_PATH}/icons/biped_icons/shoulder_icon.png",
        icon_size=QtCore.QSize(64, 64),
        minimum_size=QtCore.QSize(64, 64),
        maximum_size=QtCore.QSize(64, 64),
    )
    if not ModuleType.BIPED_SHOULDER in vulcan_window.commands:
        vulcan_window.commands[ModuleType.BIPED_SHOULDER] = AddModuleCommand(
            ModuleType.BIPED_SHOULDER, vulcan_window
        )

    # Arm Module
    btn_arm_module = put.create_new_button(
        icon_path=f"{RSRC_PATH}/icons/biped_icons/arm_icon.png",
        icon_size=QtCore.QSize(64, 64),
        minimum_size=QtCore.QSize(64, 64),
        maximum_size=QtCore.QSize(64, 64),
    )
    if not ModuleType.BIPED_ARM in vulcan_window.commands:
        vulcan_window.commands[ModuleType.BIPED_ARM] = AddModuleCommand(
            ModuleType.BIPED_ARM, vulcan_window
        )

    # Hand Module
    btn_hand_module = put.create_new_button(
        icon_path=f"{RSRC_PATH}/icons/biped_icons/hand_icon.png",
        icon_size=QtCore.QSize(64, 64),
        minimum_size=QtCore.QSize(64, 64),
        maximum_size=QtCore.QSize(64, 64),
    )
    if not ModuleType.BIPED_HAND in vulcan_window.commands:
        vulcan_window.commands[ModuleType.BIPED_HAND] = AddModuleCommand(
            ModuleType.BIPED_HAND, vulcan_window
        )

    # Leg Module
    btn_leg_module = put.create_new_button(
        icon_path=f"{RSRC_PATH}/icons/biped_icons/leg_icon.png",
        icon_size=QtCore.QSize(64, 64),
        minimum_size=QtCore.QSize(64, 64),
        maximum_size=QtCore.QSize(64, 64),
    )
    if not ModuleType.BIPED_LEG in vulcan_window.commands:
        vulcan_window.commands[ModuleType.BIPED_LEG] = AddModuleCommand(
            ModuleType.BIPED_LEG, vulcan_window
        )

    # Foot Module
    btn_foot_module = put.create_new_button(
        icon_path=f"{RSRC_PATH}/icons/biped_icons/foot_icon.png",
        icon_size=QtCore.QSize(64, 64),
        minimum_size=QtCore.QSize(64, 64),
        maximum_size=QtCore.QSize(64, 64),
    )
    if not ModuleType.BIPED_FOOT in vulcan_window.commands:
        vulcan_window.commands[ModuleType.BIPED_FOOT] = AddModuleCommand(
            ModuleType.BIPED_FOOT, vulcan_window
        )

    # Add widgets to grid
    vulcan_window.root.grid_module_members.addWidget(btn_spine_module, 0, 0)
    vulcan_window.root.grid_module_members.addWidget(btn_head_module, 0, 1)
    vulcan_window.root.grid_module_members.addWidget(btn_shoulder_module, 0, 2)
    vulcan_window.root.grid_module_members.addWidget(btn_arm_module, 1, 0)
    vulcan_window.root.grid_module_members.addWidget(btn_hand_module, 1, 1)
    vulcan_window.root.grid_module_members.addWidget(btn_leg_module, 1, 2)
    vulcan_window.root.grid_module_members.addWidget(btn_foot_module, 2, 1)

    # Connect signals
    btn_spine_module.clicked.connect(
        vulcan_window.commands[ModuleType.BIPED_SPINE].add_module_to_stack
    )
    btn_head_module.clicked.connect(
        vulcan_window.commands[ModuleType.BIPED_HEAD].add_module_to_stack
    )
    btn_shoulder_module.clicked.connect(
        vulcan_window.commands[ModuleType.BIPED_SHOULDER].add_module_to_stack
    )
    btn_arm_module.clicked.connect(
        vulcan_window.commands[ModuleType.BIPED_ARM].add_module_to_stack
    )
    btn_hand_module.clicked.connect(
        vulcan_window.commands[ModuleType.BIPED_HAND].add_module_to_stack
    )
    btn_leg_module.clicked.connect(
        vulcan_window.commands[ModuleType.BIPED_LEG].add_module_to_stack
    )
    btn_foot_module.clicked.connect(
        vulcan_window.commands[ModuleType.BIPED_FOOT].add_module_to_stack
    )
