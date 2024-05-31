# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""GUI factory classes."""

from abc import ABC, abstractmethod
import logging
import os

# Import PySide modules
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSpacerItem,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from Core import core_paths as cpath
from Core.ui.UIUtilTools.src import pyside_util_tools as put
from Core.ui.UIUtilTools.src import pyside_styling_util as pstyle
from Core.util import maya_colors

from . import gui_rig_modules, module_stack_util
from ..data.module_types import ModuleType
from ..data import module_metadata
from ..data.node_affix_types import RigSideTypes

from maya import cmds

from importlib import reload

reload(put)
reload(pstyle)
reload(maya_colors)
reload(module_metadata)
reload(gui_rig_modules)

# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 2)}"

# Full path to where .ui files are stored
RSRC_PATH = f"{MODULE_PATH}/resources"

LOG = logging.getLogger(os.path.basename(__file__))


# Abstract Factories
class StackFactory(ABC):
    def __init__(self, stack_widget: QTreeWidget, details_panel: QVBoxLayout):
        self._stack_widget = stack_widget
        self._details_panel = details_panel
        self._item_height = 64

    @abstractmethod
    def create_stack_module(
        self, module_type: ModuleType, parent_item: QTreeWidgetItem = None
    ):
        """Create a new Stack Gui object."""

    def _build_module_stack_gui(
        self, label: str, icon_path: str, parent_item: QTreeWidgetItem = None
    ):
        """Build Module stack row UI elements."""
        # Get selected item as parent item. If none are selected, add to root level
        # Create new tree item
        if parent_item is None:
            new_item = QTreeWidgetItem(self._stack_widget)
        else:
            new_item = QTreeWidgetItem(parent_item)
            parent_item.addChild(new_item)

        new_item.setText(0, label)
        new_item.setIcon(0, QtGui.QIcon(QtGui.QPixmap(icon_path)))

        return new_item

    def _build_module_label(self, module_type: ModuleType):
        new_module_label = f"{module_type.value['label']}_1"
        if module_type == ModuleType.ROOT:
            new_module_label = module_type.value["label"]

        found_modules = module_stack_util.find_all_modules_of_type(
            self._stack_widget, module_type, True
        )
        # No modules found. Default to regular type name with _#
        if len(found_modules) == 0:
            return new_module_label

        # Get list of module product labels
        module_labels = [item.text(0) for item in found_modules]

        # Iterate name till the label doesn't exist in Stack
        i = 1
        while i < 100:
            if (
                not f"{module_type.value['label']}_{i}" in module_labels
                and not cmds.objExists(f"{module_type.value['label']}_{i}")
            ):
                new_module_label = f"{module_type.value['label']}_{i}"
                break
            i += 1

        return new_module_label


# Concrete Factories
class GuiStackFactory(StackFactory):
    """Create various Biped Gui modules to add to stack tree.

    Args:
        StackFactory (StackFactory): Abstract factory class.
    """

    def create_stack_module(
        self,
        module_type: ModuleType,
        parent_item: QTreeWidgetItem = None,
        item_metadata: module_metadata.ModuleConfig = None,
    ):
        LOG.debug("Adding %s type Gui object to module stack...", module_type)
        # Must have a Root module to add a child to
        if (
            not module_type == ModuleType.ROOT
            and len(
                module_stack_util.find_all_modules_of_type(
                    self._stack_widget, module_type.ROOT, True
                )
            )
            == 0
        ):
            LOG.warning("Must have a Root Module built first.")
            return None

        # Only one Root module is allowed
        if (
            module_type == ModuleType.ROOT
            and len(
                module_stack_util.find_all_modules_of_type(
                    self._stack_widget, ModuleType.ROOT, True
                )
            )
            > 0
        ):
            LOG.warning("Root Module already exists! Only one Root Module is allowed.")
            return None

        new_module_label = self._build_module_label(module_type)
        if item_metadata is not None:
            new_module_label = item_metadata.metanode

        new_item = self._build_module_stack_gui(
            new_module_label, module_type.value["icon"], parent_item
        )
        new_item.setData(
            0, QtCore.Qt.UserRole, {"label": new_module_label, "type": module_type}
        )
        return new_item
