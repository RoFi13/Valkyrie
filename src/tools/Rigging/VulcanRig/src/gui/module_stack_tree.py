# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""Modified QTreeWidget class for Vulcan Rig tool."""

from __future__ import annotations
import logging
import os
from typing import TYPE_CHECKING

# Import PySide modules
from PySide6 import QtCore
from PySide6.QtWidgets import QSizePolicy, QTreeWidget, QTreeWidgetItem

from Core import core_paths as cpath

if TYPE_CHECKING:
    from Rigging.VulcanRig.src.vulcan_rig import VulcanRig

# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 2)}"

# Full path to where .ui files are stored
RSRC_PATH = f"{MODULE_PATH}/resources"

LOG = logging.getLogger(os.path.basename(__file__))


class StackModuleTree(QTreeWidget):
    """Modified Tree Widget for Module stack in Vulcan Rig UI."""

    def __init__(self, parent_window: VulcanRig):
        super().__init__()
        self._parent_window = parent_window
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        self.setMinimumWidth(300)
        self.setDragDropMode(QTreeWidget.InternalMove)
        self.setHeaderHidden(True)
        self.setIndentation(15)
        self.setUniformRowHeights(True)
        self.setItemsExpandable(True)
        self.setAnimated(True)
        self.setAutoScrollMargin(25)
        self.setDragEnabled(True)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.setSelectionBehavior(QTreeWidget.SelectItems)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setSizeAdjustPolicy(QTreeWidget.AdjustToContents)
        self.setObjectName("tree_module_stack")
        self.item_picked_up: QTreeWidgetItem
        self.old_parent: QTreeWidgetItem

    def startDrag(self, supportedActions):  # pylint: disable=invalid-name
        """Start item drag with grabbing item and its parent."""
        item = self.currentItem()
        if item:
            self.item_picked_up = item
            self.old_parent = item.parent()
        super().startDrag(supportedActions)

    def dropEvent(self, event):  # pylint: disable=invalid-name
        """Drop item to new location in tree and update modules and metadata."""
        super().dropEvent(event)
        new_parent = self.item_picked_up.parent()
        if not new_parent or new_parent == self.old_parent:
            return
        # Update parent and child relationships
        module_picked_up = self._parent_window.current_modules[self.item_picked_up]
        old_parent_module = self._parent_window.current_modules[self.old_parent]
        new_parent_module = self._parent_window.current_modules[new_parent]
        old_parent_module.remove_child(module_picked_up)
        new_parent_module.add_child(module_picked_up)
