# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""GUI factory classes."""
# Can't find PySide2 modules pylint: disable=I1101

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
from ..data.node_affix_types import RigSideTypes

from importlib import reload

reload(put)
reload(pstyle)
reload(maya_colors)
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
    def create_stack_module(self, module_type: ModuleType):
        """Create a new Stack Gui object."""

    def _build_module_stack_gui(self, label: str, icon_path: str):
        """Build Module stack row UI elements."""
        # stack_widget = QWidget()
        # stack_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # widget_layout = QHBoxLayout()
        # stack_widget.setLayout(widget_layout)

        # # Add Module icon
        # stack_icon_widget = QLabel()
        # stack_icon_widget.setFixedSize(32, 32)
        # stack_icon_widget.setScaledContents(True)
        # icon_pixmap = QtGui.QPixmap(icon_path)
        # icon_pixmap.scaled(QtCore.QSize(32, 32), QtCore.Qt.KeepAspectRatio)
        # stack_icon_widget.setPixmap(icon_pixmap)
        # widget_layout.addWidget(stack_icon_widget)

        # # Add Stack module label/name
        # stack_label = QLabel(label)
        # stack_label.setFixedSize(100, 32)
        # widget_layout.addWidget(stack_label)

        # # Add Spacer
        # widget_layout.addItem(QSpacerItem(20, 40, QSizePolicy.MinimumExpanding))

        # # Add color label as book end
        # stack_color_widget = QLabel()
        # stack_color_widget.setFixedSize(10, 32)
        # widget_layout.addWidget(stack_color_widget)
        # pstyle.set_right_border_color(
        #     stack_color_widget, 6, maya_colors.RGBColorOverride.YELLOW
        # )

        # Get selected item as parent item. If none are selected, add to root level
        parent_object = self._stack_widget.currentItem()
        if parent_object is None:
            # if self._stack_widget.
            parent_object = self._stack_widget

        # Create new tree item
        new_item = QTreeWidgetItem(parent_object)

        new_item.setText(0, label)
        new_item.setIcon(0, QtGui.QIcon(QtGui.QPixmap(icon_path)))

        # Add new widget to Tree item
        # self._stack_widget.setItemWidget(new_item, 0, stack_widget)

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
        module_labels = [item["label"] for item in found_modules]

        # Iterate name till the label doesn't exist in Stack
        i = 1
        while i < 100:
            if not f"{module_type.value['label']}_{i}" in module_labels:
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

    def create_stack_module(self, module_type: ModuleType):
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
        new_item = self._build_module_stack_gui(
            new_module_label, module_type.value["icon"]
        )
        new_item.setData(
            0, QtCore.Qt.UserRole, {"label": new_module_label, "type": module_type}
        )
        return new_item


# class BipedStackFactory(StackFactory):
#     """Create various Biped Gui modules to add to stack tree.

#     Args:
#         StackFactory (StackFactory): Abstract factory class.
#     """

#     def create_biped_stack_module(self, module_type: ModuleType):
#         LOG.debug("Adding %s type Gui object to module stack...", module_type)
#         if (
#             module_type == ModuleType.ROOT
#             and len(
#                 module_stack_util.find_all_modules_of_type(
#                     self._stack_widget, ModuleType.ROOT
#                 )
#             )
#             > 0
#         ):
#             LOG.warning("Root Module already exists! Only one Root Module is allowed.")
#             return False

#         new_module_label = self._build_module_label(module_type)
#         new_item = self._build_module_stack_gui(
#             new_module_label, module_stack_util.get_module_icon_path(module_type)
#         )
#         product_details = {"label": new_module_label, "module_type": module_type}

#         new_product: gui_rig_modules.ModuleProduct
#         match module_type:
#             case ModuleType.ROOT:
#                 product_details["side"] = RigSideTypes.CENTER
#                 new_product = gui_rig_modules.RootProduct(
#                     self._details_panel, product_details, self._stack_widget
#                 )
#             case ModuleType.BIPED_SPINE:
#                 product_details["side"] = RigSideTypes.CENTER
#                 new_product = gui_rig_modules.BipedSpineProduct(
#                     self._details_panel, product_details, self._stack_widget
#                 )

#         new_item.setData(0, QtCore.Qt.UserRole, new_product)
#         return True
